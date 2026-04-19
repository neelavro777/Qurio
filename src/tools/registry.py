from src.tools.calculator import calculator
from src.utils.exceptions import ToolError

# name → (function, one-line description)
TOOLS = {
    "calculator": (
        calculator,
        "Evaluates a math expression. Input: a math expression like '2 + 2' or '340 * 0.15'"
    )
}

def get_tool_descriptions() -> str:
    lines = []
    for name, (_, description) in TOOLS.items():
        lines.append(f"- {name}: {description}")
    return "\n".join(lines)


def run_tool(name: str, input: str) -> str:
    if name not in TOOLS:
        raise ToolError(f"'{name}' is not a valid tool. Available tools: {list(TOOLS.keys())}")
    func, _ = TOOLS[name]
    return func(input)