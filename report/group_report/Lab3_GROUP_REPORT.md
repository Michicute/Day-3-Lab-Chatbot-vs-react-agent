# Group Report: Lab 3 - Smart Cafe ReAct Agent

- **Team Name**: Smart Cafe Agent Team
- **Team Members**: 

   Nguyen Dinh Minh Chi - 2A202600820

   Le Van Khiem - 2A202600542
- **Deployment Date**: 2026-06-01

---

## 1. Executive Summary

Our project implements a **Smart Cafe Order Agent** that helps users order drinks, pastries, breadsticks, and combos from a Highland-style cafe menu. The goal is to compare a normal chatbot response with a ReAct agent that can use structured tools to verify menu items, prices, stock, coupons, delivery fees, and final totals.

- **Success Rate**: 5/5 automated tests passed. Manual Streamlit demo cases also worked for multi-step order calculation, invalid coupon handling, unsupported delivery districts, and ambiguous item names.
- **Key Outcome**: The ReAct agent produced more reliable answers than a plain chatbot for menu-ordering tasks because it did not need to invent prices. It used tools such as `get_menu_item`, `apply_coupon`, `calc_delivery_fee`, and `calculate_total` before giving the final answer.
- **Demo UI**: A Streamlit app was added to show the menu board, prompt examples, conversation output, and ReAct trace.

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation

The core loop is implemented in `src/agent/agent.py`.

```text
User Prompt
   |
   v
System Prompt + Tool Descriptions
   |
   v
LLM generates Thought + Action JSON
   |
   v
Agent parses Action
   |
   v
Tool execution
   |
   v
Observation appended to prompt
   |
   v
Repeat until Final Answer or max_steps
```

The agent accepts this action format:

```json
{"tool": "tool_name", "args": {"arg_name": "value"}}
```

Important guardrails:

- `max_steps=8` prevents infinite loops.
- Tool calls are executed only if the tool name exists.
- Invalid action formats are logged as `parser_error`.
- Ambiguous category matches, such as `banh mi`, return `ambiguous=true` and ask the user to choose a specific item.

### 2.2 Tool Definitions (Inventory)

| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `get_menu_item` | JSON: `item_name`, optional `size` | Looks up menu item price, stock, category, and availability. Supports `nho`, `vua`, `lon`. |
| `apply_coupon` | JSON: `coupon_code`, `subtotal`, optional `delivery_fee` | Applies `GIAM10` or `FREESHIP`. |
| `calc_delivery_fee` | JSON: `district` | Calculates delivery fee for supported districts: `quan 1`, `quan 3`, `quan 7`. |
| `calculate_total` | JSON: `subtotal`, `discount_amount`, `delivery_fee`, `delivery_discount` | Computes final payable total. |

### 2.3 LLM Providers Used

- **Primary**: OpenAI `gpt-4o` / `gpt-4o-mini`, configured through `.env`.
- **Secondary**: Gemini provider exists in `src/core/gemini_provider.py`.
- **Local Backup**: Local GGUF model support exists in `src/core/local_provider.py`.
- **Testing Provider**: `FakeLLMProvider` is used in automated tests to verify the ReAct loop without spending API cost.

---

## 3. Telemetry & Performance Dashboard

Telemetry is logged as JSON in `logs/2026-06-01.log`.

Final manual demo examples from the log:

| Scenario | Steps | Total Tokens | Total Latency | Result |
| :--- | ---: | ---: | ---: | :--- |
| `Banh Mi Que Pate + Phin Den Da size lon + invalid coupon ABC + Quan 1` | 5 | 3,872 | 11.16s | Correct total: 73,000 VND; coupon rejected |
| `banh mi` ambiguous category | 2 | 1,122 | 2.70s | Correctly asked user to choose Pate / Ga Pho Mai / Bo Sot Pho Mai |
| `Combo Hung Khoi size lon + FREESHIP + Quan 1` | 5 | 3,458 | 5.31s | Correct total: 49,000 VND; shipping removed |

Aggregate observations:

- **Average LLM calls per successful multi-step order**: 4-5 calls.
- **Average tokens per full multi-step task**: around 3,400-3,900 tokens.
- **Observed P50 step latency**: around 0.9s-1.3s in successful runs.
- **Highest observed step latency**: 5.8s for one OpenAI step in the invalid-coupon order.
- **Estimated cost**: The lab uses a mock formula in `src/telemetry/metrics.py`: `(total_tokens / 1000) * 0.01`.

