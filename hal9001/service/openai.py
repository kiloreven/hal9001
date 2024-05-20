from datetime import datetime
from logging import getLogger

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam, ChatCompletionUserMessageParam

from hal9001.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

logger = getLogger()

MAX_MESSAGES = 100
# Stack of messages for the AI context
MESSAGES: list[ChatCompletionMessageParam] = [ChatCompletionUserMessageParam(role="user", content=settings.AI_CONTEXT)]


def _add_message(prompt: str) -> None:
    """
    Adds a message to the accumulated message queue
    """
    global MESSAGES
    _max = MAX_MESSAGES + 1  # we want to add one to the stack
    if len(MESSAGES) > _max:
        context = MESSAGES.pop(0)
        MESSAGES = [context] + MESSAGES[0:_max]
    MESSAGES.append(ChatCompletionUserMessageParam(role="user", content=prompt))


def get_ai_response(prompt: str) -> str:
    _add_message(prompt)
    response = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=MESSAGES,
        temperature=settings.AI_TEMPERATURE,
        max_tokens=settings.AI_MAX_TOKENS,
        top_p=settings.AI_TOP_P,
        frequency_penalty=settings.AI_FREQUENCY_PENALTY,
    )
    _save_response(prompt, response)
    content = response.choices[0].message.content or ""
    logger.info(f"Got AI response: {content} ({response.usage.prompt_tokens if response.usage else 'N/A'} tokens)")
    return content


def _save_response(prompt: str, response: ChatCompletion) -> None:
    """
    Save response to logfile if one is configured in settings
    """
    if not response:
        return None

    def _format_ai_logline(_r: ChatCompletion) -> str:
        completion_tokens = str(_r.usage.completion_tokens) if _r.usage else "N/A"
        total_tokens = str(_r.usage.total_tokens) if _r.usage else "N/A"
        _content = _r.choices[0].message.content
        content = _content.replace("\n", "") if _content else ""
        return " | ".join([str(datetime.now()), prompt, content, completion_tokens, total_tokens]) + "\n"

    if settings.AI_RESPONSES_LOGFILE:
        with open(settings.AI_RESPONSES_LOGFILE, "a") as f:
            f.write(_format_ai_logline(response))
