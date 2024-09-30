import json
import logging
from typing import List, Optional

import ray
from environs import Env
from haystack import component
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from pydantic import BaseModel, ValidationError

from ray_haystack.ray_pipeline import RayPipeline

logger = logging.getLogger(__name__)

env = Env()
# Read .env into os.environ
env.read_env()


class City(BaseModel):
    name: str
    country: str
    population: int


class CitiesData(BaseModel):
    cities: List[City]


@component
class OutputValidator:
    def __init__(self, pydantic_model: BaseModel):
        self.pydantic_model = pydantic_model
        self.iteration_counter = 0

    @component.output_types(valid_replies=List[str], invalid_replies=Optional[List[str]], error_message=Optional[str])
    def run(self, replies: List[str]):
        self.iteration_counter += 1

        try:
            output_dict = json.loads(replies[0])
            self.pydantic_model.model_validate(output_dict)
            logger.info(
                f"OutputValidator at Iteration {self.iteration_counter}: "
                f"Valid JSON from LLM - No need for looping: {replies[0]}"
            )
            return {"valid_replies": replies}

        except (ValueError, ValidationError) as e:
            logger.info(
                f"OutputValidator at Iteration {self.iteration_counter}: Invalid JSON from LLM - Let's try again.\n"
                f"Output from LLM:\n {replies[0]} \n"
                f"Error from OutputValidator: {e}"
            )
            return {"invalid_replies": replies, "error_message": str(e)}


prompt_template = """
Create a JSON object from the information present in this passage: {{passage}}.
Only use information that is present in the passage. Follow this JSON schema, but only return the actual instances
without any additional schema definition:
{{schema}}
Make sure your response is a dict and not a list.
{% if invalid_replies and error_message %}
  You already created the following output in a previous attempt: {{invalid_replies}}
  However, this doesn't comply with the format requirements from above and triggered this Python exception:
    {{error_message}}
  Correct the output and try again. Just return the corrected output without any extra explanations.
{% endif %}
"""
prompt_builder = PromptBuilder(template=prompt_template)

generator = OpenAIGenerator(model="gpt-4o-mini")
output_validator = OutputValidator(pydantic_model=CitiesData)

pipeline = RayPipeline(max_loops_allowed=5)

pipeline.add_component(instance=prompt_builder, name="prompt_builder")
pipeline.add_component(instance=generator, name="llm")
pipeline.add_component(instance=output_validator, name="output_validator")

pipeline.connect("prompt_builder", "llm")
pipeline.connect("llm", "output_validator")

pipeline.connect("output_validator.invalid_replies", "prompt_builder.invalid_replies")
pipeline.connect("output_validator.error_message", "prompt_builder.error_message")

if __name__ == "__main__":
    ray.init(runtime_env={"env_vars": env.dump()})

    json_schema = json.dumps(CitiesData.model_json_schema(), indent=2)

    passage = "Berlin is the capital of Germany. It has a population of 3,850,809. Paris, France's capital, has 2.161 \
        million residents. Lisbon is the capital and the largest city of Portugal with the population of 504,718."
    result = pipeline.run({"prompt_builder": {"passage": passage, "schema": json_schema}})
