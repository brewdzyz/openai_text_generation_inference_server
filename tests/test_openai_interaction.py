import pytest
import requests
import json
import os
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

# Load the API key from environment variables
api_key = os.environ.get('OPENAI_API_KEY')

def test_openai_interaction():
    # Ensure the API key is set before proceeding
    assert api_key is not None, "API key is not set"

    # Example input for the OpenAI API
    input_text = "Translate the following English text to French: 'Hello, how are you?'"

    # Construct the request body
    request_body = {
        "inputs": input_text,
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 100
        }
    }

    # Send a request to the server
    response = client.post(
        "/generate_stream",
        json=request_body,
    )

    # Ensure the response status code is 200 (OK)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Ensure the response is valid JSON
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        pytest.fail("Response is not valid JSON")

    # Ensure the response contains expected keys
    assert 'token' in response_json, "Response JSON does not contain 'token' key"
    assert 'generated_text' in response_json, "Response JSON does not contain 'generated_text' key"
    assert 'details' in response_json, "Response JSON does not contain 'details' key"

    # Ensure the generated text is as expected
    generated_text = response_json['generated_text']
    assert generated_text == "Bonjour, comment ça va ?", f"Unexpected generated text: {generated_text}"

    # (Optional) Additional checks for other response fields or values...
