import logging
import time
from typing import Any, Dict, Mapping, Optional

import ray
import ray.workflow
from haystack.core.component import InputSocket

from ray_haystack.serialization import ComponentWrapper


@ray.remote
class ComponentActor:
    def __init__(self, name: str, component: ComponentWrapper):
        self.name = name
        self.component_wrapper = component

        self.inputs: Dict[str, Any] = {}
        self.outputs: Dict[str, Any] = {}

        self._warmed_up: Optional[bool] = None

        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(f"haystack.ray.component-{name}")

    def get_component(self):
        return self.component_wrapper.get_component()

    def get_input_sockets(self) -> Dict[str, InputSocket]:
        return self.get_component().__haystack_input__._sockets_dict

    def get_input_socket(self, name: str) -> InputSocket:
        return self.get_input_sockets()[name]

    def run_component(self, inputs: Dict[str, Any]):
        self.inputs.update(inputs)

        if self._has_enough_inputs_to_execute():
            self._warm_up_if_needed()

            time.sleep(1)
            result = self.get_component().run(**self.inputs)

            if isinstance(result, Mapping):
                self.outputs.update(result)

            return (self.name, result)

        self.logger.debug(f"Not enough inputs to run '{self.name}', inputs: {self.inputs}. Returning empty result")
        return (self.name, {})  # Empty Result

    def _warm_up_if_needed(self):
        component = self.get_component()
        if hasattr(component, "warm_up") and not self._warmed_up:
            self.logger.info(f"Warming up component {self.name}...")
            component.warm_up()
            self._warmed_up = True

    def _has_enough_inputs_to_execute(self) -> bool:
        for name in self.get_input_sockets().keys():
            if name not in self.inputs:
                return False
        return True

    def __repr__(self):
        return f"ComponentActor([{self.name}])"
