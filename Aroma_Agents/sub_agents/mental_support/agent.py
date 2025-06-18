from pydantic import BaseModel
from typing import Optional
from google.adk.agents.llm_agent import Agent
#from Aroma_Agents.utils.gemini_llm import GeminiLLM
from Aroma_Agents.sub_agents.mental_support.prompt import MENTAL_SUPPORT_PROMPT
from Aroma_Agents.utils.config import MENTAL_SUPPORT_MODEL
#from Aroma_Agents.tools.tts_tool import generate_audio_tts
from Aroma_Agents.tools import tts_tool



class MentalSupportInput(BaseModel):
    mood: Optional[str]
    context: Optional[str]


class MentalSupportOutput(BaseModel):
    message: str



mental_support_agent = Agent(
    name="mental_support_agent",
    model=MENTAL_SUPPORT_MODEL,
    instruction=MENTAL_SUPPORT_PROMPT,
    input_schema=MentalSupportInput,
    #output_schema=MentalSupportOutput,
    output_key="mental",
    tools=[
        tts_tool.generate_audio_tool
    ],
)
