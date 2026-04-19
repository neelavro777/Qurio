import math

from src.utils.exceptions import ToolError

def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except Exception as e:
        raise ToolError(f"Calculator failed to evaluate '{expression}'. Reason: {e}")