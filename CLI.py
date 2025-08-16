from services.cv_parser import extract_text_from_cv
from services.llm import extract_candidate_info
from models.state import CandidateState
from workflow import build_workflow

if __name__ == "__main__":
    file_path = input(" Enter path to candidate CV (PDF/DOCX/TXT): ").strip()
    cv_text = extract_text_from_cv(file_path)

    print("\n Extracting candidate info using LLM...")
    info = extract_candidate_info(cv_text)
    print(" Extracted Candidate Info:", info)

    candidate = CandidateState(
        name=info.get("name", "Unknown"),
        years_experience=info.get("years_experience", 0),
        skills=info.get("skills", []),
        cv_text=cv_text,
    )

    workflow = build_workflow()
    result = workflow.invoke(candidate)

    print("\n Final Decision:", result.decision)
