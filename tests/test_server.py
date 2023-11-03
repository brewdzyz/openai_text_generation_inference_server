import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from server import app, get_openai_stream_data, RequestBody
from unittest.mock import AsyncMock, patch

client = TestClient(app)

@patch("server.openai.ChatCompletion.acreate", new_callable=AsyncMock)
def test_generate_stream(mock_acreate):
    mock_acreate.return_value = AsyncMock()
    mock_acreate.return_value.__aiter__.return_value = iter([{
        'choices': [{
            'delta': {'content': 'Test response'},
            'finish_reason': None
        }]
    }])

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

