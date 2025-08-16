from models.state import CandidateState

def categorize_experience(state: CandidateState) -> CandidateState:
    """Categorize candidate by years of experience."""
    if state.years_experience is None:
        state.experience = "junior"
    elif state.years_experience < 2:
        state.experience = "junior"
    elif 2 <= state.years_experience < 5:
        state.experience = "mid"
    else:
        state.experience = "senior"
    return state
