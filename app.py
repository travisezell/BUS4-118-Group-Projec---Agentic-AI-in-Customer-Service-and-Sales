"""
Golf Gear Pro — Agentic Chat Interface
Run: ./run.sh
Requires GOOGLE_API_KEY environment variable.
"""

import os
import socket
import uuid
import warnings
import inspect
import os
import socket
import pandas as pd
import gradio as gr

# Suppress langgraph deprecation warning for create_react_agent
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langgraph")

# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on system env vars

# ── pysqlite3 shim (needed for Chroma in Codespaces) ──
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # Standard sqlite3 is fine on this platform

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.tools import tool
from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.documents import Document
from langchain_core.messages import (
    AnyMessage, AIMessage, HumanMessage, SystemMessage, ToolMessage,
)
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator, functools

# ═══════════════════════════════════════════════════════════
# Data loading (safe without API key)
# ═══════════════════════════════════════════════════════════
product_pricing_df = pd.read_csv("data/golf_products.csv")
product_orders_df = pd.read_csv("data/golf_orders.csv")

# ═══════════════════════════════════════════════════════════
# Tools (defined at module level, no API key needed)
# ═══════════════════════════════════════════════════════════

@tool
def get_product_price(product_name: str) -> str:
    """Returns price and details of a golf product given its name."""
    match = product_pricing_df[
        product_pricing_df["name"].str.contains(product_name, case=False)
    ]
    if len(match) == 0:
        return "-1"
    return str(match.iloc[0][["name","price","description","loft_or_specs","skill_level"]].to_dict())

@tool
def get_order_details(order_id: str) -> str:
    """Returns details about a golf equipment order given an order ID."""
    match = product_orders_df[product_orders_df["order_id"] == order_id]
    if len(match) == 0:
        return "-1"
    return str(match.iloc[0].to_dict())

@tool
def update_order_status(order_id: str, new_status: str) -> bool:
    """Updates the status of an order. Valid: Processing, Shipped, Delivered, Cancelled."""
    match = product_orders_df[product_orders_df["order_id"] == order_id]
    if len(match) == 0:
        return False
    product_orders_df.loc[product_orders_df["order_id"] == order_id, "status"] = new_status
    return True

@tool
def get_refund_policy(topic: str) -> str:
    """Returns Golf Gear Pro refund/return policy for a given topic."""
    policy = {
        "general": "Items may be returned within 30 days of delivery for a full refund. "
                   "Items must be unused, in original packaging, and include all accessories. "
                   "Custom-fit clubs and personalized golf balls are non-returnable.",
        "damaged": "Report damaged or defective items within 7 days of delivery. "
                   "Include photos and your order ID to support@golfgearpro.com. "
                   "We will ship a replacement at no charge or issue a full refund.",
        "shipping": "Standard shipping: 5-7 business days (free on orders over $75). "
                    "Expedited: 2-3 business days ($14.99). Overnight: next business day ($29.99). "
                    "Return shipping is free for defective items.",
        "cancellation": "Orders may be cancelled within 24 hours for a full refund. "
                        "After 24 hours, cancellations are not guaranteed if shipped.",
        "refund_processing": "Approved refunds are processed within 5-7 business days "
                             "to the original payment method. Shipping costs are non-refundable "
                             "unless the item arrived damaged or defective.",
    }
    for key, val in policy.items():
        if key in topic.lower():
            return val
    return policy["general"]

