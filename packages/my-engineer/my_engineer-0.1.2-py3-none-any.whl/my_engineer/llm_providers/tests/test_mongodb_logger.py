import pytest
from unittest.mock import Mock, patch
from llm_providers.mongodb_logger import MongoDBLogger

@pytest.fixture
def mock_mongo_client():
    with patch('llm_providers.mongodb_logger.MongoClient') as mock:
        yield mock

def test_mongodb_logger_initialization(mock_mongo_client):
    logger = MongoDBLogger()
    mock_mongo_client.assert_called_once_with('localhost', 27017)

def test_log_interaction(mock_mongo_client):
    logger = MongoDBLogger()
    mock_collection = Mock()
    logger.db.__getitem__.return_value = mock_collection

    logger.log_interaction('test_type', {'request': 'data'}, {'response': 'data'})

    mock_collection.insert_one.assert_called_once()
    args, _ = mock_collection.insert_one.call_args
    assert args[0]['type'] == 'test_type'
    assert 'request' in args[0]
    assert 'response' in args[0]

def test_log_request_response(mock_mongo_client):
    logger = MongoDBLogger()
    mock_collection = Mock()
    logger.db.__getitem__.return_value = mock_collection

    logger.log_request_response('test_provider', {'request': 'data'}, {'response': 'data'})

    mock_collection.insert_one.assert_called_once()
    args, _ = mock_collection.insert_one.call_args
    assert args[0]['type'] == 'test_provider_interaction'

def test_log_error(mock_mongo_client):
    logger = MongoDBLogger()
    mock_collection = Mock()
    logger.db.__getitem__.return_value = mock_collection

    logger.log_error('test_provider', {'error': 'data'})

    mock_collection.insert_one.assert_called_once()
    args, _ = mock_collection.insert_one.call_args
    assert args[0]['type'] == 'test_provider_error'
