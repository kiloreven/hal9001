import json
from io import BytesIO
from logging import getLogger
from random import randint
from typing import Any

import librosa.effects
from paho.mqtt.client import Client, MQTTMessage
from pydantic import ValidationError
from scipy.io import wavfile

from ..conf import settings
from ..prompts import PROMPTS
from ..types.message import Message
from .google import get_tts_audio
from .openai import get_ai_response
from .pygame import play_sound

logger = getLogger()


def tts_post_processing(data: BytesIO) -> BytesIO:
    """
    Do some DSP processing on the response we get from Google's TTS to make it sound a bit more like HAL
    """
    logger.info("Starting audio postprocessing")
    out_buffer = BytesIO()
    y, sr = librosa.load(data)
    logger.info("Post process: speed")
    # slow = librosa.effects.time_stretch(y, rate=0.8)
    logger.info("Post process: pitch")
    shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=-2, scale=True)
    wavfile.write(out_buffer, sr, shifted)
    logger.info("Finished audio postprocessing")
    return out_buffer


def play_text(text: str) -> None:
    audio = get_tts_audio(text)
    audio = tts_post_processing(audio)
    play_sound(audio)


def _get_random_prompt() -> str:
    num = randint(0, len(PROMPTS) - 1)
    print(len(PROMPTS), num)
    return PROMPTS[num]


def get_gpt_prompt(prompt: str) -> str:
    if prompt == "AUTO":
        prompt = _get_random_prompt()
        logger.info(f'Got automatic prompt: "{prompt}"')
    return get_ai_response(prompt)


def play_prompt(prompt: str) -> None:
    result = get_gpt_prompt(prompt)
    play_text(result)


def handle_message(_: Client, __: Any, msg: MQTTMessage) -> None:
    logger.info(f"Got MQTT message: {msg.payload.decode('utf-8')}")
    try:
        message = Message(**json.loads(msg.payload))
        if message.type == "text":
            play_text(message.text)
        elif message.type == "prompt":
            play_prompt(message.text)
        else:
            logger.error("Invalid message type")
    except json.JSONDecodeError:
        logger.error("Invalid JSON")
    except ValidationError as e:
        logger.error(f"Invalid for Message model: {e}")

    return None


def start_mqtt_listen() -> None:
    """
    Connect to MQTT queue and do something anytime we get something on the MQTT queue
    """
    logger.info("Connecting to MQTT queue")
    client = Client()
    client.on_message = handle_message
    result = client.connect(settings.MQTT_HOST, settings.MQTT_PORT)
    logger.info(f"MQTT connection status: {result}")
    client.subscribe(settings.MQTT_TOPIC, qos=1)
    logger.info(f"Connected to MQTT queue, subscribed to topic {settings.MQTT_TOPIC}")
    client.loop_forever()
