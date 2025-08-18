import os
import streamlit as st
import pandas as pd
from services.cv_parser import extract_text_from_cv
from services.llm import extract_candidate_info, match_candidate_to_job
from models.state import CandidateState
from workflow import build_workflow

st.set_page_config(page_title="HireFlow", page_icon="", layout="centered")
st.title("HireFlow - Candidate Screening")

# Step 1: Job description input
st.subheader("Job Description")
job_description = st.text_area("Paste the job description here", height=200)

# Step 2: Multiple CV uploads
uploaded_files = st.file_uploader(
    " Upload one or more CVs (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if job_description and uploaded_files:
    results = []

    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in [".pdf", ".docx", ".txt"]:
            st.error(f"Unsupported file format for {uploaded_file.name}")
            continue

        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract CV text
        cv_text = extract_text_from_cv(temp_path)

        # Extract candidate info + match to JD
        candidate_result = match_candidate_to_job(cv_text, job_description)

        # Save result
        results.append(candidate_result)

        # Display individual candidate result
        st.subheader(f"Results for {uploaded_file.name}")
        st.json(candidate_result)

        # Build workflow for internal decisioning
        candidate = CandidateState(
            name=candidate_result.get("name", "Unknown"),
            years_experience=candidate_result.get("years_experience", 0),
            skills=candidate_result.get("skills", []),
            cv_text=cv_text,
        )

        workflow = build_workflow()
        result = workflow.invoke(candidate)

        # Final decision
        decision = result.get("decision", "reject")
        st.markdown("**Final Decision:**")
        if decision == "hr":
            st.success(f"Schedule HR interview for {candidate.name}")
        elif decision == "recruiter":
            st.success(f"Escalate {candidate.name} to recruiter")
        else:
            st.error(f"Reject {candidate.name}")

    # Step 3: Summary table
    if results:
        st.subheader("Summary of All Candidates")
        summary_data = [
            {
                "Name": r["name"],
                "Experience (yrs)": r["years_experience"],
                "Match Score": r["match_score"],
                "Decision": (
                    "HR Interview" if r["match_score"] >= 70 else
                    "Recruiter Review" if r["match_score"] >= 50 else
                    "Reject"
                )
            }
            for r in results
        ]
        df = pd.DataFrame(summary_data)
        st.dataframe(df)

        # Step 4: Export options
        st.download_button(
            label="📥 Download Summary as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="candidate_summary.csv",
            mime="text/csv"
        )

        st.download_button(
            label="📥 Download Summary as Excel",
            data=df.to_excel(index=False, engine="openpyxl"),
            file_name="candidate_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
