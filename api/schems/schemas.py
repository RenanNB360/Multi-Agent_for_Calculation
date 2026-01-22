from pydantic import BaseModel
from typing import Any, Dict


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    type: str
    content: Any
    raw: Dict[str, Any] | None = None