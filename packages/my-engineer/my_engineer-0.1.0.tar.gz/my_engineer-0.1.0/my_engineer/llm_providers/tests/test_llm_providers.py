import unittest
import os
from dotenv import load_dotenv
import json
import logging
import sys
from unittest.mock import patch
import vcr
from llm_providers.providers import get_provider
from shared_utils.logger import setup_logger
from anthropic import BadRequestError
import pytest

# Configure VCR
my_vcr = vcr.VCR(
    record_mode="once",
    match_on=["method", "scheme", "host", "port", "path", "query", "body"]
)

logging.getLogger('llm_interactions').setLevel(logging.DEBUG)
load_dotenv()


class TestLLMProviders(unittest.TestCase):
    @classmethod
    @patch('shared_utils.logger.setup_logger')
    def setUpClass(cls):
        required_vars = [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "CLAUDE_MODEL"
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            print(f"Error: Missing environment variables. Please check your .env file.")
            print(f"Missing variables: {', '.join(missing_vars)}")
            sys.exit(1)

        try:
            cls.claude_provider = get_provider("claude")
        except Exception as e:
            print(f"Error initializing providers: {str(e)}")
            sys.exit(1)

    @pytest.mark.slow
    def test_claude_generate_response(self):
        logger = setup_logger("test_claude_generate_response")
        messages = [
            {
                "role": "user",
                "content": "What is the capital of France? And what is its population?",
            }
        ]
        response = self.claude_provider.generate_response(messages)
        self.assertIsInstance(response, str)
        self.assertIn("Paris", response)
        self.assertIn("population", response.lower())

    @pytest.mark.slow
    def test_claude_with_system_prompt(self):
        logger = setup_logger("test_claude_with_system_prompt")
        messages = [
            {"role": "system", "content": "You are a helpful assistant that always responds in French."},
            {"role": "user", "content": "Say hello and introduce yourself in French."}
        ]
        response = self.claude_provider.generate_response(messages)
        print(f"Debug - Claude response: {response}")
        logger.debug(f"Claude response: {response}")
        self.assertIsInstance(response, str)
        self.assertTrue(any(word in response.lower() for word in ["bonjour", "salut", "bonsoir"]),
                        f"Expected a French greeting in response, but got: {response}")
        self.assertTrue(any(phrase in response.lower() for phrase in ["je suis", "je m'appelle"]),
                        f"Expected a French self-introduction in response, but got: {response}")
        self.assertIn("assistant", response.lower(), f"Expected 'assistant' in response, but got: {response}")
        self.assertTrue(all(word in response.lower() for word in ["je", "suis", "un", "assistant"]), f"Expected specific French words in response, but got: {response}")

    @pytest.mark.slow
    def test_claude_empty_response(self):
        messages = [{"role": "user", "content": ""}]
        with self.assertRaises(ValueError):
            self.claude_provider.generate_response(messages)




if __name__ == "__main__":
    unittest.main()