from fastapi import FastAPI
from app.schemas import QueryRequest, QueryResponse
from app.graph import graph

app = FastAPI(title="LangGraph Research Copilot API")


@app.get("/")
def root():
    return {"message": "LangGraph Research Copilot API is running"}


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    result = graph.invoke({
        "question": request.question,
        "route": "",
        "retrieved_docs": [],
        "sources": [],
        "tool_output": "",
        "answer": ""
    })

    return QueryResponse(
        answer=result["answer"],
        route=result["route"],
        sources=result.get("sources", []),
        tool_used=result["route"] in ["tool", "both"]
    )