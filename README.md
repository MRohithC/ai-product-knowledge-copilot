# AI Product Knowledge Copilot

An AI-powered assistant that answers questions over product documentation using a LangGraph workflow, retrieval system, and FastAPI backend.

## Features
- Multi-step AI workflow using LangGraph
- Query routing (retrieval / tool / hybrid)
- Document-based question answering
- External tool/API integration
- REST API built with FastAPI
- Offline mode (no API required)

## How it Works
1. User submits a question
2. Router decides processing path:
   - Retrieval
   - Tool
   - Both
3. System retrieves relevant document context
4. External API tool (optional) is called
5. Final answer is generated

## Tech Stack
- Python
- LangChain
- LangGraph
- FastAPI
- FAISS (conceptually)
- REST API integration

## Run Locally
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
