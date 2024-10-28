```python
import pytest
from unittest.mock import patch, MagicMock
from generator import TestGenerator

# Mocking external dependencies
@patch('generator.requests.post')
def test_call_openai_api_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {'choices': [{'message': {'content': 'Mocked test cases'}}]}
    mock_post.return_value = mock_response

    generator = TestGenerator()
    test_cases = generator.call_openai_api('mocked prompt')

    assert test_cases == 'Mocked test cases'

def test_detect_language_unknown_extension():
    generator = TestGenerator()
    language = generator.detect_language('test.unknown')
    
    assert language == 'Unknown'

def test_get_test_framework_unknown_language():
    generator = TestGenerator()
    framework = generator.get_test_framework('Ruby')

    assert framework == 'unknown'

def test_create_prompt_file_error(caplog):
    generator = TestGenerator()
    prompt = generator.create_prompt('non_existent_file.py', 'Python')

    assert prompt is None
    assert 'Error reading file' in caplog.text

def test_save_test_cases_error(caplog):
    generator = TestGenerator()
    generator.save_test_cases('test.js', 'mocked test cases', 'JavaScript')

    assert 'Error saving test cases' not in caplog.text

def test_run_no_files_changed(caplog):
    generator = TestGenerator()
    generator.run()

    assert 'No files changed' in caplog.text

def test_run_unsupported_file(caplog):
    generator = TestGenerator()
    generator.detect_language = MagicMock(return_value='Unknown')
    generator.run()

    assert 'Unsupported file type' in caplog.text

def test_run_processing_error(caplog):
    generator = TestGenerator()
    generator.detect_language = MagicMock(side_effect=Exception('Error'))
    generator.run()

    assert 'Error processing' in caplog.text

# Add more test cases for edge cases, normal cases, and error cases
```