import os

COMPOUND_SEARCHER_MODEL = "gemini-2.0-flash"
INTENT_PARSER_MODEL = "gemini-2.0-flash"
PLANT_MAPPER_MODEL = "gemini-2.0-flash"
AROMA_RECOMMENDER_MODEL = "gemini-2.0-flash"
MENTAL_SUPPORT_MODEL = "gemini-2.0-flash"
MUSIC_AGENT_MODEL = "gemini-2.0-flash"
TTS_MODEL = "gemini-2.5-flash-preview-tts"

GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
SUNO_API_KEY = os.environ.get("SUNO_API_KEY")
