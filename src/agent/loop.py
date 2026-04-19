from src.engine.ollama_client import OllamaEngine
from src.schemas.models import ThinkStep, ToolCall, FinalAnswer
from src.tools.registry import run_tool
from src.agent.prompt_builder import (
    build_think_prompt, 
    build_tool_prompt, 
    build_answer_prompt
)
from src.utils.logger import logger
from src.utils.exceptions import EngineError, ToolError

def run_agent(task: str, max_steps: int = 6):
    """
    Runs the ReAct reasoning loop for a given task.
    """
    logger.info(f"Starting agent with task: {task}")
    engine = OllamaEngine(model_name="qwen3.5:0.8b")
    history = []

    try:
        for step in range(max_steps):
            logger.info(f"Step {step + 1}/{max_steps}")

            # 1. THINKING PHASE
            think_prompt = build_think_prompt(task, history)
            think = engine.generate_structured(think_prompt, ThinkStep)
            logger.info(f"Thought: {think.thought} || Needs Tool: {think.needs_tool}")

            history.append({
                "role": "thought", 
                "content": think.thought
            })

            # 2. DECISION PHASE
            if not think.needs_tool:
                # 2A. ANSWERING
                answer_prompt = build_answer_prompt(task, think.thought, history)
                result = engine.generate_structured(answer_prompt, FinalAnswer)
                logger.info(f"Final Answer: {result.answer}")
                return result.answer

            # 2B. TOOL CALLING
            tool_prompt = build_tool_prompt(task, think.thought)
            tool_call = engine.generate_structured(tool_prompt, ToolCall)
            logger.info(f"Using Tool: {tool_call.tool_name} with Input: {tool_call.tool_input}")

            try:
                observation = run_tool(tool_call.tool_name, tool_call.tool_input)
                logger.debug(f"Observation: {observation}")
            except ToolError as e:
                logger.warning(f"Tool Error: {e}")
                observation = f"Error: {e}"
            except Exception as e:
                logger.error(f"Unexpected Tool Crash: {e}")
                observation = f"Error: The tool crashed unexpectedly. {e}"

            history.append({
                "role": "tool_call",
                "tool": tool_call.tool_name,
                "input": tool_call.tool_input
            })
            history.append({
                "role": "observation",
                "content": observation
            })

        logger.warning("Max steps reached without a final answer.")
        return "Max steps reached."

    except EngineError as e:
        logger.error(f"LLM Engine Error: {e}")
        return f"I encountered an engine error: {e}"
    except Exception as e:
        logger.critical(f"Unexpected error in agent loop: {e}")
        return f"An unexpected error occurred: {e}"