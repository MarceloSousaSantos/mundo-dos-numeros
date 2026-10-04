"""Integrações opcionais de IA. IA nunca avalia respostas matemáticas."""
import os
from dataclasses import dataclass

@dataclass
class VoiceResult:
    audio: bytes | None = None
    error: str | None = None

def gemini_enabled() -> bool:
    return os.environ.get("ENABLE_GEMINI", "False").lower() == "true" and bool(os.environ.get("GEMINI_API_KEY"))

def generate_narration(text: str) -> VoiceResult:
    """Gera narração curta; falhas retornam resultado controlado, sem vazar segredos."""
    if not gemini_enabled():
        return VoiceResult(error="Gemini está desativado.")
    if not text or len(text) > 500:
        return VoiceResult(error="Texto de narração inválido.")
    try:
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        model = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")
        response = client.models.generate_content(model=model, contents=f"Narre em português brasileiro, com voz clara, alegre e acolhedora para crianças: {text}")
        data = getattr(getattr(response, "candidates", [None])[0], "content", None)
        return VoiceResult(audio=getattr(data, "audio", None))
    except Exception:
        return VoiceResult(error="A narração não está disponível agora.")
