import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import ray
from haystack.core.errors import PipelineMaxLoops, PipelineRuntimeError
from ray.actor import ActorHandle
from ray.util.queue import Queue

from ray_haystack.graph import ComponentNode, RayPipelineGraph
from ray_haystack.ray_pipeline_events import (
    ComponentEndEvent,
    ComponentStartEvent,
    PipelineEndEvent,
    PipelineStartEvent,
)
from ray_haystack.ray_pipeline_settings import RayPipelineSettings

# Identifies a MISSING input value, it is not the same as 'None'
MISSING = object()


def setup_logger():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("haystack.ray-pipeline-processor")


@ray.remote
class RayPipelineProcessor:
    def __init__(
        self,
        graph: RayPipelineGraph,
        max_loops_allowed: int,
        ray_settings: RayPipelineSettings,
        component_actors: Dict[str, ActorHandle],
        events_queue: Queue,
        pipeline_inputs: Dict[str, Any],
        include_outputs_from: Set[str],
    ):
        self._graph = graph
        self._max_loops_allowed = max_loops_allowed
        self._ray_settings = ray_settings
        self._component_actors = component_actors
        self._events_queue = events_queue
        self._pipeline_inputs = pipeline_inputs
        self._include_outputs_from = include_outputs_from

        self._inputs: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._outputs: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._component_data: Dict[str, _ComponentData] = {}
        self._back_edges: List[Tuple[ComponentNode, ComponentNode]] = []
        self._visits: Dict[str, int] = defaultdict(int)

        self.logger = setup_logger()

    def run_pipeline(self) -> Dict[str, Any]:
        unfinished = []

        # Update pipeline inputs for each component and assign defaults to non-connected inputs (both if available)
        for node_name, node in self._graph._nodes.items():
            self._component_data[node_name] = _ComponentData(node, self)

        # Obtain components which are ready to run (run_queue) or can potentially run with defaults (wait_queue)
        (run_queue, wait_queue) = self._initial_nodes_to_run()

        self.logger.debug(f"Initial components to run: {run_queue}, waiting queue: {wait_queue}")

        self._events_queue.put_nowait(
            PipelineStartEvent(
                data={
                    "pipeline_inputs": self._pipeline_inputs,
                    "run_queue": [node.get_name() for node in run_queue],
                    "wait_queue": [node.get_name() for node in wait_queue],
                }
            )
        )

        # Initially run components which we can run straight away (no incoming connections)
        for node in run_queue:
            unfinished.append(self._schedule_component_run(node.get_name()))

        while unfinished or wait_queue:
            finished, unfinished = ray.wait(unfinished, num_returns=1)
            next_nodes_to_run: List[Tuple[Union[ComponentNode, None], ComponentNode]] = []

            if finished:
                node_name, outputs = ray.get(finished[0])
                finished_node = self._graph.get_node(node_name)

                # If we finished running a node and it was in a waiting queue, remove it from wait_queue
                if finished_node in wait_queue:
                    self.logger.debug(f"Remove {finished_node} from wait_queue, remaining: {wait_queue}")
                    wait_queue.remove(finished_node)

                self.logger.debug(f"Finished running component {node_name}, outputs {outputs}")

                if not isinstance(outputs, dict):
                    raise PipelineRuntimeError(
                        f"Component '{node_name}' didn't return a dictionary. "
                        "Components must always return dictionaries: check the the documentation."
                    )

                self._events_queue.put_nowait(
                    ComponentEndEvent(
                        data={
                            "name": finished_node.get_name(),
                            "output": outputs,
                            "iteration": self._visits[node_name],
                        }
                    )
                )

                # Increase 'visits' count - track number of times component has ran
                self._visits[node_name] += 1

                # Update (and store) component outputs with most recent invocation results
                self._outputs[node_name] = outputs

                # We will try to run all downstream components which expect inputs from upstream (just finished) node
                next_nodes_to_run = [(finished_node, next_node) for next_node in finished_node.downstream]

                # Update component connected inputs with recent invocation results from 'finished_node'
                for from_node, to_node in next_nodes_to_run:
                    self._component_data[to_node.get_name()].assign_connection_values(from_node, outputs)
            elif wait_queue:
                waiting_node_to_run = wait_queue.pop(0)
                next_nodes_to_run = [(None, waiting_node_to_run)]
                self.logger.debug(f"Running next node from waiting queue {waiting_node_to_run}")

            while next_nodes_to_run:
                (from_node, to_node) = next_nodes_to_run.pop()
                to_node_name = to_node.get_name()
                component_data = self._component_data[to_node_name]

                component_data.prepare_default_values()

                if not component_data.all_inputs_are_ready():
                    self.logger.debug(f"Skip running '{to_node}'. Not enough connected inputs have been triggered.")
                    continue

                if component_data.has_enough_inputs_to_run():
                    if self._visits[to_node_name] > self._max_loops_allowed:
                        msg = f"Maximum loops count ({self._max_loops_allowed}) exceeded for component '{to_node_name}'"
                        raise PipelineMaxLoops(msg)

                    running_component = self._schedule_component_run(to_node_name, sender_name=node_name)
                    unfinished.append(running_component)
                else:
                    self.logger.debug(
                        f"Not enough inputs to run '{to_node}'."
                        "Find waiting downstream components with missing variadic inputs."
                    )
                    self._find_variadic_which_will_receive_a_missing_input(to_node, wait_queue, [to_node_name])

        pipeline_output = self._build_pipeline_outputs()

        self._events_queue.put_nowait(
            PipelineEndEvent(
                data={
                    "output": pipeline_output,
                    "include_outputs_from": [],
                }
            )
        )

        return pipeline_output

    def _find_variadic_which_will_receive_a_missing_input(
        self, from_node: ComponentNode, wait_queue: List[ComponentNode], visited_nodes: Optional[List[str]] = None
    ):
        visited_nodes = visited_nodes or []
        for downstream in from_node.downstream:
            if downstream.get_name() in visited_nodes:
                continue

            visited_nodes.append(downstream.get_name())

            component_data = self._component_data[downstream.get_name()]
            variadic_inputs = component_data.get_non_greedy_variadic_inputs()
            if len(variadic_inputs) > 0:
                for input_value in variadic_inputs:
                    input_value.update_with_missing(from_node=from_node)
                self.logger.debug(f"Adding '{downstream}' with variadic inputs to the waiting queue.")
                if downstream not in wait_queue:
                    wait_queue.append(downstream)

            # Search again, in case more downstream components are variadic and waiting for a missing input
            self._find_variadic_which_will_receive_a_missing_input(downstream, wait_queue, visited_nodes)

    def _schedule_component_run(self, name: str, sender_name: Optional[str] = None):
        actor = self._component_actors[name]
        component_data = self._component_data[name]
        component_inputs = component_data.build_inputs()

        self.logger.debug(f"Schedule '{name}', with inputs: {component_inputs}")

        # Start execution of component (`run`) with given inputs. It is a non-blocking call
        scheduled_run = actor.run_component.remote(component_inputs)  # type:ignore

        self._events_queue.put_nowait(
            ComponentStartEvent(
                data={
                    "name": name,
                    "sender_name": sender_name,
                    "input": component_inputs,
                    "iteration": self._visits[name],
                }
            )
        )

        # After scheduling component execution we will make sure input flags are reset
        component_data.reset_inputs()

        return scheduled_run

    def _build_pipeline_outputs(self):
        result = {}

        for name, output in self._outputs.items():
            if name in self._include_outputs_from:
                result[name] = output
            else:
                consumed_keys = self._graph.get_node(name).get_output_names()
                unconsumed_output = {key: value for key, value in output.items() if key not in consumed_keys}
                if unconsumed_output:
                    result[name] = unconsumed_output

        return result

    def _is_back_edge(self, from_node: ComponentNode, to_node: ComponentNode) -> bool:
        return any(from_node == edge_from and to_node == edge_to for edge_from, edge_to in self._back_edges)

    def _initial_nodes_to_run(self) -> Tuple[List[ComponentNode], List[ComponentNode]]:
        to_run = []
        to_wait = []
        has_cycles = False

        for node_name, node in self._graph._nodes.items():
            if node.in_degree_is_zero():
                to_run.append(node)
                continue

            has_cycles = True
            component_pipeline_inputs = self._pipeline_inputs.get(node_name, {})

            can_run_with_defaults = all(
                input_name in component_pipeline_inputs or node.has_default_value(input_name)
                for input_name in node.get_all_input_names()
            )

            if can_run_with_defaults:
                to_wait.append(node)

        if has_cycles:
            self._back_edges = self._graph.find_back_edges()

        return (to_run, to_wait)


