import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from server import app, RequestBody
from unittest.mock import AsyncMock, patch

client = TestClient(app)

async def mock_openai_stream_data(request):
    yield {
        'choices': [{
            'delta': {'content': 'Test response'},
            'finish_reason': None
        }]
    }

@pytest.mark.asyncio
@patch("server.get_openai_stream_data", new=mock_openai_stream_data)
async def test_generate_stream():
    request_body = {
        "inputs": "What is AI?",
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 100
        }
    }

    response = client.post(
        "/generate_stream",
        json=request_body,
    )

    assert response.status_code == 200
    assert "Test response" in response.text
