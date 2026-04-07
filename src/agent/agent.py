import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Ensure project root is on sys.path so imports work regardless of how this is run
ROOT_DIR = Path(__file__).parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.agent.tools import search_flights, search_hotels, calculate_budget

load_dotenv(ROOT_DIR / ".env")

# 1. Đọc System Prompt
with open(ROOT_DIR / "system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


# ============================================================
# Conversation Logger – writes one JSON line per event to
# logs/conversation_YYYYMMDD_HHMMSS.jsonl (file-only, no console spam)
# ============================================================

class ConversationLogger:
    def __init__(self, log_dir: Path):
        log_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = log_dir / f"conversation_{self.session_id}.jsonl"

    def log(self, event: str, data: dict) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session": self.session_id,
            "event": event,
            "data": data,
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# Module-level logger reference — set by run_chat() before the graph runs
_conv_logger: ConversationLogger | None = None


# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  → Gọi tool: {tc['name']}({tc['args']})")
            if _conv_logger:
                _conv_logger.log("TOOL_CALL", {"tool": tc["name"], "args": tc["args"]})
    else:
        print("  → Trả lời trực tiếp (không gọi tool)")
        if _conv_logger:
            _conv_logger.log("AI_RESPONSE", {"content": response.content})

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()


# 6. Chat loop (callable from main.py or run directly)
def run_chat() -> None:
    global _conv_logger

    log_dir = ROOT_DIR / "logs"
    _conv_logger = ConversationLogger(log_dir)
    _conv_logger.log("SESSION_START", {"model": "gpt-4o-mini"})
    print(f"[Log] Saving conversation to {_conv_logger.log_file.name}")

    print("=" * 60)
    print("  TravelBuddy – Trợ lý Du lịch Thông minh")
    print("  Gõ 'quit' hoặc 'q' để thoát")
    print("=" * 60)

    conversation_history: list = []
    turn = 0

    while True:
        user_input = input("\nBạn: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            _conv_logger.log("SESSION_END", {"turns": turn})
            print("Tạm biệt! Chúc bạn có chuyến đi vui vẻ 🌏")
            break

        turn += 1
        _conv_logger.log("USER_MESSAGE", {"turn": turn, "content": user_input})

        # Append new user message and pass full history so context is preserved
        conversation_history.append(HumanMessage(content=user_input))

        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": conversation_history})

        # Save full updated history (includes tool calls, observations, AI reply)
        conversation_history = result["messages"]
        final = conversation_history[-1]
        print(f"\nTravelBuddy: {final.content}")


if __name__ == "__main__":
    run_chat()
