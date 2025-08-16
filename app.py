import os
import streamlit as st
from services.cv_parser import extract_text_from_cv
from services.llm import extract_candidate_info
from models.state import CandidateState
from workflow import build_workflow

st.set_page_config(page_title="HireFlow", page_icon="", layout="centered")
st.title("HireFlow - Candidate Screening")

uploaded_file = st.file_uploader(
    "📂 Upload a CV (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:
    # Preserve original extension
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext not in [".pdf", ".docx", ".txt"]:
        st.error("Unsupported file format. Please upload PDF, DOCX, or TXT.")
    else:
        temp_path = f"temp_cv{file_ext}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract CV text
        st.info("Extracting CV text...")
        cv_text = extract_text_from_cv(temp_path)
        st.subheader("CV Text Preview")
        st.text_area("CV Text", cv_text, height=300)

        # Extract candidate info using LLM
        st.info("Extracting candidate info using LLM...")
        candidate_info = extract_candidate_info(cv_text)

        st.subheader("Extracted Candidate Info")
        st.json(candidate_info)

        # Prepare candidate state
        candidate = CandidateState(
            name=candidate_info.get("name", "Unknown"),
            years_experience=candidate_info.get("years_experience", 0),
            skills=candidate_info.get("skills", []),
            cv_text=cv_text,
        )

        # Run workflow
        workflow = build_workflow()
        result = workflow.invoke(candidate)

        # Dictionary-safe access
        st.subheader("Final Decision")
        decision = result.get("decision", "reject")

        if decision == "hr":
            st.success(f"Schedule HR interview for {candidate.name}")
        elif decision == "recruiter":
            st.success(f"Escalate {candidate.name} to recruiter")
        else:
            st.error(f"Reject {candidate.name}")
