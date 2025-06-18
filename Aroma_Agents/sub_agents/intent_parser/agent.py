from pydantic import BaseModel
from typing import Optional
from google.adk.agents import LlmAgent
from .prompt import INTENT_PROMPT
from Aroma_Agents.utils.config import INTENT_PARSER_MODEL

class IntentInput(BaseModel):
    user_input: str


class IntentOutput(BaseModel):
    mood: Optional[str] = None
    context: Optional[str] = None
    preferences: Optional[str] = None


intent_parser_agent = LlmAgent(
    name="intent_parser_agent",
    model=INTENT_PARSER_MODEL,
    instruction=INTENT_PROMPT,  # instruction 现在已包含 {{ user_input }}
    input_schema=IntentInput,
    output_schema=IntentOutput,
    output_key="intent",
)
