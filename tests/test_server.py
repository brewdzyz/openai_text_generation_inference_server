import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from server import app, RequestBody
from unittest.mock import AsyncMock, patch

client = TestClient(app)

class MockStream:
    async def __aiter__(self):
        yield {
            'choices': [{
                'delta': {'content': 'Test response'},
                'finish_reason': None
            }]
        }

@pytest.mark.asyncio
@patch("server.get_openai_stream_data", return_value=MockStream())
async def test_generate_stream(mock_get_openai_stream_data):
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
