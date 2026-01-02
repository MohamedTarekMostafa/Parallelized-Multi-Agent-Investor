# ⚖️ 🤖 BullVBear: Agentic Financial Intelligence
A Multi-Agent ecosystem where specialized Bulls and Bears clash to deliver data-driven investment verdicts.
[![Framework - LangGraph](https://img.shields.io/badge/Framework-LangGraph-blue.svg)](https://langchain-ai.github.io/langgraph/)
[![Model - Llama 3.3 70B](https://img.shields.io/badge/Model-Llama_3.3_70B-orange.svg)](https://groq.com/)
[![Architecture - Parallel DAG](https://img.shields.io/badge/Architecture-Parallel_DAG-red.svg)](#-architecture)

This is a production-grade **Multi-Agent Financial Intelligence System**. Instead of a simple chatbot, it uses a **Parallel Fan-out/Fan-in Architecture** to simulate a professional investment committee, where conflicting perspectives (Bullish vs. Bearish) are synthesized to provide a data-driven, non-biased investment verdict.

## 🌟 The Innovation: "Conflict-Driven Reasoning"
Most AI financial tools suffer from **Confirmation Bias**. This system solves this by forcing a "clash" between specialized agents:
* **🟢 The Bull Agent**: Programmed to find catalysts, growth, and optimism.
* **🔴 The Bear Agent**: Programmed to find risks, debts, and market threats.
* **📊 The Quant Agent**: Provides the "Ground Truth" using hard market data (P/E, Dividends, Volatility).
* **⚖️ The Aggregator (Chief Investment Officer)**: Acts as the judge, resolving conflicts and tailoring the verdict to the user's specific **Memory-stored Risk Profile**.

---

## 🏗️ Architecture
The system is built on a **Directed Acyclic Graph (DAG)** using `LangGraph`:

* **Parallel Execution**: Research and Data Fetching nodes run concurrently, drastically reducing latency.
* **Stateful Persistence**: Uses `MemorySaver` to track user financial profiles (e.g., age, risk tolerance) across sessions.
* **Decoupled Tools**: Each agent has its own tool node, ensuring clean data context and preventing "hallucination contamination."

---

## 🛠️ Tech Stack
* **Orchestration**: `LangGraph` (for complex agentic workflows).
* **Brain**: `Llama-3.3-70B-Versatile` (via Groq for ultra-fast inference).
* **Real-time Data**: `yfinance` (Market stats) & `Tavily Search` (Financial news).
* **UI**: `Streamlit` (Interactive Dashboard with Multi-tab views).
* **Observability**: `Langfuse` (Tracing & Monitoring).

---

## 🧪 Real-World Test Case (Reasoning in Action)
**User Profile Stored in Memory:** "65-year-old retiree, low risk tolerance."
**Question:** "Analyze AMD vs Intel."

**The Result:** Even though AMD is showing massive growth potential (The Bull's view), the **Aggregator** issues a verdict favoring **Intel**. 
**Reason:** The system identifies that Intel's stable dividends and lower valuation (Quant data) align better with a **Retiree's Risk Profile**, proving the system doesn't just "chat"—it thinks and remembers.

---

