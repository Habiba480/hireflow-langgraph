from models.state import CandidateState
from utils.logger import log

def escalate_to_recruiter(state: CandidateState) -> CandidateState:
    log(f" Escalating {state.name} ({state.experience}) to recruiter...")
    return state
