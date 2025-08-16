import requests
import json
import re

LLM_API_URL = "http://localhost:1234/v1/chat/completions"
LLM_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"

def call_llm(prompt: str) -> str:
    """
    Sends a prompt to the LLM API and returns the text output.
    """
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }

    response = requests.post(LLM_API_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    return data['choices'][0]['message']['content']

def extract_candidate_info(cv_text: str) -> dict:
    """
    Extract candidate info from CV text using the LLM.
    Returns a dictionary: {"name": ..., "years_experience": ..., "skills": [...]}
    """
    prompt = f"""
You are an AI CV parser. Extract the following info from the CV text below:

- Full name
- Total years of professional experience
- List of main skills

Return **ONLY** a single JSON object in this format, no extra text:

{{
  "name": "Full Name",
  "years_experience": <number>,
  "skills": ["skill1", "skill2", ...]
}}

CV Text:
{cv_text}
"""

    response_text = call_llm(prompt)

    # Extract JSON from LLM output using regex
    try:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            candidate_info = json.loads(match.group())
        else:
            candidate_info = {
                "name": "Unknown",
                "years_experience": 0,
                "skills": []
            }
    except json.JSONDecodeError:
        candidate_info = {
            "name": "Unknown",
            "years_experience": 0,
            "skills": []
        }

    return candidate_info
