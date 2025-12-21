# FastAPI LLM Project

A FastAPI-based AI Chat Service with streaming support for Large Language Model (LLM) interactions.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 💬 **Streaming Chat** - Server-sent events (SSE) for real-time chat responses
- 🔄 **Health Check** - Service health monitoring endpoint
- 🐳 **Docker Support** - DevContainer configuration for easy development
- 📦 **Type Safety** - Pydantic models for request/response validation

## Project Structure

```
fastApi-llm-project/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chat.py          # Chat streaming endpoint
│   │   │   ├── health.py        # Health check endpoint
│   │   │   └── router.py        # API v1 router
│   │   └── router.py            # Main API router
│   ├── core/
│   │   └── config.py            # Application configuration
│   ├── models/
│   │   ├── chat.py              # Chat request/response models
│   │   └── health.py            # Health check models
│   ├── services/
│   │   └── chat_service.py      # Chat streaming service logic
│   └── main.py                  # FastAPI application entry point
├── .devcontainer/
│   ├── Dockerfile               # Development container image
│   └── devcontainer.json        # VS Code devcontainer configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ObaidaExperts/fastApi-llm-project.git
cd fastApi-llm-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Health Check
```http
GET /api/v1/health
```

Response:
```json
{
  "status": "ok",
  "service": "ai-chat-service"
}
```

#### Chat Stream
```http
POST /api/v1/chat/stream
Content-Type: application/json
```

Request Body:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ],
  "stream": true
}
```

Response: Server-Sent Events (SSE) stream
```
data: Hello 
data: how 
data: are 
data: you? 
data: [DONE]
```

### Example Usage with cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Chat stream
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Tell me a joke"}
    ]
  }'
```

## Development

### Using DevContainer

This project includes a VS Code DevContainer configuration for a consistent development environment:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. The container will automatically:
   - Install dependencies
   - Start the FastAPI server on port 8000
   - Configure Python extensions

### Environment Variables

Create a `.env` file in the project root for environment-specific configuration:

```env
# Add your environment variables here
```

## Dependencies

- **fastapi** >= 0.110 - Web framework
- **uvicorn[standard]** >= 0.27 - ASGI server
- **pydantic** >= 2.0 - Data validation

## Next Steps

To integrate with a real LLM provider:

1. Update `app/services/chat_service.py` to connect to your LLM API
2. Add API keys to your `.env` file
3. Update `app/core/config.py` to load configuration from environment variables

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
