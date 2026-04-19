from src.tools.registry import get_tool_descriptions

def build_think_prompt(task: str, history: list) -> str:
    
    history_text = format_history(history)
    tools_text = get_tool_descriptions()

    return f"""You are Qurio, a reasoning agent.

            Task: {task}

            Tools available:
            {tools_text}

            What has happened so far:
            {history_text}

            Think about what to do next.
            Do you need to use a tool, or do you already have enough to answer?
            """


def build_tool_prompt(task: str, thought: str) -> str:
    tools_text = get_tool_descriptions()

    return f"""You decided to use a tool.

    Task: {task}
    Your reasoning: {thought}

    Tools available:
    {tools_text}

    Which tool and what input?"""


def build_answer_prompt(task: str, thought: str, history: list) -> str:
    history_text = format_history(history)

    return f"""You have enough information to answer.

    Task: {task}
    Your reasoning: {thought}

    What you found out:
    {history_text}

    Give your final answer."""


def format_history(history: list) -> str:
    if not history:
        return "Nothing yet."
    
    lines = []
    for entry in history:
        if entry["role"] == "thought":
            lines.append(f"Thought: {entry['content']}")
        elif entry["role"] == "tool_call":
            lines.append(f"Used tool '{entry['tool']}' with input: {entry['input']}")
        elif entry["role"] == "observation":
            lines.append(f"Tool returned: {entry['content']}")
    
    return "\n".join(lines)