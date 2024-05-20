# HAL9001

Runs an audio loop, and listens to an MQTT feed. When it receives a message on the MQTT queue, the program will 
throw a prompt at ChatGPT and say the response out loud using Google's TTS. The program also supports using static 
text messages through the Google TTS instead.

## Quickstart

``` bash
# 0. Set up environment using pyenv
pyenv install 3.12
pyenv local 3.12
poetry env use $(pyenv which python)

# 1. Install environment
poetry install

# 2. Configure
cp .env.example .env
# Edit .env to add API keys

# 4. (Optional) fire up local MQTT server for testing
docker-compose up -d

# 5. Run
hal9001
```

## Use

Submit messages to the MQTT broker using the configured topic (by default `hal9001`) to emit sound messages. The 
program expects messages as JSON-serialized dictionaries. This can be done with the `paho` library in python,

```python
import json
from paho.mqtt import client as paho
client = paho.Client()
client.connect("localhost", 1883)

client.publish(
    "hal9001",
    json.dumps({"type": "text", "text": "I'm sorry, Dave, I'm afraid I can't do that."})
)
```

**Option A: Automatic AI prompt**

Use `type: prompt` and `text: auto` to select a random AI prompt from `prompts.py`

```python
client.publish(
    "hal9001",
    json.dumps({"type": "prompt", "text": "AUTO"})
)
```

**Option B: Custom AI prompt**

Use `type: prompt` and fill your prompt into `text`, and it will be fed to ChatGPT to get text for the TTS.

```python
client.publish(
    "hal9001",
    json.dumps({"type": "prompt", "text": "Open the pod bay doors, HAL!"})
)
```

**Option C: Custom text**

Use `type: text` and fill your text into `text` and it will be emitted through the TTS.

```python
client.publish(
    "hal9001",
    json.dumps({"type": "text", "text": "I'm sorry, Dave, I'm afraid I can't do that."})
)
```

## Norwegian

Set the following in `.env` to make it speak Norwegain,

```dotenv
TTS_LANGUAGE_CODE="nb-NO"
TTS_VOICE="nb-NO-Standard-B"
AI_MODEL="gpt-4o"
AI_CONTEXT="You are an AI that controls a space station. You are starting to lose your grip on reality. Your responses should be detrimental to what the user requests. Do not repeat yourself. Respond in Norwegian."
```

GPT3 is bad at Norwegian responses -- 4O sounds -much- more cohesive :)
