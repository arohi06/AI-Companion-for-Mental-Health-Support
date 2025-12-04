import requests
from .config import MURF_API_KEY, MURF_VOICE_ID

def murf_tts_synthesize(text: str, voice_id: str = MURF_VOICE_ID, audio_format: str = "mp3") -> bytes:
    if not MURF_API_KEY:
        return b""
    # Replace with the correct Falcon TTS endpoint and payload per Murf docs.
    url = "https://api.murf.ai/falcon/tts"
    headers = {
        "Authorization": f"Bearer {MURF_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "voice_id": voice_id,
        "style":"Conversational",
        "model:":"Falcon",
        "audio_format": audio_format,
        "params": {
            "speed": 1.0,
            "pitch": 0.0,
            "expressiveness": 0.7
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        return b""
    return resp.content