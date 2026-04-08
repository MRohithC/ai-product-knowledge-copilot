from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.retriever import simple_retriever
from app.tools import get_external_post
from app.prompts import ROUTER_PROMPT, ANSWER_PROMPT


#llm = ChatOpenAI(
 #   model=CHAT_MODEL,
  #  temperature=0,
   # api_key=OPENAI_API_KEY
#)


class GraphState(TypedDict):
    question: str
    route: str
    retrieved_docs: List[str]
    sources: List[str]
    tool_output: str
    answer: str


def route_node(state):
    question = state["question"].lower()

    if "external" in question:
        route = "tool"
    elif "compare" in question:
        route = "both"
    else:
        route = "retrieval"

    return {"route": route}


def retrieval_node(state):
    question = state["question"]
    docs = simple_retriever(question)

    retrieved_texts = [doc.page_content for doc in docs]
    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    return {
        "retrieved_docs": retrieved_texts,
        "sources": sources
    }


def tool_node(state: GraphState):
    data = get_external_post()
    tool_output = f"title: {data['title']}\nbody: {data['body']}"
    return {"tool_output": tool_output}


def answer_node(state):
    question = state["question"]
    retrieved_docs = state.get("retrieved_docs", [])
    tool_output = state.get("tool_output", "")
    route = state.get("route", "")

    if not retrieved_docs and not tool_output:
        answer = (
            f"Question: {question}\n\n"
            "I could not find relevant information in the internal document or tool output."
        )
        return {"answer": answer}

    context = "\n\n".join(retrieved_docs)

    if route == "retrieval":
        answer = (
            f"Question: {question}\n\n"
            f"Based on internal documents:\n{context[:500]}"
        )
    elif route == "tool":
        answer = (
            f"Question: {question}\n\n"
            f"Based on external tool output:\n{tool_output}"
        )
    else:
        answer = (
            f"Question: {question}\n\n"
            f"Based on internal documents:\n{context[:300]}\n\n"
            f"External Info:\n{tool_output}"
        )

    return {"answer": answer}


def route_decision(state: GraphState):
    route = state["route"]
    if route == "retrieval":
        return "retrieval"
    if route == "tool":
        return "tool"
    return "both"


builder = StateGraph(GraphState)

builder.add_node("route_node", route_node)
builder.add_node("retrieval", retrieval_node)
builder.add_node("tool", tool_node)
builder.add_node("answer", answer_node)

builder.set_entry_point("route_node")

builder.add_conditional_edges(
    "route_node",
    route_decision,
    {
        "retrieval": "retrieval",
        "tool": "tool",
        "both": "retrieval"
    }
)

builder.add_edge("retrieval", "tool")
builder.add_edge("tool", "answer")
builder.add_edge("answer", END)

graph = builder.compile()