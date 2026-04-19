# Project Explanation: Local ReAct Agent (Qurio)

This repository is designed to be a modular foundation for a local **ReAct (Reason + Act) Agent** using the Ollama engine. Below is a breakdown of how the code works and what each part does.

---

## 📂 Repository Structure

```text
Qurio/
├── src/
│   ├── engine/       # Logic for connecting to LLMs (Ollama)
│   ├── schemas/      # Data structures and validation (Pydantic)
│   └── prompts/      # Persona and strategy templates (Future use)
├── main.py           # Entry point for testing components
└── requirements.txt  # Project dependencies
```

---

## 🧠 Core Components

### 1. The Engine (`src/engine/ollama_client.py`)
This is the "connector" that talks to Ollama. It doesn't just send text; it manages **Structured Generation**.

#### Key Logic Snippet:
```python
def generate_structured(self, prompt: str, schema: Type[T]) -> T:
    # 1. Simplify the schema for the 0.8B model
    schema_dict = schema.model_json_schema()
    fields_info = "\n".join([f"- {k}: {v.get('description', '')}" for k, v in schema_dict.get("properties", {}).items()])

    # 2. Strict System Prompt
    system_prompt = f"Output a JSON object with these fields:\n{fields_info}"

    # 3. Handle 'Hypnotized' Tiny Models
    if "properties" in data and isinstance(data["properties"], dict):
        data = data["properties"]  # Extract actual data if model echoed the schema structure
```

**What it does:**
- **Prompt Simplification**: Small models (like `0.8b`) get confused by complex JSON Schemas. We convert the schema into a simple bulleted list to make it easier for the model to follow.
- **Robustness**: If the model "hallucinates" and returns data wrapped in a `properties` or `required` tag (echoing the schema itself), our code automatically "digs" into the JSON to find the correct data.

---

### 2. The Schemas (`src/schemas/models.py`)
We use **Pydantic** to define our data models. This serves two purposes:
1.  **Documentation**: It tells the model exactly what we want.
2.  **Validation**: It guarantees that the data returned by the LLM is correctly typed (e.g., "age" must be an integer).

#### Example:
```python
class UserProfile(BaseModel):
    name: str = Field(description="The full name of the user")
    age: int = Field(description="The age of the user")
    interests: List[str] = Field(description="A list of interests or hobbies")
```

**What it does:**
- If the model forgets a field or returns a string for "age", the code will throw a clear error instead of crashing later.

---

### 3. The Integration (`main.py`)
This is where we glue everything together to test it.

```python
def test_structured_output():
    engine = OllamaEngine(model_name="qwen3.5:0.8b")
    profile = engine.generate_structured("My name is John Doe...", UserProfile)
    print(profile.model_dump_json(indent=2))
```

**What it does:**
- It initializes the `OllamaEngine`.
- It picks a target `schema` (`UserProfile`).
- It passes the user's natural language to the engine and receives a **fully validated Python object** back.

---

### 🚀 Summary of the Flow
1.  **Input**: User sends "I'm 28 and like coding."
2.  **Mapping**: Code looks at the `UserProfile` schema to see what's needed.
3.  **Prompting**: Engine asks Ollama for a JSON with `name`, `age`, and `interests`.
4.  **Healing**: If Ollama makes a structural mistake, the engine fixes it.
5.  **Validation**: Pydantic ensures `28` is a number and `coding` is in a list.
6.  **Output**: You get a clean Python object ready for use!
