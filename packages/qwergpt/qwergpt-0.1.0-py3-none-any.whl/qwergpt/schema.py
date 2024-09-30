from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from pydantic import BaseModel


class ToolDef(BaseModel):
    type: str
    function: Dict[str, Any]


class ToolCall(BaseModel):
    id: str
    type: str
    function: Dict[str, Any]


class Message(BaseModel):
    role: str
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


@dataclass
class TaskDef:
    name: str
    desc: str
    guidance: str


class Task(BaseModel):
    task_id: str
    instruction: str
    dependent_task_ids: list[str]
    code: Optional[str] = ''
    result: Optional[str] = ''


class Question(BaseModel):
    question: str
    answer: str


class Document(BaseModel):
    content: str
    metadata: Optional[dict]
