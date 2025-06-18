# gemini_tts_generator.py

import mimetypes
import os
import struct
from pathlib import Path
from google import genai
from google.genai import types


class GeminiTTSGenerator:
    def __init__(self, api_key: str, voice: str = "Zephyr", model: str = "gemini-2.5-flash-preview-tts"):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.voice_name = voice

    def generate_audio(self, text: str, output_path: str = "output", base_filename: str = "tts_audio") -> str:
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=text)],
            ),
        ]

        config = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.voice_name
                    )
                )
            ),
        )

        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        file_index = 0
        output_file_path = None

        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config,
        ):
            parts = chunk.candidates[0].content.parts if chunk.candidates else None
            if parts and parts[0].inline_data and parts[0].inline_data.data:
                inline_data = parts[0].inline_data
                mime = inline_data.mime_type or "audio/mpeg"
                extension = mimetypes.guess_extension(mime) or ".mp3"
                data = inline_data.data

                # Only convert to WAV if it's raw PCM data (e.g., audio/L16)
                if mime.startswith("audio/L"):
                    data = self.convert_to_wav(data, mime)
                    extension = ".wav"

                filename = output_dir / f"{base_filename}_{file_index}{extension}"
                with open(filename, "wb") as f:
                    f.write(data)
                    print(f"✅ Saved audio to: {filename}")
                output_file_path = str(filename)
                file_index += 1

        return output_file_path

    @staticmethod
    def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
        params = GeminiTTSGenerator.parse_audio_mime_type(mime_type)
        bits_per_sample = params["bits_per_sample"]
        rate = params["rate"]
        num_channels = 1
        data_size = len(audio_data)
        bytes_per_sample = bits_per_sample // 8
        block_align = num_channels * bytes_per_sample
        byte_rate = rate * block_align
        chunk_size = 36 + data_size

        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",
            chunk_size,
            b"WAVE",
            b"fmt ",
            16,
            1,
            num_channels,
            rate,
            byte_rate,
            block_align,
            bits_per_sample,
            b"data",
            data_size,
        )
        return header + audio_data

    @staticmethod
    def parse_audio_mime_type(mime_type: str) -> dict:
        bits_per_sample = 16
        rate = 24000
        parts = mime_type.split(";")
        for param in parts:
            param = param.strip()
            if param.lower().startswith("rate="):
                try:
                    rate = int(param.split("=")[1])
                except:
                    pass
            elif param.startswith("audio/L"):
                try:
                    bits_per_sample = int(param.split("L")[1])
                except:
                    pass
        return {"bits_per_sample": bits_per_sample, "rate": rate}
