```python
import pytest
from unittest.mock import patch

from generator import TestGenerator


@pytest.fixture
def test_generator():
    return TestGenerator()


def test_get_changed_files_no_args(test_generator):
    assert test_generator.get_changed_files() == []


def test_get_changed_files_with_args():
    import sys

    sys.argv = ['script.py', 'file1.py file2.js']
    generator = TestGenerator()
    assert generator.get_changed_files() == ['file1.py', 'file2.js']


def test_detect_language_python(test_generator):
    assert test_generator.detect_language('test.py') == 'Python'


def test_detect_language_unknown(test_generator):
    assert test_generator.detect_language('test.txt') == 'Unknown'


def test_get_test_framework_python(test_generator):
    assert test_generator.get_test_framework('Python') == 'pytest'


def test_get_test_framework_unknown(test_generator):
    assert test_generator.get_test_framework('Unknown') == 'unknown'


def test_create_prompt_success(test_generator):
    with patch('builtins.open', create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = "print('Hello, World!')"
        prompt = test_generator.create_prompt('test.py', 'Python')
        assert prompt is not None


def test_create_prompt_failure(test_generator):
    with patch('builtins.open', side_effect=Exception):
        prompt = test_generator.create_prompt('test.py', 'Python')
        assert prompt is None


def test_call_openai_api_success(test_generator):
    test_generator.api_key = 'test_key'
    test_generator.model = 'test_model'
    test_generator.max_tokens = 2000
    prompt = 'Generate test cases'
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'choices': [{'message': {'content': 'Generated test cases'}}}
        assert test_generator.call_openai_api(prompt) == 'Generated test cases'


def test_call_openai_api_failure(test_generator):
    test_generator.api_key = 'test_key'
    test_generator.model = 'test_model'
    test_generator.max_tokens = 2000
    prompt = 'Generate test cases'
    with patch('requests.post', side_effect=Exception):
        assert test_generator.call_openai_api(prompt) is None


def test_save_test_cases_success(test_generator, tmp_path):
    test_generator.save_test_cases(str(tmp_path / 'test.py'), 'def test_example():\n    assert True\n', 'Python')
    test_file = tmp_path / 'tests/python/test_test.py'
    assert test_file.exists()


def test_save_test_cases_failure(test_generator, tmp_path):
    with patch('builtins.open', side_effect=Exception):
        test_generator.save_test_cases(str(tmp_path / 'test.py'), 'def test_example():\n    assert True\n', 'Python')
    test_file = tmp_path / 'tests/python/test_test.py'
    assert not test_file.exists()


def test_run_no_files_changed(test_generator, caplog):
    test_generator.run()
    assert "No files changed." in caplog.text


def test_run_unsupported_file_type(test_generator, caplog):
    with patch('generator.TestGenerator.detect_language') as mock_detect_language:
        mock_detect_language.return_value = 'Unknown'
        test_generator.run()
        assert "Unsupported file type" in caplog.text


def test_run_success(test_generator, tmp_path, caplog):
    with patch('generator.TestGenerator.call_openai_api') as mock_call_openai_api:
        mock_call_openai_api.return_value = 'def test_example():\n    assert True\n'
        sys.argv = ['script.py', str(tmp_path / 'test.py')]
        test_generator.run()
        test_file = tmp_path / 'tests/python/test_test.py'
        assert test_file.exists()
        assert "Test cases saved to" in caplog.text


def test_run_error(test_generator, caplog):
    with patch('generator.TestGenerator.detect_language', side_effect=Exception):
        test_generator.run()
        assert "Error processing" in caplog.text
```