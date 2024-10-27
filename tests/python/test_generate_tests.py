```python
import pytest
from unittest.mock import patch, MagicMock
from generator import TestGenerator

@pytest.fixture
def test_generator():
    return TestGenerator()

def test_get_changed_files_empty_args(test_generator):
    assert test_generator.get_changed_files() == []

def test_get_changed_files_with_args(test_generator):
    import sys
    sys.argv = ['test.py', 'file1.py file2.js']
    assert test_generator.get_changed_files() == ['file1.py', 'file2.js']

@patch('builtins.open', return_value=MagicMock(read=lambda: 'print("Hello, World!")'))
def test_create_prompt_success(mock_open, test_generator):
    prompt = test_generator.create_prompt('test.py', 'Python')
    assert prompt is not None
    assert len(prompt) > 0

@patch('generator.requests.post')
def test_call_openai_api_success(mock_post, test_generator):
    mock_post.return_value.json.return_value = {'choices': [{'message': {'content': 'pytest code here'}}]}
    test_cases = test_generator.call_openai_api('test prompt')
    assert test_cases == 'pytest code here'

@patch('generator.requests.post', side_effect=requests.RequestException)
def test_call_openai_api_failure(mock_post, test_generator):
    test_cases = test_generator.call_openai_api('test prompt')
    assert test_cases is None

def test_detect_language_python(test_generator):
    assert test_generator.detect_language('file.py') == 'Python'

def test_detect_language_unknown(test_generator):
    assert test_generator.detect_language('file.unknown') == 'Unknown'

def test_get_test_framework_python(test_generator):
    assert test_generator.get_test_framework('Python') == 'pytest'

def test_get_test_framework_unknown(test_generator):
    assert test_generator.get_test_framework('Unknown') == 'unknown'

def test_save_test_cases_success(test_generator, tmp_path):
    test_cases = 'generated test cases'
    test_generator.save_test_cases(str(tmp_path / 'file.py'), test_cases, 'Python')
    file_path = tmp_path / 'tests' / 'python' / 'test_file.py'
    assert file_path.exists()
    with open(file_path, 'r') as f:
        assert f.read() == test_cases

def test_save_test_cases_failure(test_generator, tmp_path):
    with patch('builtins.open', side_effect=Exception):
        test_generator.save_test_cases(str(tmp_path / 'file.py'), 'generated test cases', 'Python')
    file_path = tmp_path / 'tests' / 'python' / 'test_file.py'
    assert not file_path.exists()

def test_run_no_files_changed(caplog, test_generator):
    test_generator.get_changed_files = MagicMock(return_value=[])
    test_generator.run()
    assert "No files changed." in caplog.text

def test_run_with_files_changed_success(caplog, test_generator):
    import sys
    sys.argv = ['test.py', 'file.py']
    with patch.object(test_generator, 'create_prompt', return_value='test prompt'), \
         patch.object(test_generator, 'call_openai_api', return_value='generated test cases'):
        test_generator.run()
    assert "Processing file.py (Python)" in caplog.text
    assert "Test cases saved to" in caplog.text

def test_run_with_files_changed_unknown_language(caplog, test_generator):
    import sys
    sys.argv = ['test.py', 'file.unknown']
    test_generator.run()
    assert "Unsupported file type: file.unknown" in caplog.text

def test_run_with_files_changed_failed_generation(caplog, test_generator):
    import sys
    sys.argv = ['test.py', 'file.py']
    with patch.object(test_generator, 'create_prompt', return_value='test prompt'), \
         patch.object(test_generator, 'call_openai_api', return_value=None):
        test_generator.run()
    assert "Failed to generate test cases" in caplog.text
```