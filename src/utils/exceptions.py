class QurioError(Exception):
    """Base exception class for the Qurio agent."""
    pass

class EngineError(QurioError):
    """Raised when the LLM engine fails to generate or parse a response."""
    pass

class ToolError(QurioError):
    """Raised when a tool fails during execution."""
    pass

class AgentLoopError(QurioError):
    """Raised when there is an error in the agent's reasoning loop logic."""
    pass
