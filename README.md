# Qurio: Local ReAct Agent

Qurio is a modular, reasoning-capable agent powered by local LLMs (via Ollama). It implements the **ReAct (Reason + Act)** pattern to solve tasks by thinking, selecting tools, and processing observations.

## Key Features
- **Local-First**: Runs entirely on your machine using Ollama (default: `qwen3.5:0.8b`).
- **Structured Reasoning**: Uses explicit "Thought" and "Tool Call" phases for reliable behavior.
- **Schema Validation**: Powered by Pydantic to ensure the LLM follows strict JSON structures.
- **Tool Registry**: Easily add new capabilities in `src/tools/`.


## Repository Structure
```text
Qurio/
├── logs/             # Application logs (app.log)
├── src/
│   ├── agent/        # Core ReAct loop and prompt logic
│   ├── engine/       # Ollama connector and structured generation
│   ├── schemas/      # Pydantic data models
│   ├── tools/        # Tool definitions and registry
│   └── utils/        # Logger and custom exceptions
├── main.py           # Entry point
└── requirements.txt  # Dependencies
```

## 🛠 Setup & Usage

### 1. Prerequisites
- [Ollama](https://ollama.com/) installed and running.
- Pull the default model:
  ```bash
  ollama pull qwen3.5:0.8b
  ```

### 2. Installation
```bash
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Running the Agent
Simply run the main script and follow the prompt:
```bash
python main.py
```

## 🧠 How it Works
The agent followed a 3-step cycle for every task:
1. **Think**: The agent analyzes the task and decides if it needs a tool.
2. **Act**: If a tool is needed, it generates the specific arguments and executes it via the registry.
3. **Observe**: The output of the tool is fed back into its memory (history) for the next reasoning step.

## Error Handling
Qurio uses a custom exception system:
- **EngineError**: Raised if Ollama fails or returns invalid JSON.
- **ToolError**: Raised if a tool fails or is misused, allowing the agent to self-correct.
