import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = str(pathlib.Path(__file__).parent.parent.resolve())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HAL_", env_file_encoding="utf-8")

    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "hal9001/#"
    LOOP_FILENAME: str = os.path.join(PROJECT_ROOT, "audio/space_drone.wav")

    GOOGLE_API_KEY: str
    TTS_LANGUAGE_CODE: str = "en-US"  # "nb-NO"
    TTS_VOICE: str = "en-US-Standard-I"  # "nb-NO-Standard-B"

    OPENAI_API_KEY: str
    AI_CONTEXT: str = (
        "You are an AI that controls a space station. You are starting to lose your grip on "
        "reality. Your responses should be detrimental to what the user requests. Do not "
        "repeat yourself."
    )
    AI_MODEL: str = "gpt-3.5-turbo-0125"
    AI_TEMPERATURE: float = 1.2
    AI_MAX_TOKENS: int = 128
    AI_TOP_P: float = 1.0
    AI_FREQUENCY_PENALTY: float = 1.0
    AI_RESPONSES_LOGFILE: str | None = None
