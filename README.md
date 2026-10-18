markdown
# LangGraph Research Agent

A conversational AI agent built with LangGraph that intelligently routes questions — answering from knowledge or searching the web in real time.

## Tech Stack

- **LangGraph** — agent orchestration and state management
- **Claude (Anthropic)** — LLM for answering and routing decisions
- **Tavily** — real-time web search
- **LangChain** — LLM integration layer
- **Python 3.11**

## Features

- Automatically decides whether to answer directly or search the web
- Maintains conversation memory across turns
- Clean modular project structure

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/bhavith0999/langraph-agent.git
cd langraph-agent
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file in the root:

ANTHROPIC_API_KEY=your-anthropic-key
TAVILY_API_KEY=your-tavily-key


### 5. Run

```bash
python main.py
```

## Project Structure

langraph-agent/
├── main.py
├── requirements.txt
└── src/
└── agent/
├── state.py # shared agent state
├── nodes.py # router, answer, search nodes
└── graph.py # graph assembly


## How It Works

User question
↓
Router node — Claude decides: search or answer?
↓
┌────┴────┐
Answer Search
node node (Tavily + Claude)
└────┬────┘
↓
Reply to user