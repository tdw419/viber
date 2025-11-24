
from pydantic import BaseModel
from typing import List
from .agent import Agent

class Debate(BaseModel):
    id: int
    topic: str
    participants: List[Agent]
    messages: List[str] = []
