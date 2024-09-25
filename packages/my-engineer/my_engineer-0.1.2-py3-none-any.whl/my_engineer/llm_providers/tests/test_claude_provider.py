import pytest
from llm_providers.providers.claude_provider import ClaudeProvider
from unittest.mock import patch, MagicMock
import logging
from llm_providers.logging_utils import logger

logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

@pytest.fixture
def claude_provider(tmp_path):
    return ClaudeProvider(run_dir=str(tmp_path))

def test_generate_response_with_system_message(claude_provider):
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="I'm doing well, thank you for asking!")]
    
    # Mock the usage attribute
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = 10
    mock_response.usage.output_tokens = 20
    mock_response.usage.cache_creation_input_tokens = 5
    mock_response.usage.cache_read_input_tokens = 3
    
    with patch.object(claude_provider.client.messages, 'create', return_value=mock_response) as mock_create, \
         patch('llm_providers.logging_utils.setup_logging') as mock_setup_logging:
    
        response = claude_provider.generate_response(messages)
    
        assert response == "I'm doing well, thank you for asking!"
        mock_create.assert_called_once()
    
        call_args = mock_create.call_args[1]
        print(f"Debug - call_args: {call_args}")  # Add this line for debugging
        assert "messages" in call_args, f"Expected 'messages' in call_args, but got {call_args.keys()}"
        assert isinstance(call_args["messages"], list), f"Expected 'messages' to be a list, but got {type(call_args['messages'])}"
        assert len(call_args["messages"]) == 1, f"Expected 1 message, but got {len(call_args['messages'])}"
        
        user_message = call_args["messages"][0]
        assert user_message["role"] == "user", f"Expected message role to be 'user', but got {user_message['role']}"
        assert user_message["content"][0]["text"] == "Hello, how are you?", f"Unexpected user message: {user_message['content'][0]['text']}"

        assert "system" not in call_args, "Unexpected 'system' key in call_args"