from pydantic import BaseModel
from typing import List, Optional
from google.adk.agents import LlmAgent
from Aroma_Agents.sub_agents.recommender.prompt import RECOMMENDER_PROMPT
from Aroma_Agents.utils.config import AROMA_RECOMMENDER_MODEL


class RecommenderInput(BaseModel):
    plant_name: str
    use_case: Optional[str] = None


class RecommenderOutput(BaseModel):
    recommended_use: str
    scent_profile: Optional[str] = None
    explanation: Optional[str] = None


recommender_agent = LlmAgent(
    name="recommender_agent",
    model=AROMA_RECOMMENDER_MODEL,
    instruction=RECOMMENDER_PROMPT,
    input_schema=RecommenderInput,
    output_schema=RecommenderOutput,
    output_key="recommendation_result",
)
