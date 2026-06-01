import html
import os
from typing import Dict, List

import streamlit as st
from dotenv import load_dotenv

from src.agent.agent import ReActAgent
from src.tools.cafe_tools import COUPONS, DELIVERY_FEES, MENU_CATEGORIES, get_cafe_tools


EXAMPLE_PROMPTS = [
    "Toi muon mua 2 Phin Sua Da size nho va 1 Tra Thanh Dao size nho, dung ma GIAM10, giao toi Quan 1. Tong tien bao nhieu?",
    "Toi muon mua 1 Freeze Tra Xanh size lon va 1 Banh Chuoi, giao toi Quan 3.",
    "Toi muon mua 1 Tra Sen Vang size vua, dung ma FREESHIP, giao toi Quan 7.",
    "Toi muon mua 1 Banh Mi Que Pate va 1 Phin Den Da size lon, dung ma ABC, giao toi Quan 1.",
    "Toi muon mua 1 Combo Chuyen Tro size lon giao toi Quan 12.",
]


def build_provider():
    provider = os.getenv("DEFAULT_PROVIDER", "openai").lower()
    model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

    if provider == "openai":
        from src.core.openai_provider import OpenAIProvider

        return OpenAIProvider(
            model_name=model,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    if provider in {"google", "gemini"}:
        from src.core.gemini_provider import GeminiProvider

        return GeminiProvider(
            model_name=model or "gemini-1.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
        )

    if provider == "local":
        from src.core.local_provider import LocalProvider

        return LocalProvider(
            model_path=os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf"),
        )

    raise ValueError(f"Unsupported DEFAULT_PROVIDER: {provider}")


def create_agent() -> ReActAgent:
    return ReActAgent(
        llm=build_provider(),
        tools=get_cafe_tools(),
        max_steps=8,
    )


def format_price(value: int) -> str:
    return str(int(value / 1000))


def format_money(value) -> str:
    if value is None:
        return "N/A"
    return f"{int(value):,} VND"


def css():
    st.markdown(
        """
<style>
div[data-testid="stAppViewContainer"] {
    background: #f8f2e8 !important;
    color: #3f2c24 !important;
}
section[data-testid="stSidebar"] {
    background: #3f2c24 !important;
    border-right: 1px solid #ead9c6;
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
    color: #fff7ec !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    background: transparent !important;
}
.block-container {
    max-width: 1280px;
    padding-top: 1.4rem;
}
div[data-testid="stAppViewContainer"] h1,
div[data-testid="stAppViewContainer"] h2,
div[data-testid="stAppViewContainer"] h3,
div[data-testid="stAppViewContainer"] h4,
div[data-testid="stAppViewContainer"] p,
div[data-testid="stAppViewContainer"] label,
div[data-testid="stAppViewContainer"] span,
div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"],
div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] * {
    color: #3f2c24 !important;
}
div[data-testid="stAlert"] {
    background: #fff7ec !important;
    border: 1px solid #ead9c6 !important;
    color: #3f2c24 !important;
}
div[data-testid="stAlert"] *,
div[data-testid="stAlert"] p {
    color: #3f2c24 !important;
}
div[data-testid="stMetric"] {
    background: #fff7ec !important;
    border: 1px solid #ead9c6 !important;
    padding: 14px 16px;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div {
    color: #3f2c24 !important;
}
div[data-baseweb="select"] > div {
    background: #fffdf8 !important;
    border-color: #b99577 !important;
    color: #3f2c24 !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] svg {
    color: #3f2c24 !important;
    fill: #3f2c24 !important;
}
textarea {
    background: #fffdf8 !important;
    border: 1px solid #b99577 !important;
    color: #3f2c24 !important;
}
textarea::placeholder {
    color: #8a6b58 !important;
}
div[data-testid="stChatMessage"] {
    background: #fff7ec !important;
    border: 1px solid #ead9c6 !important;
}
div[data-testid="stChatMessage"] *,
div[data-testid="stChatMessage"] p {
    color: #3f2c24 !important;
}
div[data-testid="stExpander"] {
    background: #fff7ec !important;
    border: 1px solid #ead9c6 !important;
}
div[data-testid="stExpander"] details,
div[data-testid="stExpander"] summary {
    background: #fff7ec !important;
    color: #3f2c24 !important;
}
div[data-testid="stExpander"] *,
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] svg {
    color: #3f2c24 !important;
    fill: #3f2c24 !important;
}
pre,
code,
div[data-testid="stCodeBlock"],
div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code {
    background: #241f20 !important;
    color: #fff7ec !important;
}
div[data-testid="stCodeBlock"] span {
    color: #fff7ec !important;
}
button[kind="primary"] {
    background: #c42b32 !important;
    border-color: #c42b32 !important;
    color: #ffffff !important;
}
button[kind="secondary"] {
    background: #3f2c24 !important;
    border-color: #3f2c24 !important;
    color: #ffffff !important;
}
button * {
    color: inherit !important;
}
.menu-board {
    background:
        radial-gradient(circle at 16% 6%, rgba(255,255,255,0.95), rgba(255,255,255,0) 28%),
        linear-gradient(90deg, #efe2cf 0%, #fffaf1 18%, #ffffff 52%, #f7ead8 100%);
    border: 1px solid #e7d7c4;
    box-shadow: 0 18px 42px rgba(74, 47, 34, 0.12);
    padding: 34px 38px 28px;
}
.menu-title {
    color: #4c352a;
    font-size: 46px;
    line-height: 1;
    font-weight: 900;
    letter-spacing: 0;
    text-transform: uppercase;
}
.menu-subtitle {
    color: #6b4b3b;
    font-size: 18px;
    font-weight: 800;
    text-transform: uppercase;
    margin-top: 2px;
}
.menu-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 34px 58px;
}
.menu-section {
    margin-bottom: 28px;
}
.menu-header {
    display: grid;
    grid-template-columns: minmax(220px, 1fr) repeat(3, 58px);
    align-items: end;
    column-gap: 12px;
    margin: 10px 0 8px;
}
.size-head {
    color: #5a3c30;
    font-size: 18px;
    line-height: 1.1;
    font-weight: 900;
    text-align: center;
}
.size-head span {
    display: block;
    color: #795c4c;
    font-size: 15px;
    font-weight: 700;
    margin-top: 3px;
}
.menu-row {
    display: grid;
    grid-template-columns: minmax(220px, 1fr) repeat(3, 58px);
    align-items: baseline;
    column-gap: 12px;
    margin: 9px 0;
}
.single-price-row {
    display: grid;
    grid-template-columns: minmax(220px, 1fr) 60px;
    align-items: baseline;
    column-gap: 14px;
    margin: 9px 0;
}
.item-name {
    color: #4b342b;
    font-size: 23px;
    line-height: 1.05;
    font-weight: 900;
}
.item-en {
    color: #6f5b4e;
    font-size: 14px;
    line-height: 1.15;
    font-style: italic;
    font-weight: 650;
    margin-top: 2px;
}
.price {
    color: #c42b32;
    font-size: 28px;
    line-height: 1;
    font-weight: 950;
    text-align: center;
}
.single-price {
    color: #c42b32;
    font-size: 28px;
    line-height: 1;
    font-weight: 950;
    text-align: right;
}
.menu-note {
    color: #5a3c30;
    font-size: 15px;
    font-weight: 800;
    margin-top: 8px;
}
.combo-band {
    border-top: 2px solid #e2cfba;
    margin-top: 18px;
    padding-top: 18px;
}
.unit-note {
    color: #4c352a;
    font-size: 20px;
    font-weight: 900;
    text-align: right;
    margin-top: 20px;
}
.control-panel {
    margin-top: 24px;
    padding: 22px 24px;
    background: #fffaf3;
    border: 1px solid #ead9c6;
}
.trace-box code {
    white-space: pre-wrap;
}
/* Final overrides for Streamlit theme collisions. Keep these near the end. */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
div[data-testid="stSidebar"],
div[data-testid="stSidebarContent"] {
    background: #fff7ec !important;
    color: #3f2c24 !important;
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] *,
div[data-testid="stSidebar"] *,
div[data-testid="stSidebarContent"] * {
    color: #3f2c24 !important;
    fill: #3f2c24 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-weight: 900 !important;
}
div[data-testid="stExpander"],
div[data-testid="stExpander"] details,
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] div,
div[data-testid="stExpander"] div[role="button"] {
    background: #fff7ec !important;
    color: #3f2c24 !important;
    border-color: #ead9c6 !important;
}
div[data-testid="stExpander"] *,
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] label,
div[data-testid="stExpander"] svg,
div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"],
div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] * {
    color: #3f2c24 !important;
    fill: #3f2c24 !important;
}
div[data-testid="stExpander"] pre,
div[data-testid="stExpander"] code,
div[data-testid="stExpander"] pre *,
div[data-testid="stExpander"] code *,
div[data-testid="stCodeBlock"],
div[data-testid="stCodeBlock"] *,
div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code {
    background: #241f20 !important;
    color: #fff7ec !important;
    fill: #fff7ec !important;
}
@media (max-width: 900px) {
    .menu-board {
        padding: 24px 20px;
    }
    .menu-grid {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    .menu-title {
        font-size: 34px;
    }
    .menu-header,
    .menu-row {
        grid-template-columns: minmax(160px, 1fr) repeat(3, 44px);
        column-gap: 8px;
    }
    .item-name {
        font-size: 19px;
    }
    .price,
    .single-price {
        font-size: 23px;
    }
}
</style>
""",
        unsafe_allow_html=True,
    )


def section_html(category: Dict) -> str:
    sizes = category["sizes"]
    html_parts = [
        '<section class="menu-section">',
        f'<div class="menu-title">{html.escape(category["name"])}</div>',
    ]
    if category["subtitle"]:
        html_parts.append(f'<div class="menu-subtitle">{html.escape(category["subtitle"])}</div>')

    if sizes:
        html_parts.append('<div class="menu-header"><div></div>')
        for size, ounce in zip(sizes, ["12oz", "16oz", "20oz"]):
            if category["name"] in {"CA PHE PHIN", "PHINDI"}:
                ounce = {"Nho": "10oz", "Vua": "12oz", "Lon": "16oz"}[size]
            html_parts.append(f'<div class="size-head">{html.escape(size)}<span>{ounce}</span></div>')
        html_parts.append("</div>")

        for item in category["items"]:
            html_parts.append('<div class="menu-row">')
            html_parts.append(
                '<div>'
                f'<div class="item-name">{html.escape(item["name"])}</div>'
                f'<div class="item-en">{html.escape(item["english"])}</div>'
                '</div>'
            )
            for key in ["nho", "vua", "lon"]:
                html_parts.append(f'<div class="price">{format_price(item["prices"][key])}</div>')
            html_parts.append("</div>")
    else:
        for item in category["items"]:
            html_parts.append('<div class="single-price-row">')
            html_parts.append(
                '<div>'
                f'<div class="item-name">{html.escape(item["name"])}</div>'
                f'<div class="item-en">{html.escape(item["english"])}</div>'
                '</div>'
            )
            html_parts.append(f'<div class="single-price">{format_price(item["prices"]["one_size"])}</div>')
            html_parts.append("</div>")

    if category["name"] in {"CA PHE PHIN", "TRA"}:
        html_parts.append('<div class="menu-note">Ban co the lua chon nong hoac da / You can choose hot or ice</div>')

    html_parts.append("</section>")
    return "".join(html_parts)


def render_menu_board():
    left_names = {"CA PHE PHIN", "PHINDI", "BANH", "BANH MI QUE"}
    right_names = {"TRA", "FREEZE", "COMBO"}

    left_sections = [category for category in MENU_CATEGORIES if category["name"] in left_names]
    right_sections = [category for category in MENU_CATEGORIES if category["name"] in right_names]

    left_html = "".join(section_html(category) for category in left_sections)
    right_html = "".join(section_html(category) for category in right_sections)

    st.markdown(
        f"""
<div class="menu-board">
    <div class="menu-grid">
        <div>{left_html}</div>
        <div>{right_html}</div>
    </div>
    <div class="unit-note">Don vi tinh / Unit: 1.000 VND</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.title("Smart Cafe Agent")
    st.sidebar.write("The agent uses this menu as tool data.")

    st.sidebar.subheader("Coupons")
    for code, coupon in COUPONS.items():
        if coupon["type"] == "percent":
            st.sidebar.write(f"{code}: {int(coupon['value'] * 100)}% off subtotal")
        else:
            st.sidebar.write(f"{code}: free shipping")

    st.sidebar.subheader("Delivery")
    for district, fee in DELIVERY_FEES.items():
        st.sidebar.write(f"{district}: {format_money(fee)}")


def render_trace(history: List[Dict]):
    if not history:
        st.info("Run a prompt to see the ReAct trace.")
        return

    for event in history:
        with st.expander(f"Step {event['step']}", expanded=False):
            st.code(event["llm_output"], language="text")


def main():
    load_dotenv()
    st.set_page_config(page_title="Smart Cafe ReAct Agent", layout="wide")
    css()
    render_sidebar()

    render_menu_board()

    provider = os.getenv("DEFAULT_PROVIDER", "openai")
    model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.subheader("Order with ReAct Agent")
    metric_cols = st.columns(3)
    metric_cols[0].metric("Provider", provider)
    metric_cols[1].metric("Model", model)
    metric_cols[2].metric("Max Steps", "8")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_trace" not in st.session_state:
        st.session_state.last_trace = []

    with st.form("prompt_form"):
        selected_example = st.selectbox("Example prompts", EXAMPLE_PROMPTS)
        prompt = st.text_area("Your prompt", value=selected_example, height=105)
        submitted = st.form_submit_button("Run Agent", type="primary")

    if submitted and prompt.strip():
        with st.spinner("Agent is checking the menu and calling tools..."):
            agent = create_agent()
            answer = agent.run(prompt.strip())
            st.session_state.last_trace = agent.history
            st.session_state.messages.append({"role": "user", "content": prompt.strip()})
            st.session_state.messages.append({"role": "assistant", "content": answer})

    left, right = st.columns([1.05, 0.95])

    with left:
        st.subheader("Conversation")
        if not st.session_state.messages:
            st.info("Choose an example or write your own cafe order, then run the agent.")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    with right:
        st.subheader("ReAct Trace")
        render_trace(st.session_state.last_trace)

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.last_trace = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
