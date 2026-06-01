# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyen Dinh Minh Chi
- **Student ID**: 2A202600820
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

### Modules Implemented

My main contribution was building and improving the **Smart Cafe ReAct Agent** demo.

- `src/tools/cafe_tools.py`
  - Built the cafe menu tool data based on the visual menu board.
  - Added menu categories: `CA PHE PHIN`, `PHINDI`, `TRA`, `FREEZE`, `BANH`, `BANH MI QUE`, and `COMBO`.
  - Implemented `get_menu_item(item_name, size)` with Vietnamese normalization and size support.
  - Implemented category ambiguity handling for inputs like `banh mi`, `banh mi que`, and `breadstick`.
  - Implemented coupon, delivery fee, and total calculation tools.

- `src/agent/agent.py`
  - Improved the ReAct system prompt.
  - Added a rule for `ambiguous=true` observations so the agent asks the user to choose a specific item.
  - Integrated the ReAct loop with telemetry events and structured tool observations.

- `streamlit_app.py`
  - Built a Streamlit demo UI with a menu-board layout.
  - Added prompt examples, conversation display, and ReAct trace display.
  - Improved CSS to make the app readable under Streamlit theme conflicts.

- `tests/test_cafe_agent.py`
  - Added automated tests for the happy path order flow.
  - Added tests for unknown menu items.
  - Added tests for ambiguous category handling.
  - Verified the ReAct loop using a `FakeLLMProvider`.

### Code Highlights

The most important tool behavior is the category-aware lookup in `src/tools/cafe_tools.py`.

```python
CATEGORY_ALIASES = {
    "banh mi": "BANH MI QUE",
    "banh mi que": "BANH MI QUE",
    "breadstick": "BANH MI QUE",
    "breadsticks": "BANH MI QUE",
}
```

When a user asks for a category instead of a specific item, the tool returns:

```json
{
  "found": true,
  "ambiguous": true,
  "category": "BANH MI QUE",
  "message": "This is a menu category. Ask the user to choose one specific item."
}
```

This allows the agent to respond with options instead of incorrectly saying that the menu item does not exist.

### Documentation

The cafe tools interact with the ReAct loop through the tool inventory passed into `ReActAgent`. The LLM chooses a tool by producing an `Action` JSON object. The agent parses the JSON, executes the matching Python function, then feeds the tool result back as an `Observation`. This loop repeats until the LLM returns a `Final Answer`.

---

## II. Debugging Case Study (10 Points)

### Problem Description

The agent incorrectly answered that `bánh mì que` was not in the menu, even though the Streamlit menu clearly showed a `BANH MI QUE` section.

Example user input:

```text
Cho tôi 1 bánh mì que
```

The agent replied:

```text
Rất tiếc, món "bánh mì que" không có trong thực đơn của chúng tôi.
```

### Log Source

From `logs/2026-06-01.log`:

```json
{
  "event": "TOOL_CALL",
  "data": {
    "tool": "get_menu_item",
    "args": {"item_name": "bánh mì que"},
    "observation": {
      "found": false,
      "item_name": "bánh mì que",
      "message": "Item is not on the cafe menu."
    }
  }
}
```

### Diagnosis

The failure was caused by the tool specification and lookup logic, not by the LLM alone.

The menu had specific items under the `BANH MI QUE` category:

- `Pate`
- `Ga Pho Mai`
- `Bo Sot Pho Mai`

However, the tool only supported exact item lookup. Therefore, generic category inputs like `bánh mì`, `bánh mì que`, or `breadstick` were treated as missing items.

### Solution

I added category aliases in `src/tools/cafe_tools.py`:

```python
CATEGORY_ALIASES = {
    "banh mi": "BANH MI QUE",
    "banh mi que": "BANH MI QUE",
    "breadstick": "BANH MI QUE",
    "breadsticks": "BANH MI QUE",
}
```

Then I updated `get_menu_item()` so category inputs return `ambiguous=true` with a list of options.

Improved observation:

```json
{
  "found": true,
  "ambiguous": true,
  "category": "BANH MI QUE",
  "options": [
    {"item_name": "Pate", "prices": {"one_size": 19000}},
    {"item_name": "Ga Pho Mai", "prices": {"one_size": 19000}},
    {"item_name": "Bo Sot Pho Mai", "prices": {"one_size": 25000}}
  ]
}
```

I also added this rule to the agent system prompt:

```text
If a tool observation has ambiguous=true, show the available options and ask the user to choose a specific item.
```

After the fix, the agent correctly asks the user to choose between `Pate`, `Ga Pho Mai`, and `Bo Sot Pho Mai`.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

### 1. Reasoning

The `Thought` block helps the agent break the order into smaller steps. For example, instead of immediately guessing the total price, the agent can first check the item price, then check delivery fee, then apply coupon, then calculate the final total.

This is more reliable than a normal chatbot because the answer is grounded in tool observations.

### 2. Reliability

The ReAct agent is stronger in multi-step tasks, but it can perform worse than a chatbot when:

- The prompt is vague and needs clarification.
- The tool schema is incomplete.
- The LLM outputs plain text instead of the required `Action` or `Final Answer` format.
- The agent loops through multiple tool calls for a simple question.

In the `bánh mì que` case, the agent failed because the tool design did not represent categories well enough. This showed that agent reliability depends heavily on the quality of tool descriptions and tool data.

### 3. Observation

Observations are the most important difference between a chatbot and an agent. The chatbot only has internal model knowledge, while the ReAct agent receives external feedback from tools.

For example:

- `get_menu_item` confirms the exact price and stock.
- `apply_coupon` confirms whether a coupon is valid.
- `calc_delivery_fee` confirms supported delivery districts.
- `calculate_total` prevents arithmetic mistakes.

The observation step gives the LLM a factual state to reason from in the next step.

---

## IV. Future Improvements (5 Points)

### Scalability

The hard-coded Python menu should be moved to a database, Google Sheet, CMS, or JSON API. This would allow staff to update menu items, prices, stock, and coupons without changing code.

### Safety

The agent should include stricter validation before confirming orders:

- Ask for confirmation before final checkout.
- Validate quantity is a positive integer.
- Reject unsupported delivery addresses.
- Prevent arbitrary tool names or unexpected arguments.

### Performance

The current ReAct loop may call the LLM multiple times for one order. In production, performance could be improved by:

- Combining deterministic calculations into fewer tool calls.
- Adding a dedicated `create_order_summary` tool.
- Caching menu lookup results.
- Using a cheaper model for simple menu routing.

### Production-Level Extension

A production version could use LangGraph or another state-machine framework to separate the flow into clear states:

```text
Collect Order -> Validate Items -> Apply Coupon -> Delivery -> Confirm Order -> Checkout
```

This would make the system easier to debug and safer for real customers.

---

## Final Reflection

This lab showed me that an agent is not just a chatbot with a longer prompt. A useful agent needs good tools, clear action formats, observability, and failure analysis. The strongest learning point was that logs reveal the real reason for failure: sometimes the model is not the problem; the tool design is.