class _ComponentData:
    def __init__(self, node: ComponentNode, processor: "RayPipelineProcessor"):
        self._processor = processor
        self._node = node
        self._pipeline_inputs = processor._pipeline_inputs.get(node.get_name(), {})
        self._inputs: Dict[str, Any] = {}
        self._input_values: Dict[str, _InputValue] = {}

        self.logger = processor.logger
        self._assign_initial_inputs()

    def assign_connection_values(self, from_node: ComponentNode, outputs: Dict[str, Any]):
        output_is_from_loop = self._processor._is_back_edge(from_node, self._node)
        fulfilled_inputs: Set[str] = set()

        for out_name, in_name in self._node._node_in_args[from_node].items():
            connection_value = outputs.get(out_name, MISSING)
            self._input_values[in_name].update_value(
                value=connection_value,
                from_node=from_node,
                out_name=out_name,
            )
            fulfilled_inputs.add(in_name)

        # When
        if output_is_from_loop:
            for input_name, input_value in self._input_values.items():
                if input_name not in fulfilled_inputs and not input_value.is_absent():
                    input_value.update_flags(is_ready=True, can_run=True)

    def prepare_default_values(self):
        for input_name in self._node.get_connected_input_names():
            input_value = self._input_values[input_name]

            if input_value.is_variadic:
                for from_node in input_value.senders:
                    if self._processor._is_back_edge(from_node, self._node):
                        input_value.update_with_missing(from_node=from_node)
            elif input_value.is_absent() and self._node.has_default_value(input_name):
                from_node = input_value.senders[0]
                if self._processor._is_back_edge(from_node, self._node):
                    input_value.update_value_with_default(from_node=from_node)

    def all_inputs_are_ready(self) -> bool:
        return all(value.is_ready for value in self._input_values.values())

    def has_enough_inputs_to_run(self):
        return all(value.can_run for value in self._input_values.values())

    def build_inputs(self):
        for input_name, input_value in self._input_values.items():
            if input_value.is_variadic:
                non_missing_values = [value for value in input_value.value if value is not MISSING]
                if len(non_missing_values) > 0:
                    self._inputs[input_name] = non_missing_values
            elif input_value.value is not MISSING:
                self._inputs[input_name] = input_value.value
        return self._inputs

    def reset_inputs(self):
        for input_value in self._input_values.values():
            input_value.reset()

    def get_non_greedy_variadic_inputs(self) -> List["_InputValue"]:
        return [
            input_value
            for input_value in self._input_values.values()
            if input_value.is_variadic and not input_value.is_greedy
        ]

    def _assign_initial_inputs(self):
        for input_name in self._node.get_all_input_names():
            input_values = _InputValue(node=self._node, input_name=input_name)
            self._input_values[input_name] = input_values

            if input_name in self._pipeline_inputs:
                pipeline_input_value = self._pipeline_inputs[input_name]
                self._inputs[input_name] = pipeline_input_value
                input_values.value = pipeline_input_value
                input_values.update_flags(is_ready=True, can_run=True)
            elif self._node.has_default_value(input_name) and not self._node.is_connected(input_name):
                default_value = self._node.get_default_value(input_name)
                self._inputs[input_name] = default_value
                input_values.value = default_value
                input_values.update_flags(is_ready=True, can_run=True)


