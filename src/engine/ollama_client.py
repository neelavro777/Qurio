import ollama
import json
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from src.utils.logger import logger
from src.utils.exceptions import EngineError

T = TypeVar("T", bound=BaseModel)

class OllamaEngine:
    def __init__(self, model_name: str = "qwen3.5:0.8b"):
        self.model_name = model_name

    def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        """
        Generates a structured response from Ollama.
        Improved for tiny models (0.8b) by simplifying instructions.
        """
        # Simplify the schema representation for small models
        schema_dict = schema.model_json_schema()
        fields_info = "\n".join([
            f"- {k}: {v.get('description', '')} ({v.get('type', 'any')})"
            for k, v in schema_dict.get("properties", {}).items()
        ])

        system_prompt = (
            "You are a focused assistant that ONLY outputs JSON. Do not explain anything.\n"
            "Output a JSON object with these fields:\n"
            f"{fields_info}\n\n"
            "IMPORTANT: Do not wrap the output in 'properties' or 'schema' tags. Just the flat JSON object."
        )

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            format="json",
        )

        content = response["message"]["content"]
        try:
            data = json.loads(content)
            
            # Robust extraction: if the model echoed the schema structure
            if "properties" in data and isinstance(data["properties"], dict):
                # Check if the keys of the properties dict match our schema
                props = data["properties"]
                expected_keys = schema.model_fields.keys()
                # If the inner dict has the actual values, use it
                if any(k in props for k in expected_keys):
                    data = props

            return schema.model_validate(data)
        except Exception as e:
            logger.error(f"Error parsing response: {content}")
            raise EngineError(f"Failed to parse structured response from Ollama: {e}") from e
