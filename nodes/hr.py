from models.state import CandidateState
from utils.logger import log

def schedule_hr_interview(state: CandidateState) -> CandidateState:
    log(f"📅 Scheduling HR interview for {state.name} ({state.experience})...")
    return state
