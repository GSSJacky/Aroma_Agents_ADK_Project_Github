# agent.py

from pydantic import BaseModel
from typing import List, Optional
from google.adk.agents import LlmAgent
from .prompt import PLANT_MAPPER_PROMPT
from Aroma_Agents.utils.config import PLANT_MAPPER_MODEL


# Output schema for plant_mapper
class PlantInfo(BaseModel):
    plant_name: str
    part_used: str
    additional_info: Optional[str] = None

class PlantMapperInput(BaseModel):
    compound_candidates: List[str]

class PlantMapperOutput(BaseModel):
    matching_plants_or_products: List[PlantInfo]  # ✅ 用于满足 prompt 替换变量需求

plant_mapper_agent = LlmAgent(
    name="plant_mapper_agent",
    model=PLANT_MAPPER_MODEL,
    instruction=PLANT_MAPPER_PROMPT,  # Prompt 中包含 {+compound_candidates+}
    input_schema=PlantMapperInput,
    output_schema=PlantMapperOutput,
    output_key="matching_plants_or_products"
)
