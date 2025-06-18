from google.adk.agents import SequentialAgent

# Import all sub-agents
from .sub_agents.intent_parser.agent import intent_parser_agent
from .sub_agents.compound_searcher.agent import compound_searcher_agent
from .sub_agents.plant_mapper.agent import plant_mapper_agent
from .sub_agents.recommender.agent import recommender_agent
from .sub_agents.music.agent import music_agent
from .sub_agents.mental_support.agent import mental_support_agent
#from Aroma_Agents.tools.tts_tool import generate_audio_tts

from google.adk.agents import SequentialAgent
# Define pipeline
aroma_agent = SequentialAgent(
    name="Aroma_Agents",
    description="An emotional support agent pipeline combining aroma, music, and text-based care.",
    sub_agents=[
        intent_parser_agent,
        compound_searcher_agent,
        plant_mapper_agent,
        recommender_agent,
        mental_support_agent, # Using the agent with the new native TTS service
        music_agent,
    ],
)

root_agent = aroma_agent