Automated validation:

```text
pytest -q
5 passed
```

---

## 4. Root Cause Analysis (RCA) - Failure Traces

### Case Study 1: Category Treated as Missing Item

- **Input**: `Cho tôi 1 bánh mì que`
- **Failed Observation Before Fix**:

```json
{
  "found": false,
  "item_name": "bánh mì que",
  "message": "Item is not on the cafe menu."
}
```

- **Root Cause**: The menu contained specific breadstick items (`Pate`, `Ga Pho Mai`, `Bo Sot Pho Mai`) but the tool only performed exact item lookup. Generic category inputs like `banh mi`, `banh mi que`, or `breadstick` were not mapped to the `BANH MI QUE` category.
- **Fix**: Added `CATEGORY_ALIASES` and `ambiguous=true` behavior in `src/tools/cafe_tools.py`.
- **Improved Observation After Fix**:

```json
{
  "found": true,
  "ambiguous": true,
  "category": "BANH MI QUE",
  "options": ["Pate", "Ga Pho Mai", "Bo Sot Pho Mai"]
}
```

- **Result**: The agent now asks the user to choose a specific breadstick instead of incorrectly saying the item does not exist.

### Case Study 2: Parser Error After Ambiguous Tool Result

- **Input**: `Toi muon mua 1 banh mi que`
- **Observation**: The tool returned valid options, but the LLM responded directly with a question without `Final Answer:`, causing a `parser_error`.
- **Root Cause**: The system prompt required either Action JSON or Final Answer, but the model sometimes produced plain text after receiving an ambiguous observation.
- **Fix**: Added a system prompt rule: if observation has `ambiguous=true`, show available options and ask the user to choose a specific item. Later runs show the model using `Final Answer` correctly for `banh mi`.

---

## 5. Ablation Studies & Experiments

### Experiment 1: Exact Lookup vs Category-Aware Lookup

| Version | Behavior |
| :--- | :--- |
| Tool v1 | `banh mi` and `banh mi que` returned `found=false`. |
| Tool v2 | Generic category names return `ambiguous=true` with available item options. |

**Result**: Category-aware lookup reduced false negative menu answers and improved the ordering flow.

### Experiment 2: Chatbot vs ReAct Agent

| Case | Chatbot Result | Agent Result | Winner |
| :--- | :--- | :--- | :--- |
| Simple recommendation | Can answer conversationally but may invent menu items | Can answer, but should use menu data for reliability | Draw |
| Multi-step order with coupon and delivery | Likely to miscalculate or invent fee | Uses tools to calculate subtotal, coupon, delivery, total | **Agent** |
| Invalid coupon | May assume coupon works | Correctly rejects invalid coupon `ABC` | **Agent** |
| Ambiguous `banh mi` request | May guess a product | Asks user to choose Pate / Ga Pho Mai / Bo Sot Pho Mai | **Agent** |

---

## 6. Production Readiness Review

- **Security**: Tool inputs are structured JSON and filtered against function signatures before execution.
- **Guardrails**: The ReAct loop has `max_steps=8` to prevent runaway API calls.
- **Observability**: Every LLM call and tool call is logged with JSON telemetry.
- **Reliability**: Ambiguous categories are handled explicitly instead of being treated as missing items.
- **Testing**: Automated tests cover happy path, unknown items, category ambiguity, and ReAct loop execution.
- **Scaling**: For a production system, the menu should move from hard-coded Python data to a database or CMS. The ReAct loop could also be migrated to LangGraph for stronger state management.
- **Future Improvements**:
  - Add `list_menu_category(category_name)` as a dedicated tool.
  - Add delivery time estimates.
  - Add order confirmation state.
  - Add multilingual aliases for English and Vietnamese menu names.
  - Replace mock cost calculation with real OpenAI/Gemini pricing.

---

## 7. Submission Checklist

- ReAct agent loop implemented.
- Cafe tools implemented.
- Streamlit demo implemented.
- Telemetry logs generated.
- Failure trace documented.
- Automated tests pass.
- Group report completed.
