from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    route: str
    sources: List[str]
    tool_used: bool