@dataclass
class _InputValue:
    node: ComponentNode
    input_name: str

    is_variadic: bool = False
    is_greedy: bool = False
    is_connected = False
    senders: List[ComponentNode] = field(default_factory=list)

    is_ready: bool = False
    can_run: bool = False
    value: Union[Any, List[Any]] = None

    _values_per_connection: Dict[ComponentNode, Dict[str, Any]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict())
    )

    def __post_init__(self):
        self.is_variadic = self.node.is_variadic(self.input_name)
        self.is_greedy = self.node.is_greedy(self.input_name)
        self.is_connected = self.node.is_connected(self.input_name)
        self.senders = self.node.get_senders(self.input_name)

    def is_absent(self) -> bool:
        return self.value is None

    def update_value(
        self,
        value: Any,
        from_node: ComponentNode,
        out_name: Optional[str] = None,
        update_flags: Optional[bool] = True,
    ):
        if self.is_variadic:
            self.value = [] if not isinstance(self.value, list) else self.value
            self.value.append(value)
        else:
            self.value = value

        if out_name is None:
            out_name = self.node.get_output_name_from_input(self.input_name, from_node)

        # Keep track of exactly which connection has provided the value
        self._values_per_connection[from_node][out_name] = value

        if update_flags:
            # Once value is updated lets update corresponding flags
            # is_ready will become `True` if all inputs provided
            # can_run will be `True` if provided inputs are not MISSING
            self._update_flags()

    def update_value_with_default(
        self, from_node: ComponentNode, out_name: Optional[str] = None, update_flags: Optional[bool] = True
    ):
        self.update_value(
            value=self.node.get_default_value(self.input_name),
            from_node=from_node,
            out_name=out_name,
            update_flags=update_flags,
        )

    def update_flags(self, is_ready: Optional[bool] = None, can_run: Optional[bool] = None):
        if is_ready is not None:
            self.is_ready = is_ready

        if can_run is not None:
            self.can_run = can_run

    def update_with_missing(
        self, from_node: ComponentNode, out_name: Optional[str] = None, update_flags: Optional[bool] = True
    ):
        self.update_value(
            value=MISSING,
            from_node=from_node,
            out_name=out_name,
            update_flags=update_flags,
        )

    def reset(self):
        if self.is_variadic:
            self.value = []

        if self.is_connected:
            self.is_ready = False
            self.can_run = False

    def _update_flags(self):
        if self.is_variadic:
            non_missing_values = [input_value for input_value in self.value if input_value is not MISSING]
            has_non_missing_value = len(non_missing_values) > 0

            if self.is_greedy:
                # We are ready to run greedy inputs as soon as at least one non-missing value is available
                enough_values_to_run = has_non_missing_value and len(self.value) > 0
                self.is_ready = self.can_run = enough_values_to_run
            else:
                self.is_ready = len(self.value) >= len(self.senders)
                self.can_run = has_non_missing_value
        else:
            self.is_ready = True
            self.can_run = self.value is not MISSING
