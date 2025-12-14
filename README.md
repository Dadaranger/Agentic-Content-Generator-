# Agentic Content Generator

A powerful AI-driven content generation system built with LangGraph and FastAPI that generates blog content with titles and supports multi-language translation using the Groq LLM API.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Request Examples](#request-examples)
- [Architecture](#architecture)
  - [Components](#components)
  - [Workflow](#workflow)
- [Dependencies](#dependencies)
- [API Keys & Configuration](#api-keys--configuration)
- [Development](#development)
- [License](#license)

## 🎯 Overview

The Agentic Content Generator is an intelligent content creation system that leverages large language models to generate high-quality blog content. It supports two main use cases:

1. **Basic Content Generation**: Generate a blog post with an engaging title and detailed content based on a topic
2. **Content Generation with Translation**: Generate blog content and automatically translate it into specified languages (Traditional Chinese or Japanese)

The system uses LangGraph to orchestrate complex workflows and FastAPI for REST API endpoints.

## ✨ Features

- **Intelligent Title Generation**: Creates engaging, SEO-friendly blog titles
- **Content Generation**: Produces detailed, well-structured blog content in Markdown format
- **Multi-language Support**: Translates generated content into Traditional Chinese and Japanese
- **State Management**: Tracks content state through the generation pipeline
- **RESTful API**: Easy-to-use HTTP endpoints for content generation
- **LLM Integration**: Uses Groq's powerful Llama 3.1 8B model
- **LangSmith Monitoring**: Integrated with LangSmith for debugging and monitoring

## 📁 Project Structure

```
ContentGenerator/
├── src/
│   ├── __init__.py
│   ├── graphs/
│   │   ├── __init__.py
│   │   └── graph_builder.py          # LangGraph workflow orchestration
│   ├── llms/
│   │   ├── __init__.py
│   │   └── groqllm.py                # Groq LLM wrapper
│   ├── nodes/
│   │   ├── __init__.py
│   │   └── content_node.py           # Content generation nodes
│   └── states/
│       ├── __init__.py
│       └── contentstate.py           # State definitions
├── app.py                             # FastAPI application
├── main.py                            # Entry point
├── pyproject.toml                     # Project dependencies
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables (not in repo)
├── request.json                       # Example API requests
└── README.md                          # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.13+
- pip or uv package manager
- API Keys for Groq, LangSmith, and optionally Tavily

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ContentGenerator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Unix
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGCHAIN_PROJECT="Agentic Content Generator"
   TAVILY_API_KEY=your_tavily_api_key (optional)
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq LLM service | ✅ Yes |
| `LANGSMITH_API_KEY` | API key for LangSmith monitoring | ✅ Yes |
| `LANGCHAIN_PROJECT` | Project name for LangSmith | ✅ Yes |
| `TAVILY_API_KEY` | API key for Tavily search (optional) | ❌ No |

### LLM Configuration

The system uses the **Llama 3.1 8B Instant** model from Groq for optimal performance and cost efficiency. This can be modified in `src/llms/groqllm.py`.

## 📡 Usage

### Running the Application

```bash
python app.py
```

The API will start on `http://0.0.0.0:8000`

### API Endpoints

#### 1. Content Generation Endpoint

**Endpoint:** `POST /content/`

**Description:** Generate blog content based on a topic, with optional translation

**Request Body:**

```json
{
  "topic": "string (required)",
  "language": "string (optional)"
}
```

**Parameters:**
- `topic` (required): The subject for blog content generation
- `language` (optional): Target language for translation. Supported values:
  - `"traditional chinese"`
  - `"japanese"`
  - Any other language will skip translation and return English content

**Response:**

```json
{
  "data": {
    "topic": "your_topic",
    "blog": {
      "title": "Generated blog title",
      "content": "Generated blog content in Markdown format"
    },
    "current_language": "target_language"
  }
}
```

### Request Examples

#### Example 1: Basic Content Generation (English)

```bash
curl -X POST http://localhost:8000/content/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "climate change"}'
```

**Or using the request.json file:**
```json
{
  "topic": "weather_update"
}
```

#### Example 2: Content Generation with Traditional Chinese Translation

```bash
curl -X POST http://localhost:8000/content/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "artificial intelligence", "language": "traditional chinese"}'
```

**Or using the request.json file:**
```json
{
  "topic": "weather_update",
  "language": "traditional chinese"
}
```

#### Example 3: Content Generation with Japanese Translation

```bash
curl -X POST http://localhost:8000/content/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "machine learning", "language": "japanese"}'
```

## 🏗️ Architecture

### Components

#### 1. **State Management** (`src/states/contentstate.py`)

Defines the data structures that flow through the pipeline:

- **`Maincontent`** (Pydantic Model): Represents generated content
  - `title`: Blog title
  - `content`: Blog body content

- **`ContentState`** (TypedDict): Manages pipeline state
  - `topic`: User input topic
  - `blog`: Generated content (Maincontent)
  - `current_language`: Target language for translation

#### 2. **LLM Integration** (`src/llms/groqllm.py`)

The `GroqLLM` class encapsulates:
- LLM initialization with Groq API
- Model selection (Llama 3.1 8B Instant)
- Error handling for API failures
- API key management

#### 3. **Content Nodes** (`src/nodes/content_node.py`)

The `ContentNode` class contains workflow nodes:

- **`title_creation(state)`**: Creates an engaging blog title
  - Input: Topic
  - Output: Blog title with SEO optimization
  - Prompt: Expert blog writer persona

- **`content_creation(state)`**: Generates detailed blog content
  - Input: Topic and generated title
  - Output: Markdown-formatted blog content
  - Prompt: Expert blog writer with detailed breakdown

- **`translation(state)`**: Translates content to target language
  - Input: Blog content and target language
  - Output: Translated blog content
  - Supports: Traditional Chinese, Japanese

- **`route(state)`**: Passes state through the routing layer
  - Input: Current state
  - Output: Updated state with language routing info

- **`route_decision(state)`**: Routes to appropriate translation node
  - Input: Target language
  - Output: Route selection (language-specific node or END)
  - Logic: Normalizes language input and selects appropriate node

#### 4. **Graph Orchestration** (`src/graphs/graph_builder.py`)

The `GraphBuilder` class orchestrates two workflows:

**Topic Graph (Basic Content Generation):**
```
START → title_creation → content_creation → END
```

**Language Graph (Content Generation + Translation):**
```
START → title_creation → content_creation → route →  
  ├─→ chinese_translation → END
  ├─→ japanese_translation → END
  └─→ END
```

#### 5. **FastAPI Application** (`app.py`)

REST API server exposing:
- Single POST endpoint: `/content/`
- Request validation and routing
- Graph selection based on input parameters
- Response formatting

### Workflow

#### Basic Workflow (Topic Only)
1. User sends topic via POST request
2. System generates engaging blog title
3. System generates detailed blog content
4. Results returned to user

#### Extended Workflow (Topic + Language)
1. User sends topic and target language via POST request
2. System generates engaging blog title
3. System generates detailed blog content
4. Route node determines translation target
5. System translates content to selected language
6. Results returned to user

## 📦 Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | >=0.122.1 | Web framework |
| `langchain` | >=1.1.0 | LLM orchestration |
| `langchain-core` | >=1.1.0 | Core LangChain functionality |
| `langchain-groq` | >=1.1.0 | Groq LLM integration |
| `langgraph` | >=1.0.4 | Workflow graph orchestration |
| `uvicorn` | >=0.38.0 | ASGI server |
| `watchdog` | >=6.0.0 | File watching for auto-reload |

### Optional Tools

- **langgraph-cli**: Command-line tools for LangGraph management
- **python-dotenv**: Environment variable loading

## 🔑 API Keys & Configuration

### Getting API Keys

1. **Groq API Key**
   - Visit: https://console.groq.com
   - Create an account
   - Generate API key from dashboard
   - Copy key to `.env` file

2. **LangSmith API Key**
   - Visit: https://smith.langchain.com
   - Create workspace
   - Generate API key
   - Copy key to `.env` file

3. **Tavily API Key** (Optional)
   - Visit: https://tavily.com
   - Create account
   - Generate API key (optional for search features)

### Testing API Keys

Verify your setup works:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GROQ_API_KEY:', os.getenv('GROQ_API_KEY')[:10] + '...' if os.getenv('GROQ_API_KEY') else 'Not set')"
```

## 🛠️ Development

### Running in Development Mode

```bash
python app.py
```

The server auto-reloads on file changes (via watchdog).

### Testing the API Locally

Using curl:
```bash
curl -X POST http://localhost:8000/content/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "test topic"}'
```

Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/content/",
    json={"topic": "test topic", "language": "traditional chinese"}
)
print(response.json())
```

### Monitoring with LangSmith

View trace details at: https://smith.langchain.com

All requests are automatically logged and can be inspected for:
- Input/output tracking
- Token usage
- Latency analysis
- Error debugging

### Code Structure Best Practices

- **Separation of Concerns**: Each module has a single responsibility
- **Type Hints**: Python type hints for better IDE support
- **Docstrings**: Clear documentation for all methods
- **Error Handling**: Try-catch blocks for API failures
- **Configuration Management**: Environment-based configuration

## 📊 Performance Notes

- **Model**: Llama 3.1 8B Instant (optimized for speed and cost)
- **Token Limit**: ~8K tokens per request
- **Average Generation Time**: 5-15 seconds depending on content length
- **API Rate Limits**: Depends on Groq plan

## 🐛 Troubleshooting

### Common Issues

1. **"Cannot import name 'BlogState'"**
   - Issue: Incorrect state class name
   - Solution: Use `ContentState` not `BlogState`

2. **"LANGSMITH_API_KEY not found"**
   - Issue: Missing environment variable
   - Solution: Check `.env` file and restart server

3. **"Groq API Error"**
   - Issue: Invalid API key or rate limit exceeded
   - Solution: Verify API key, check Groq dashboard

4. **Module not found errors**
   - Issue: Missing dependencies
   - Solution: Run `pip install -r requirements.txt`

## 📝 License

Personal Use

## 👤 Author

@Dadaranger

---

**Last Updated:** December 2025
**Version:** 0.1.0
