"""Motor unificado de síntese de voz (TTS) para os capítulos."""

import os
from typing import Dict, Any

class BaseTTSEngine:
    def synthesize(self, payload: Dict[str, Any], output_path: str) -> str:
        raise NotImplementedError

class EdgeTTSEngine(BaseTTSEngine):
    """Motor Neural com suporte a modulação por SSML e controle de prosódia."""

    def synthesize(self, payload: Dict[str, Any], output_path: str) -> str:
        import edge_tts

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        voice = payload.get("voice_id", "pt-BR-AntonioNeural")
        rate = payload.get("rate", "+0%")
        pitch = payload.get("pitch", "+0Hz")
        volume = payload.get("volume", "+0%")
        speech_text = payload.get("speech_text", "")

        communicator = edge_tts.Communicate(
            text=speech_text,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
        communicator.save_sync(output_path)
        return output_path

def get_engine(engine_name: str = "edge-tts") -> BaseTTSEngine:
    if engine_name == "edge-tts":
        return EdgeTTSEngine()
    else:
        # Padrão seguro
        return EdgeTTSEngine()
