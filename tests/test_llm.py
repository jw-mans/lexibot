import pytest
from unittest.mock import patch, MagicMock

from src.core.llm.client import GPTClient
from src.core.llm.pipeline import Pipeline

# Client Tests

@pytest.fixture
def mock_yandex_response():
    "Fake response from GPT API"
    return {
        "result": {
            "alternatives": [
                {"message": {"text": "Это тестовый ответ от YandexGPT."}}
            ]
        }
    }

@patch("requests.post")
def test_client_complete(mock_post, mock_yandex_response):
    """Test that client sends correct request and processes response."""
    mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_yandex_response)

    client = GPTClient()
    result = client.complete(
        messages=[{"role": "user", "text": "Привет!"}],
        temperature=0.7,
        max_tokens=100
    )

    assert "тестовый ответ" in result # check response content
    # check that request gone out to correct URL with proper headers and payload
    mock_post.assert_called_once()
    call_args = mock_post.call_args[1]
    assert call_args["headers"]["Authorization"].startswith("Api-Key")
    assert "messages" in call_args["json"]
    assert call_args["json"]["completionOptions"]["temperature"] == 0.7

# LLM Pipeline Tests

@patch.object(GPTClient, "complete", return_value="Ответ от модели")
def test_llm_pipeline_ask(mock_complete):
    """Test that pipeline constructs prompt and calls client correctly."""
    pipeline = Pipeline(GPTClient())

    result = pipeline.ask("Это контекст", "О чём текст?")
    assert result == "Ответ от модели"

    mock_complete.assert_called_once()
    args, kwargs = mock_complete.call_args
    messages = args[0]

    # check that prompt contain context and question
    assert any("контекст" in m["text"].lower() for m in messages)
    assert any("вопрос" in m["text"].lower() for m in messages)