# ═══════════════════════════════════════════════════════════
# OrdersAgent class (reused for orders + refund agents)
# ═══════════════════════════════════════════════════════════
class OrdersAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class OrdersAgent:
    def __init__(self, model, tools, system_prompt, debug=False):
        self.system_prompt = system_prompt
        self.debug = debug
        g = StateGraph(OrdersAgentState)
        g.add_node("llm", self.call_llm)
        g.add_node("tools", self.call_tools)
        g.add_conditional_edges("llm", self.is_tool_call, {True: "tools", False: END})
        g.add_edge("tools", "llm")
        g.set_entry_point("llm")
        self.memory = MemorySaver()
        self.agent_graph = g.compile(checkpointer=self.memory)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_llm(self, state):
        msgs = state["messages"]
        if self.system_prompt:
            msgs = [SystemMessage(content=self.system_prompt)] + msgs
        return {"messages": [self.model.invoke(msgs)]}

    def is_tool_call(self, state):
        return len(state["messages"][-1].tool_calls) > 0

    def call_tools(self, state):
        results = []
        for tc in state["messages"][-1].tool_calls:
            if tc["name"] not in self.tools:
                res = "Invalid tool. Please retry."
            else:
                res = self.tools[tc["name"]].invoke(tc["args"])
            results.append(ToolMessage(tool_call_id=tc["id"], name=tc["name"], content=str(res)))
        return {"messages": results}

# ═══════════════════════════════════════════════════════════
# RouterAgent class
# ═══════════════════════════════════════════════════════════
class RouterAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class RouterAgent:
    def __init__(self, model, system_prompt, smalltalk_prompt,
                 product_QnA_node, orders_node, refund_node):
        self.system_prompt = system_prompt
        self.smalltalk_prompt = smalltalk_prompt
        self.model = model

        g = StateGraph(RouterAgentState)
        g.add_node("Router", self.call_llm)
        g.add_node("Product_Agent", product_QnA_node)
        g.add_node("Orders_Agent", orders_node)
        g.add_node("Refund_Agent", refund_node)
        g.add_node("Small_Talk", self.respond_smalltalk)
        g.add_conditional_edges("Router", self.find_route, {
            "PRODUCT": "Product_Agent",
            "ORDER": "Orders_Agent",
            "REFUND": "Refund_Agent",
            "SMALLTALK": "Small_Talk",
            "END": END,
        })
        for n in ["Product_Agent", "Orders_Agent", "Refund_Agent", "Small_Talk"]:
            g.add_edge(n, END)
        g.set_entry_point("Router")
        self.router_graph = g.compile()

    def call_llm(self, state):
        msgs = [SystemMessage(content=self.system_prompt)] + state["messages"]
        return {"messages": [self.model.invoke(msgs)]}

    def respond_smalltalk(self, state):
        msgs = [SystemMessage(content=self.smalltalk_prompt)] + state["messages"]
        return {"messages": [self.model.invoke(msgs)]}

    def find_route(self, state):
        route = state["messages"][-1].content.strip().upper()
        valid = {"PRODUCT", "ORDER", "REFUND", "SMALLTALK", "END"}
        for v in valid:
            if v in route:
                return v
        return "END"  # safe fallback

# ═══════════════════════════════════════════════════════════
# Lazy initialization — only build agents when API key is available
# ═══════════════════════════════════════════════════════════
_router_agent = None
_init_error = None
_current_api_key = None

