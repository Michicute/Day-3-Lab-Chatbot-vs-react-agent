import inspect
import json
import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker

class ReActAgent:
    """
    SKELETON: A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Students should implement the core loop logic and tool execution.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        Build the system prompt that instructs the agent to follow ReAct.
        """
        tool_descriptions = "\n".join(
            [
                f"- {tool['name']}: {tool['description']}\n"
                f"  Args schema: {json.dumps(tool.get('args_schema', {}), ensure_ascii=False)}"
                for tool in self.tools
            ]
        )
        return f"""
You are a careful ReAct ordering assistant for a cafe.
You have access to these tools:
{tool_descriptions}

Rules:
- Use tools for menu prices, stock, coupons, delivery fees, and final totals.
- Do not invent prices, stock, discounts, or delivery fees.
- If an item is out of stock, unsupported, or a coupon is invalid, say so clearly.
- If a tool observation has ambiguous=true, show the available options and ask the user to choose a specific item.
- Use Vietnamese in the Final Answer if the user asks in Vietnamese.

Output exactly one of these formats each step:

Thought: short reasoning about the next needed step.
Action: {{"tool": "tool_name", "args": {{"arg_name": "value"}}}}

or:

Thought: short reasoning that you have enough information.
Final Answer: final response to the user.
"""

    def run(self, user_input: str) -> str:
        """
        Run the ReAct loop:
        1. Ask the LLM for Thought + Action.
        2. Execute the selected tool.
        3. Feed the Observation back into the next prompt.
        4. Stop when the LLM emits Final Answer or max_steps is reached.
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        
        transcript = [f"Question: {user_input}"]

        for step in range(1, self.max_steps + 1):
            current_prompt = "\n\n".join(transcript)
            result = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            content = result.get("content", "").strip()

            tracker.track_request(
                provider=result.get("provider", "unknown"),
                model=self.llm.model_name,
                usage=result.get("usage", {}),
                latency_ms=result.get("latency_ms", 0),
            )
            logger.log_event("AGENT_STEP", {"step": step, "llm_output": content})

            self.history.append({"step": step, "llm_output": content})

            final_answer = self._parse_final_answer(content)
            if final_answer:
                logger.log_event("AGENT_END", {"steps": step, "status": "final_answer"})
                return final_answer

            action = self._parse_action(content)
            if not action:
                observation = {
                    "error": "parser_error",
                    "message": "No valid Action JSON found. Use Action: {\"tool\": \"...\", \"args\": {...}}",
                }
                logger.log_event("AGENT_ERROR", {"step": step, **observation})
                transcript.append(content)
                transcript.append(f"Observation: {json.dumps(observation, ensure_ascii=False)}")
                continue

            observation = self._execute_tool(action["tool"], action.get("args", {}))
            logger.log_event(
                "TOOL_CALL",
                {"step": step, "tool": action["tool"], "args": action.get("args", {}), "observation": observation},
            )
            transcript.append(content)
            transcript.append(f"Observation: {json.dumps(observation, ensure_ascii=False)}")

        logger.log_event("AGENT_END", {"steps": self.max_steps, "status": "max_steps"})
        return "Xin lỗi, agent đã vượt quá số bước cho phép trước khi hoàn tất câu trả lời."

    def _parse_final_answer(self, text: str) -> Optional[str]:
        match = re.search(r"Final Answer\s*:\s*(.*)", text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _parse_action(self, text: str) -> Optional[Dict[str, Any]]:
        match = re.search(r"Action\s*:\s*(\{.*\})", text, flags=re.IGNORECASE | re.DOTALL)
        if not match:
            return None

        raw_json = match.group(1).strip()
        try:
            payload = json.loads(raw_json)
        except json.JSONDecodeError:
            return None

        tool_name = payload.get("tool")
        args = payload.get("args", {})
        if not isinstance(tool_name, str) or not isinstance(args, dict):
            return None
        return {"tool": tool_name, "args": args}

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name. Tools are dictionaries with a callable in "func".
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                func = tool.get("func")
                if not callable(func):
                    return {"error": "tool_not_callable", "tool": tool_name}

                try:
                    signature = inspect.signature(func)
                    filtered_args = {
                        key: value
                        for key, value in args.items()
                        if key in signature.parameters
                    }
                    return func(**filtered_args)
                except TypeError as exc:
                    return {"error": "invalid_tool_args", "tool": tool_name, "message": str(exc)}
                except Exception as exc:
                    logger.error(f"Tool execution failed: {tool_name}")
                    return {"error": "tool_execution_error", "tool": tool_name, "message": str(exc)}

        return {"error": "tool_not_found", "tool": tool_name}
