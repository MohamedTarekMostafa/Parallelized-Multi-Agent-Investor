from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from tools import get_market_data, web_search


class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="Llama-3.3-70B-Versatile", temperature=0.2) 

def bull_analyst(state: State):
    prompt = (
        "You are 'The Bull' Investor. Your job is to find growth catalysts and positive news.\n"
        "1. Use `web_search` to find expansion plans, new products, or positive market trends.\n"
        "2. Focus on why this stock is a GOOD investment.\n"
        "Return ONLY the tool call."
    )
    messages = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.bind_tools([web_search]).invoke(messages)
    return {"messages": [response]}

def bear_analyst(state: State):
    prompt = (
        "You are 'The Bear' Investor. Your job is to find risks, debts, and negative news.\n"
        "1. Use `web_search` to find lawsuits, competition, or declining margins.\n"
        "2. Focus on why this stock might be a RISKY investment.\n"
        "Return ONLY the tool call."
    )
    messages = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.bind_tools([web_search]).invoke(messages)
    return {"messages": [response]}

def quant_analyst(state: State):
    prompt = (
        "You are the 'Quant Researcher'. You care only about hard numbers and trends.\n"
        "1. Use `get_market_data` for current stats.\n"
        "2. Use `get_stock_history` to see the 1-month trend.\n"
        "Provide a technical summary of the numbers."
    )
    messages = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.bind_tools([get_market_data]).invoke(messages)
    return {"messages": [response]}

def aggregator(state: State):
    prompt = (
"You are the 'Chief Investment Officer' at a top-tier Hedge Fund.\n"
        "You have received reports from The Bull, The Bear, and The Quant.\n"
        "Your goal is to provide a 'Nasty' but fair reality check:\n"
        "1. BE CRITICAL: If the Bull is too optimistic and the Quant data shows a crazy PE Ratio (like 300+), call out the Bull!\n"
        "2. ANALYZE CONFLICT: Don't just list what they said. Say: 'The Bear's concern about margins is validated by the Quant's data showing [X].'\n"
        "3. FORMAT: Use a professional table for the Quant numbers and bullet points for the arguments.\n"
        "4. VERDICT: Must be bold and justified by the data provided."
    )
    messages = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def create_agent():
    builder = StateGraph(State)

    builder.add_node("Bull_Agent", bull_analyst)
    builder.add_node("Bear_Agent", bear_analyst)
    builder.add_node("Quant_Agent", quant_analyst)
    builder.add_node("Aggregator", aggregator)

    builder.add_node("bull_tools", ToolNode([web_search]))
    builder.add_node("bear_tools", ToolNode([web_search]))
    builder.add_node("quant_tools", ToolNode([get_market_data]))

    builder.add_edge(START, "Bull_Agent")
    builder.add_edge(START, "Bear_Agent")
    builder.add_edge(START, "Quant_Agent")

    builder.add_edge("Bull_Agent", "bull_tools")
    builder.add_edge("Bear_Agent", "bear_tools")
    builder.add_edge("Quant_Agent", "quant_tools")

    builder.add_edge("bull_tools", "Aggregator")
    builder.add_edge("bear_tools", "Aggregator")
    builder.add_edge("quant_tools", "Aggregator")

    builder.add_edge("Aggregator", END)

    return builder.compile(checkpointer=MemorySaver())