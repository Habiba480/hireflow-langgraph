# HireFlow LangGraph

**HireFlow LangGraph** is a candidate recruitment workflow system built with **LangGraph** and **Streamlit**. It automates candidate evaluation, skill assessment, and routing to HR interviews or recruiter review, streamlining the hiring process.

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)

  * [1. Streamlit Web App](#1-streamlit-web-app)
  * [2. CLI Mode](#2-cli-mode)
* [Project Structure](#project-structure)
* [Workflow Description](#workflow-description)
* [Contributing](#contributing)
* [License](#license)

## Features

* Web interface for candidate screening using Streamlit
* CLI mode for command-line workflow execution
* Automates candidate evaluation with a state-based workflow
* Categorizes candidate experience and assesses skill sets
* Routes candidates to HR interview, recruiter review, or rejection
* Integrates with CV parsing and LLM services
* Extensible and configurable using LangGraph

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Habiba480/hireflow-langgraph.git
cd hireflow-langgraph
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Requires Python 3.8 or higher.

## Usage

### 1. Streamlit Web App

Run the web interface:

```bash
streamlit run app.py
```

Steps:

1. Upload a candidate CV (PDF, DOCX, or TXT).
2. Preview the extracted CV text.
3. Candidate info is extracted automatically using the LLM.
4. The workflow runs, and the final decision is displayed:

   * Schedule HR interview
   * Escalate to recruiter
   * Reject candidate

### 2. CLI Mode

Run the workflow via command line using `main.py`:

```bash
python main.py
```

Steps:

1. Enter the path to the candidate CV when prompted.
2. The script extracts text from the CV and extracts candidate info using the LLM.
3. A `CandidateState` is created and the workflow is executed.
4. The final decision is printed to the console.

## Project Structure

```
hireflow-langgraph/
│── app.py                 # Streamlit web app
│── main.py                # CLI demo / optional script
│── workflow.py            # Workflow graph builder
│
├── models/
│   └── state.py           # Pydantic CandidateState definition
│
├── nodes/
│   ├── categorize.py      # categorize_experience node
│   ├── assess.py          # assess_skillset node
│   ├── recruiter.py       # escalate_to_recruiter node
│   ├── reject.py          # reject_application node
│   └── hr.py              # schedule_hr_interview node
│
├── services/
│   ├── cv_parser.py       # Extract text from CV files
│   └── llm.py             # Wrapper for LLM calls
│
└── utils/
    └── logger.py          # Logging helper
```

## Workflow Description

The workflow is implemented using **LangGraph** and consists of the following nodes:

1. **categorize\_experience** – Categorizes candidates based on experience.
2. **assess\_skillset** – Evaluates candidate skills and decides the next step.
3. Conditional routing from `assess_skillset`:

   * `recruiter` → escalates the candidate for recruiter review
   * `reject` → rejects the candidate
   * `hr` → schedules an HR interview
4. **escalate\_to\_recruiter**, **reject\_application**, **schedule\_hr\_interview** – Terminal nodes that complete the workflow.

Additional services:

* **CV Parser** (`services/cv_parser.py`) – Extracts text from uploaded CVs.
* **LLM Wrapper** (`services/llm.py`) – Handles interactions with large language models for candidate analysis.

## Contributing

Contributions are welcome. Submit issues or pull requests to improve functionality or fix bugs.

## License

This project is licensed under the MIT License.
