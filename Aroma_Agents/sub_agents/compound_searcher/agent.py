from pydantic import BaseModel
from typing import Optional
from google.adk.agents import LlmAgent
from Aroma_Agents.sub_agents.compound_searcher.prompt import COMPOUND_PROMPT
from Aroma_Agents.utils.config import COMPOUND_SEARCHER_MODEL


# 输入模式：接收来自 intent_parser 的情绪、偏好等
class CompoundSearchInput(BaseModel):
    mood: Optional[str] = None
    context: Optional[str] = None
    preferences: Optional[str] = None

# 输出模式：生成目标化合物或关键词
#class CompoundSearchOutput(BaseModel):
#    target_compound: str
#    reason: Optional[str] = None

class CompoundSearcherOutput(BaseModel):
    compound_candidates: list[str]  # 原本是 target_compound 和 reason，现在改为 list[str]

compound_searcher_agent = LlmAgent(
    name="compound_searcher_agent",
    model=COMPOUND_SEARCHER_MODEL,
    instruction=COMPOUND_PROMPT,
    input_schema=CompoundSearchInput,
    output_schema=CompoundSearcherOutput,
    output_key="compound_candidates",  # 与 output_schema 对应
)

