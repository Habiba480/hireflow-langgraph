from models.state import CandidateState

def assess_skillset(state: CandidateState) -> CandidateState:
    """Decide next step based on experience level."""
    if state.experience == "junior":
        state.decision = "hr"
    elif state.experience == "mid":
        state.decision = "recruiter"
    elif state.experience == "senior":
        state.decision = "recruiter"
    else:
        state.decision = "reject"
    return state
