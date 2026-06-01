# Lab 3: Chatbot vs ReAct Agent (Industry Edition)

Welcome to Phase 3 of the Agentic AI course! This lab focuses on moving from a simple LLM Chatbot to a sophisticated **ReAct Agent** with industry-standard monitoring.

## 🚀 Getting Started

### 1. Setup Environment
Copy the `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Directory Structure
- `src/tools/`: Extension point for your custom tools.

## Smart Cafe Order Agent Demo

This repo now includes a simple ReAct scenario for a cafe ordering assistant.
The agent can check menu stock, apply coupons, calculate delivery fees, and
return the final payable total.

Use OpenAI by setting `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-4o-mini
```

Run the demo:
```bash
python3 run_cafe_agent.py
```

Then type your own prompt in the terminal. Type `exit` or `quit` to stop.
If you press Enter without typing a prompt, the script will use the default
demo prompt below.

Example prompt:
```text
Toi muon mua 2 Phin Sua Da size nho va 1 Tra Thanh Dao size nho, dung ma GIAM10, giao toi Quan 1. Tong tien bao nhieu?
```

Expected result:
```text
Subtotal = 103000 VND
Discount = 10300 VND
Delivery = 15000 VND
Total = 107700 VND
```

Run the Streamlit demo:
```bash
python3 -m streamlit run streamlit_app.py
```

The Streamlit app shows a menu-board layout, prompt examples, conversation
output, and the ReAct trace for each tool-calling step.

## 🏠 Running with Local Models (CPU)

If you don't want to use OpenAI or Gemini, you can run open-source models (like Phi-3) directly on your CPU using `llama-cpp-python`.

### 1. Download the Model
Download the **Phi-3-mini-4k-instruct-q4.gguf** (approx 2.2GB) from Hugging Face:
- [Phi-3-mini-4k-instruct-GGUF](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf)
- Direct Download: [phi-3-mini-4k-instruct-q4.gguf](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf)

### 2. Place Model in Project
Create a `models/` folder in the root and move the downloaded `.gguf` file there.

### 3. Update `.env`
Change your `DEFAULT_PROVIDER` and set the path:
```env
DEFAULT_PROVIDER=local
LOCAL_MODEL_PATH=./models/Phi-3-mini-4k-instruct-q4.gguf
```

## 🎯 Lab Objectives

1.  **Baseline Chatbot**: Observe the limitations of a standard LLM when faced with multi-step reasoning.
2.  **ReAct Loop**: Implement the `Thought-Action-Observation` cycle in `src/agent/agent.py`.
3.  **Provider Switching**: Swap between OpenAI and Gemini seamlessly using the `LLMProvider` interface.
4.  **Failure Analysis**: Use the structured logs in `logs/` to identify why the agent fails (hallucinations, parsing errors).
5.  **Grading & Bonus**: Follow the [SCORING.md](file:///Users/tindt/personal/ai-thuc-chien/day03-lab-agent/SCORING.md) to maximize your points and explore bonus metrics.

## 🛠️ How to Use This Baseline
The code is designed as a **Production Prototype**. It includes:
- **Telemetry**: Every action is logged in JSON format for later analysis.
- **Robust Provider Pattern**: Easily extendable to any LLM API.
- **Clean Skeletons**: Focus on the logic that matters—the agent's reasoning process.

---

*Happy Coding! Let's build agents that actually work.*