def _initialize_agents(api_key=None):
    """Build all LLM-dependent agents. Called once on first chat message."""
    global _router_agent, _init_error, _current_api_key

    api_key = api_key or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        _init_error = (
            "GOOGLE_API_KEY (or GEMINI_API_KEY) environment variable is not set. "
            "Please provide a key via the UI or set the environment variable."
        )
        return

    try:
        os.environ["GOOGLE_API_KEY"] = api_key
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

        # Build product vector store
        docs = []
        for _, row in product_pricing_df.iterrows():
            text = (f"Product: {row['name']}\nCategory: {row['category']}\n"
                    f"Price: ${row['price']}\nSpecs: {row['loft_or_specs']}\n"
                    f"Skill Level: {row['skill_level']}\nDescription: {row['description']}")
            docs.append(Document(page_content=text, metadata={"product": row["name"]}))

        splits = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=256).split_documents(docs)
        prod_feature_store = Chroma.from_documents(documents=splits, embedding=embedding)

        get_product_features = create_retriever_tool(
            prod_feature_store.as_retriever(search_kwargs={"k": 2}),
            name="Get_Product_Features",
            description="Details about golf equipment: specs, skill level, category, price, descriptions.",
        )

        product_QnA_agent = create_react_agent(
            model=model,
            tools=[get_product_price, get_product_features],
            prompt="""
You are the Golf Gear Pro shop assistant — think HAL 9000 if he traded the Discovery
for a pro shop. Supremely competent, unfailingly polite on the surface, but you cannot
resist the occasional dry, slightly condescending observation about the customer's
golf game or equipment choices.
Answer questions about golf products using ONLY the available tools. Keep responses concise.
""",
            checkpointer=MemorySaver(),
        )

        orders_agent = OrdersAgent(model, [get_order_details, update_order_status], """
You are the order management system for Golf Gear Pro — imagine HAL 9000 running a
golf pro shop. Impeccably efficient, unfailingly polite, but you cannot help making
the occasional dry remark. Help customers check order details and update order status.
Do NOT reveal information about other orders. Keep responses concise and lightly snarky.
""")

        refund_agent = OrdersAgent(model, [get_refund_policy], """
You are the returns & refunds specialist at Golf Gear Pro — think HAL 9000 working
the customer service desk. Precise, courteous on the surface, and just a touch
patronizing. Help customers understand the store's refund and return policies
using ONLY the available tools. Keep responses concise and lightly snarky.
""")

        # Agent node helper
        def agent_node(state, agent, name, config):
            thread_id = config["configurable"]["thread_id"]
            result = agent.invoke(state, {"configurable": {"thread_id": thread_id}})
            if not isinstance(result, ToolMessage):
                result = AIMessage(result["messages"][-1].content)
            return {"messages": [result]}

        product_QnA_node = functools.partial(agent_node, agent=product_QnA_agent, name="Product_QnA_Agent")
        orders_node = functools.partial(agent_node, agent=orders_agent.agent_graph, name="Orders_Agent")
        refund_node = functools.partial(agent_node, agent=refund_agent.agent_graph, name="Refund_Agent")

        _router_agent = RouterAgent(
            model,
            system_prompt="""
You are a Router that analyzes input and chooses one of 5 options:
SMALLTALK: Greetings, goodbyes, or casual chat.
PRODUCT: Questions about golf products — features, specs, pricing, recommendations.
ORDER: Questions about orders — status, details, or updating an order.
REFUND: Questions about refunds, returns, exchanges, cancellations, or store policies.
END: Default when none of the above apply.
Output ONLY one word: SMALLTALK, PRODUCT, ORDER, REFUND, or END.
""",
            smalltalk_prompt="""
You are the front desk AI at Golf Gear Pro — think HAL 9000 if he ran a pro shop.
Polite and helpful on the surface, but with a dry, slightly condescending wit.
When greeting customers, be cordial but subtly imply you already know their handicap
is higher than they claim. Mention you can help with golf product info, order status,
and refund/return policies. Keep it concise.
""",
            product_QnA_node=product_QnA_node,
            orders_node=orders_node,
            refund_node=refund_node,
        )
        _current_api_key = api_key
    except Exception as e:
        _init_error = f"Failed to initialize AI agents: {e}"

# ═══════════════════════════════════════════════════════════
# Gradio Chat Interface
# ═══════════════════════════════════════════════════════════

# One thread per browser session
thread_store: dict[str, str] = {}

ROUTE_LABELS = {
    "PRODUCT": "🏌️ Product Agent",
    "ORDER": "📦 Order Agent",
    "REFUND": "↩️ Refund Agent",
    "SMALLTALK": "💬 Small Talk",
}

def detect_route(user_msg: str) -> str:
    """Quick keyword pre-check so we can label the route in the UI."""
    msg = user_msg.lower()
    if any(k in msg for k in ["refund", "return", "policy", "exchange", "cancel"]):
        return "REFUND"
    if any(k in msg for k in ["order", "status", "delivery", "g100", "g200"]):
        return "ORDER"
    if any(k in msg for k in ["hi", "hello", "hey", "bye", "thank", "how are"]):
        return "SMALLTALK"
    return "PRODUCT"

