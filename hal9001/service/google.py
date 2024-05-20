import io
import json
from logging import getLogger

from google.cloud import texttospeech

from ..conf import settings

logger = getLogger()


def get_tts_client() -> texttospeech.TextToSpeechClient:
    client: texttospeech.TextToSpeechClient = texttospeech.TextToSpeechClient.from_service_account_info(
        json.loads(settings.GOOGLE_API_KEY)
    )
    return client


def get_tts_audio(text: str) -> io.BytesIO:
    client = get_tts_client()
    logger.info(f"Sending to TTS: {text}")
    input_ = texttospeech.SynthesisInput({"text": text})
    voice = texttospeech.VoiceSelectionParams({
        "language_code": settings.TTS_LANGUAGE_CODE,
        "ssml_gender": texttospeech.SsmlVoiceGender.MALE,
        "name": settings.TTS_VOICE,
    })
    audio_config = texttospeech.AudioConfig({"audio_encoding": texttospeech.AudioEncoding.MP3})
    response = client.synthesize_speech(
        input=input_,
        voice=voice,
        audio_config=audio_config,
    )

    return io.BytesIO(response.audio_content)
