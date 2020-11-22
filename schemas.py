from typing import List

from pydantic import BaseModel


class SingleRequest(BaseModel):
    text: str


class BatchRequest(BaseModel):
    text_list: List[str]


class SentimentScore(BaseModel):
    Mixed: float
    Negative: float
    Neutral: float
    Positive: float


class SentimentResponse(BaseModel):
    sentiment: str
    language: str
    message: str = 'Successfully processed'
    score: SentimentScore


class BatchResponse(BaseModel):
    response: List[SentimentResponse]
