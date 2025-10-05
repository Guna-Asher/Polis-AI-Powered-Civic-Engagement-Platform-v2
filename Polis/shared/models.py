from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class SentimentLevel(str, Enum):
    STRONGLY_OPPOSE = "strongly_oppose"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    SUPPORT = "support"
    STRONGLY_SUPPORT = "strongly_support"

class ClauseFeedback(BaseModel):
    clause_id: str
    clause_text: str
    sentiment: SentimentLevel
    tags: List[str]
    free_text: Optional[str] = None

class LegislationSummary(BaseModel):
    title: str
    summary: str
    key_points: List[str]
    clauses: List[Dict[str, Any]]

class CivicPulseData(BaseModel):
    total_feedback: int
    sentiment_distribution: Dict[SentimentLevel, float]
    tag_cloud: Dict[str, int]
    clause_sentiments: Dict[str, Dict[SentimentLevel, int]]
    demographic_breakdown: Optional[Dict[str, Any]] = None