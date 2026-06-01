import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.agent import ReActAgent
from src.core.llm_provider import LLMProvider
from src.tools.cafe_tools import (
    apply_coupon,
    calc_delivery_fee,
    calculate_total,
    get_cafe_tools,
    get_menu_item,
)


class FakeLLMProvider(LLMProvider):
    def __init__(self, responses):
        super().__init__(model_name="fake-react-model")
        self.responses = list(responses)

    def generate(self, prompt, system_prompt=None):
        content = self.responses.pop(0)
        return {
            "content": content,
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            "latency_ms": 1,
            "provider": "fake",
        }

    def stream(self, prompt, system_prompt=None):
        yield self.generate(prompt, system_prompt)["content"]


def test_cafe_tools_happy_path():
    coffee = get_menu_item("ca phe sua")
    tea = get_menu_item("tra dao")
    delivery = calc_delivery_fee("Quan 1")
    coupon = apply_coupon("GIAM10", subtotal=105000, delivery_fee=delivery["fee"])
    total = calculate_total(
        subtotal=(2 * coffee["price"]) + tea["price"],
        discount_amount=coupon["discount_amount"],
        delivery_fee=delivery["fee"],
    )

    assert coffee["available"] is True
    assert tea["price"] == 45000
    assert delivery["fee"] == 15000
    assert coupon["discount_amount"] == 10500
    assert total["total"] == 109500


def test_cafe_tool_out_of_stock():
    item = get_menu_item("matcha latte")

    assert item["found"] is True
    assert item["available"] is False
    assert item["stock"] == 0


def test_react_agent_calls_tools_and_returns_final_answer():
    fake_llm = FakeLLMProvider(
        [
            'Thought: Need coffee price and stock.\nAction: {"tool": "get_menu_item", "args": {"item_name": "ca phe sua"}}',
            'Thought: Need tea price and stock.\nAction: {"tool": "get_menu_item", "args": {"item_name": "tra dao"}}',
            'Thought: Need delivery fee.\nAction: {"tool": "calc_delivery_fee", "args": {"district": "Quan 1"}}',
            'Thought: Apply coupon to subtotal.\nAction: {"tool": "apply_coupon", "args": {"coupon_code": "GIAM10", "subtotal": 105000, "delivery_fee": 15000}}',
            'Thought: Calculate the final total.\nAction: {"tool": "calculate_total", "args": {"subtotal": 105000, "discount_amount": 10500, "delivery_fee": 15000}}',
            "Thought: I have the final total.\nFinal Answer: Tong tien la 109500 VND.",
        ]
    )
    agent = ReActAgent(llm=fake_llm, tools=get_cafe_tools(), max_steps=8)

    answer = agent.run("Toi muon mua 2 ca phe sua va 1 tra dao, dung ma GIAM10, giao Quan 1.")

    assert "109500" in answer
    assert len(agent.history) == 6
