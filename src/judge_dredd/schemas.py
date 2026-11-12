from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class ReviewInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    reviewer: str = Field(min_length=1, max_length=160)
    opinion: Literal["agree", "disagree", "need_more_evidence", "abstain"]
    rationale: str = Field(min_length=1, max_length=20000)
    assessment_id: str | None = None