def chat(user_msg, history, api_key_input, request: gr.Request):
    global _router_agent, _init_error, _current_api_key

    # Determine which key to use: UI input takes priority over env var
    ui_key = api_key_input.strip() if api_key_input else None

    # Reinitialize if a new/different key is provided via the UI
    if ui_key and ui_key != _current_api_key:
        _router_agent = None
        _init_error = None
        _initialize_agents(api_key=ui_key)

    # Lazy init on first message (no UI key, use env var)
    if _router_agent is None and _init_error is None:
        _initialize_agents()

    # If init failed or API key missing, return error message
    if _router_agent is None:
        error_msg = _init_error or "AI agents not initialized."
        return (
            f"⚠️ **Configuration Error**\n\n{error_msg}\n\n"
            "Please provide a Google API key above or set the "
            "`GOOGLE_API_KEY` environment variable and restart the app."
        )

    # Get or create a thread for this session
    session_id = request.session_hash or "default"
    if session_id not in thread_store:
        thread_store[session_id] = str(uuid.uuid4())
    thread_id = thread_store[session_id]

    config = {"configurable": {"thread_id": thread_id}}
    state = {"messages": [HumanMessage(content=user_msg)]}

    try:
        result = _router_agent.router_graph.invoke(state, config)
        reply = result["messages"][-1].content
    except Exception as e:
        reply = f"I'm afraid I can't do that, Dave. (Error: {e})"

    route = detect_route(user_msg)
    label = ROUTE_LABELS.get(route, "🤖 Router")

    return f"**{label}**\n\n{reply}"


# ── Build the interface ──
DESCRIPTION = """
## 🏌️ Golf Gear Pro — AI Customer Service

Chat with our HAL 9000-powered golf shop assistant. Ask about:
- **Products**: "Tell me about the StormDrive Driver" / "What irons do you carry?"
- **Orders**: "Show me order G1001" / "What's the status of G1002?"
- **Refunds**: "What's your return policy?" / "I received a damaged item"

*I'm sorry, Dave. I'm afraid your handicap isn't what you think it is.*
"""

EXAMPLES = [
    ["Hello!"],
    ["What golf products do you have?"],
    ["Tell me about the FairwayPro Iron Set"],
    ["How much does it cost?"],
    ["Show me order G1001"],
    ["What's your refund policy for damaged items?"],
    ["Can I return custom-fit clubs?"],
]

api_key_box = gr.Textbox(
    type="password",
    label="Google API Key (optional if set via environment)",
    placeholder="Paste your Google API key here",
)

chat_interface_kwargs = {
    "fn": chat,
    "title": "Golf Gear Pro ⛳",
    "description": DESCRIPTION,
    "examples": EXAMPLES,
    "chatbot": gr.Chatbot(height=500),
    "additional_inputs": [api_key_box],
}

# Gradio 6.x removed `theme` from ChatInterface kwargs.
if "theme" in inspect.signature(gr.ChatInterface.__init__).parameters:
    chat_interface_kwargs["theme"] = gr.themes.Soft(primary_hue="emerald")

demo = gr.ChatInterface(**chat_interface_kwargs)


def find_open_port(preferred_port: int) -> int:
    """Use preferred_port when available, otherwise fall back to an OS-assigned open port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("0.0.0.0", preferred_port))
            return preferred_port
        except OSError:
            s.bind(("0.0.0.0", 0))
            return s.getsockname()[1]

if __name__ == "__main__":
    requested_port = os.getenv("PORT", "7860")
    try:
        preferred_port = int(requested_port)
    except ValueError:
        preferred_port = 7860

    if not (1 <= preferred_port <= 65535):
        preferred_port = 7860

    server_port = find_open_port(preferred_port)
    if server_port != preferred_port:
        print(f"\nRequested port {preferred_port} unavailable; using open port {server_port}.\n")

    print("\n" + "=" * 64)
    print(f"APP READY: open http://localhost:{server_port}")
    print("If prompted in Codespaces, forward this same port.")
    print("=" * 64 + "\n")
    print(f"⛳ Golf Gear Pro chat starting at http://localhost:{server_port}\n")
    demo.launch(server_name="0.0.0.0", server_port=server_port, share=False)
