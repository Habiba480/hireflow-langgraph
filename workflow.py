from langgraph.graph import StateGraph, END
from models.state import CandidateState
from nodes.categorize import categorize_experience
from nodes.assess import assess_skillset
from nodes.recruiter import escalate_to_recruiter
from nodes.reject import reject_application
from nodes.hr import schedule_hr_interview

def build_workflow():
    """Build the candidate recruitment workflow graph."""
    graph = StateGraph(CandidateState)

    graph.add_node("categorize_experience", categorize_experience)
    graph.add_node("assess_skillset", assess_skillset)
    graph.add_node("escalate_to_recruiter", escalate_to_recruiter)
    graph.add_node("reject_application", reject_application)
    graph.add_node("schedule_hr_interview", schedule_hr_interview)

    graph.set_entry_point("categorize_experience")
    graph.add_edge("categorize_experience", "assess_skillset")

    graph.add_conditional_edges(
        "assess_skillset",
        lambda state: state.decision,
        {
            "recruiter": "escalate_to_recruiter",
            "reject": "reject_application",
            "hr": "schedule_hr_interview",
        },
    )

    graph.add_edge("escalate_to_recruiter", END)
    graph.add_edge("reject_application", END)
    graph.add_edge("schedule_hr_interview", END)

    return graph.compile()
