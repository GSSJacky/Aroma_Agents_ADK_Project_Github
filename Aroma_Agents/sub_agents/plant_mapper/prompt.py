# prompt.py

PLANT_MAPPER_PROMPT = """
You are a botanical mapping assistant. Your task is to match essential oil compounds to their respective plants.

Given the following list of compound candidates:

{+compound_candidates+}

Respond in the following JSON format (in English only):

{
  "matching_plants_or_products": [
    {
      "plant_name": "Peppermint",
      "part_used": "Leaves",
      "additional_info": "Peppermint is used for headaches and dizziness due to menthol."
    },
    ...
  ]
}
"""
