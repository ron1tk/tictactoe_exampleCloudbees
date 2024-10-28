``` python
import pytest
from unittest.mock import patch, Mock
from generator import TestGenerator

@pytest.fixture
def test_generator():
    return TestGenerator()

def test_get_changed_files_empty_args(test_generator):
    assert test_generator.get_changed_files() == []

def test_get_changed_files_with_args():
    import sys
    sys.argv = ['test.py', 'file1.py file2.py']
    assert test_generator.get_changed_files() == ['file1.py', 'file2.py']

def test_detect_language_unknown_extension(test_generator):
    assert test_generator.detect_language('file.unknown') == 'Unknown'

def test_detect_language_known_extension():
    assert test_generator.detect_language('file.py') == 'Python'

def test_get_test_framework_unknown_language(test_generator):
    assert test_generator.get_test_framework('Ruby') == 'unknown'

def test_get_test_framework_known_language():
    assert test_generator.get_test_framework('Python') == 'pytest'

@patch('generator.requests')
def test_call_openai_api_success(mock_requests, test_generator):
    mock_response = Mock()
    mock_response.json.return_value = {'choices': [{'message': {'content': 'Generated test cases'}}]}
    mock_requests.post.return_value = mock_response

    test_cases = test_generator.call_openai_api('prompt')
    assert test_cases == 'Generated test cases'

@patch('generator.requests')
def test_call_openai_api_failure(mock_requests, test_generator):
    mock_requests.post.side_effect = Exception('API error')
    
    test_cases = test_generator.call_openai_api('prompt')
    assert test_cases is None

def test_save_test_cases_success(test_generator, tmp_path):
    test_cases = 'Generated test cases'
    test_generator.save_test_cases(str(tmp_path / 'file.py'), test_cases, 'Python')
    
    test_file = tmp_path / 'tests/python/test_file.py'
    assert test_file.exists()
    with open(test_file, 'r') as f:
        saved_test_cases = f.read()
    assert saved_test_cases == test_cases

def test_save_test_cases_failure(test_generator, tmp_path):
    test_cases = 'Generated test cases'
    with patch('builtins.open', side_effect=Exception('Write error')):
        test_generator.save_test_cases(str(tmp_path / 'file.py'), test_cases, 'Python')
    
    test_file = tmp_path / 'tests/python/test_file.py'
    assert not test_file.exists()

def test_run_no_files_changed(test_generator, caplog):
    test_generator.run()
    assert "No files changed." in caplog.text

def test_run_unsupported_file_type(test_generator, caplog):
    with patch('generator.logging.warning') as mock_warning:
        test_generator.run()
        assert mock_warning.called

def test_run_process_files_success(test_generator, caplog, tmp_path):
    test_file = tmp_path / 'file.py'
    test_file.write_text("print('Hello, World!')")
    sys.argv = ['test.py', str(test_file)]

    with patch('generator.logging.info') as mock_info:
        test_generator.run()
        assert "Processing" in [call[1][0] for call in mock_info.call_args_list]
        assert "Test cases saved to" in caplog.text

def test_run_process_files_failure(test_generator, caplog, tmp_path):
    test_file = tmp_path / 'file.py'
    test_file.write_text("invalid python code")
    sys.argv = ['test.py', str(test_file)]

    with patch('generator.logging.error') as mock_error:
        test_generator.run()
        assert "Error processing" in caplog.text
        assert mock_error.called

def test_run_fatal_error(test_generator, caplog):
    with patch('generator.TestGenerator.run', side_effect=Exception('Fatal error')):
        TestGenerator.run()
        assert "Fatal error" in caplog.text
