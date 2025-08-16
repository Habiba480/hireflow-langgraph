from models.state import CandidateState
from utils.logger import log

def reject_application(state: CandidateState) -> CandidateState:
    log(f" Rejecting application for {state.name} ({state.experience})...")
    return state
