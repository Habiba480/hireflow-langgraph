from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class CandidateState(BaseModel):
    """Workflow state for a candidate application."""

    name: str = Field(..., description="Candidate's name")
    cv_text: Optional[str] = None
    years_experience: Optional[int] = None
    skills: List[str] = []
    experience: Optional[Literal["junior", "mid", "senior"]] = None
    decision: Optional[Literal["recruiter", "reject", "hr"]] = None
