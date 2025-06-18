# Aroma_Agents/sub_agents/music/agent.py

from google.adk.agents.llm_agent import LlmAgent
from pydantic import BaseModel
from typing import Optional
from .prompt import MUSIC_AGENT_PROMPT
from Aroma_Agents.tools import music_tool
from Aroma_Agents.utils.config import MUSIC_AGENT_MODEL



class MusicInput(BaseModel):
    mood: str
    context: Optional[str] = None


class MusicOutput(BaseModel):
    lyrics: str


music_agent = LlmAgent(
    name="music_agent",
    model=MUSIC_AGENT_MODEL,
    description="Generates a healing-themed original song lyrics based on mood and context.",
    instruction=MUSIC_AGENT_PROMPT,
    input_schema=MusicInput,
    #output_schema=MusicOutput,
    tools=[
        music_tool.create_and_generate_music 
    ], 
)
