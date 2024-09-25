import pytest
import os
from unittest.mock import patch, Mock
from llm_providers.logging_utils import setup_logging, log_formatted_json
import logging


@pytest.fixture
def mock_logger():
    with patch("llm_providers.logging_utils.logging.getLogger") as mock:
        mock_logger = Mock()
        mock.return_value = mock_logger
        yield mock_logger


@pytest.fixture
def mock_file_handler():
    with patch("llm_providers.logging_utils.logging.FileHandler") as mock:
        yield mock


@pytest.fixture
def mock_mongodb_logger():
    with patch("llm_providers.logging_utils.MongoDBLogger") as mock:
        yield mock



def test_log_formatted_json(mock_logger, mock_mongodb_logger):
    message = "Test message"
    data = {"key": "value"}

    with patch("llm_providers.logging_utils.logger", mock_logger), patch(
        "llm_providers.logging_utils.mongo_logger", mock_mongodb_logger
    ):
        log_formatted_json(message, data)

    mock_logger.info.assert_called_once()
    mock_mongodb_logger.log.assert_called_once_with(message, data)
