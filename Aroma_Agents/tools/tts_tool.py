# Aroma_Agents/tools/tts_tool.py

from pathlib import Path
# 1. 不再需要导入 Tool 或 ToolContext
from Aroma_Agents.utils.gemini_tts_generator import GeminiTTSGenerator
# 确保从 config.py 中同时导入 API 密钥和模型名称
from Aroma_Agents.utils.config import GOOGLE_API_KEY, TTS_MODEL


# 2. 定义一个具有简单类型签名的普通函数
def generate_audio_tool(text: str, filename: str) -> str:
    """
    Generates an audio file from text using a Text-to-Speech (TTS) engine.

    Args:
        text: The text to be synthesized into audio.
        filename: A unique base filename for the output audio file, without extension.

    Returns:
        A string indicating the result of the operation.
    """
    # 3. 直接使用函数参数，而不是 context.inputs
    if not text:
        message = "⚠️ Missing 'text' input for TTS. Skipping synthesis."
        print(message)  # 使用 print 进行日志记录
        return message

    # 初始化 TTS 生成器
    # (请确保 GeminiTTSGenerator 的实现是正确的，并且能接收这些参数)
    tts = GeminiTTSGenerator(api_key=GOOGLE_API_KEY, model=TTS_MODEL)

    output_dir = Path("audio_outputs")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # 调用实际的生成逻辑
        output_path = tts.generate_audio(
            text=text,
            output_path=str(output_dir),
            base_filename=filename
        )
        success_message = f"Audio successfully generated and saved to {output_path}"
        print(success_message)
        return success_message
    except Exception as e:
        error_message = f"❌ Error during TTS synthesis: {e}"
        print(error_message)
        return error_message