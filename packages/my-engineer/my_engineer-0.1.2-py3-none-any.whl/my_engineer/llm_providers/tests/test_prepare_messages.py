import unittest
from llm_providers.providers import prepare_messages
import pytest

@pytest.mark.unit
class TestPrepareMessages(unittest.TestCase):
    def test_empty_messages(self):
        messages = []
        result = prepare_messages(messages)
        self.assertEqual(result, [])

    def test_single_message(self):
        messages = [{"role": "user", "content": "Hello"}]
        result = prepare_messages(messages)
        self.assertEqual(result, messages)

    def test_alternating_messages(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
            {"role": "user", "content": "How are you?"},
        ]
        result = prepare_messages(messages)
        self.assertEqual(result, messages)

    def test_consecutive_user_messages(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm fine, thanks"},
        ]
        expected = [
            {"role": "user", "content": "Hello\nHow are you?"},
            {"role": "assistant", "content": "I'm fine, thanks"},
        ]
        result = prepare_messages(messages)
        self.assertEqual(result, expected)

    def test_consecutive_assistant_messages(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
            {"role": "assistant", "content": "How can I help you?"},
            {"role": "user", "content": "I have a question"},
        ]
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there\nHow can I help you?"},
            {"role": "user", "content": "I have a question"},
        ]
        result = prepare_messages(messages)
        self.assertEqual(result, expected)

    def test_mixed_consecutive_messages(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm fine"},
            {"role": "assistant", "content": "How can I help?"},
            {"role": "user", "content": "I have a question"},
            {"role": "user", "content": "About Python"},
        ]
        expected = [
            {"role": "user", "content": "Hello\nHow are you?"},
            {"role": "assistant", "content": "I'm fine\nHow can I help?"},
            {"role": "user", "content": "I have a question\nAbout Python"},
        ]
        result = prepare_messages(messages)
        self.assertEqual(result, expected)

    def test_empty_content_messages(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "Hi"},
            {"role": "assistant", "content": "  "},
            {"role": "user", "content": "How are you?"},
        ]
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": "How are you?"},
        ]
        result = prepare_messages(messages)
        self.assertEqual(result, expected)

    def test_system_messages(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
            {"role": "system", "content": "Remember to be polite"},
            {"role": "user", "content": "How are you?"},
        ]
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
            {"role": "user", "content": "How are you?"},
        ]
        result = prepare_messages(messages)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()