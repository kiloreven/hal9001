from enum import Enum

from pydantic import BaseModel


class Message(BaseModel):
    class Type(str, Enum):
        text = "text"
        prompt = "prompt"

    type: Type
    text: str
