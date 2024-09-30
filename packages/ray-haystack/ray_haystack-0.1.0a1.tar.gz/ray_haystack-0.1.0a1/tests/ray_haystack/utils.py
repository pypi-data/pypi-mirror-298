from typing import Any, Dict, List, Optional, Set, Tuple

from ray_haystack.ray_pipeline import RayPipeline


def run_pipeline(
    pipeline: RayPipeline, inputs: Dict[str, Any], include_outputs_from: Optional[Set[str]] = None
) -> Tuple[Dict[str, Any], List[Any]]:
    result = pipeline.process_nowait(inputs, include_outputs_from=include_outputs_from)

    pipeline_output = result.get_pipeline_output()

    pipeline_events = result.consume_events()
    components_run_order = [
        event.data["name"] for event in pipeline_events if event.type == "ray.haystack.component-start"
    ]

    return (pipeline_output, components_run_order)
