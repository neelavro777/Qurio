from pydantic import BaseModel, Field
from typing import List

class UserProfile(BaseModel):
    name: str = Field(description="The full name of the user")
    age: int = Field(description="The age of the user")
    interests: List[str] = Field(description="A list of interests or hobbies")

class ExtractionResult(BaseModel):
    summary: str = Field(description="A brief summary of the input text")
    sentiment: str = Field(description="The sentiment of the text (e.g., positive, negative, neutral)")
    keywords: List[str] = Field(description="Key topics mentioned in the text")

class ThinkStep(BaseModel):
    thought: str = Field(description="your reasoning about what to do next")
    needs_tool: bool = Field(description="true if you need a tool, false if you can answer now")

class ToolCall(BaseModel):
    tool_name: str = Field(description="exact name of the tool to use")
    tool_input: str = Field(description="the input to pass to the tool, as plain text")

class FinalAnswer(BaseModel):
    answer: str = Field(description="your final answer to the task")