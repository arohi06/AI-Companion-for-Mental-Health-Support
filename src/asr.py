import speech_recognition as sr

def transcribe_from_microphone(language_code: str = "en-IN", timeout_sec: int = 6):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=timeout_sec)
    try:
        text = r.recognize_google(audio, language=language_code)
        return text
    except Exception:
        return ""