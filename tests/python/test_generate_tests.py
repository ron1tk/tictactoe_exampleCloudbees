```python
import pytest
from unittest.mock import patch, Mock
from generator import TestGenerator

@pytest.fixture
def test_generator():
    return TestGenerator()

@pytest.mark.parametrize("argv, expected_files", [
    ([], []),
    (["file1.py file2.py"], ["file1.py", "file2.py"]),
    ([""], []),
])
def test_get_changed_files(test_generator, argv, expected_files):
    import sys
    sys.argv = ["script_name"] + argv
    assert test_generator.get_changed_files() == expected_files

def test_detect_language(test_generator):
    assert test_generator.detect_language("file.py") == "Python"
    assert test_generator.detect_language("file.js") == "JavaScript"
    assert test_generator.detect_language("file.ts") == "TypeScript"
    assert test_generator.detect_language("file.java") == "Java"
    assert test_generator.detect_language("file.cpp") == "C++"
    assert test_generator.detect_language("file.cs") == "C#"
    assert test_generator.detect_language("file.unknown") == "Unknown"

def test_get_test_framework(test_generator):
    assert test_generator.get_test_framework("Python") == "pytest"
    assert test_generator.get_test_framework("JavaScript") == "jest"
    assert test_generator.get_test_framework("TypeScript") == "jest"
    assert test_generator.get_test_framework("Java") == "JUnit"
    assert test_generator.get_test_framework("C++") == "Google Test"
    assert test_generator.get_test_framework("C#") == "NUnit"
    assert test_generator.get_test_framework("Unknown") == "unknown"

@patch("builtins.open", return_value=Mock(__enter__=Mock(return_value=Mock(read=Mock(return_value="sample code")))))
def test_create_prompt(mock_open, test_generator):
    assert "Generate comprehensive unit tests" in test_generator.create_prompt("test.py", "Python")

@patch("requests.post")
def test_call_openai_api(mock_post, test_generator):
    mock_post.return_value.json.return_value = {'choices': [{'message': {'content': 'test cases'}}}
    assert test_generator.call_openai_api("prompt") == 'test cases'

@patch("logging.error")
def test_save_test_cases(mock_logging_error, test_generator, tmp_path):
    test_generator.save_test_cases(str(tmp_path / "test.py"), "test cases", "Python")
    assert (tmp_path / "tests/python/test_test.py").exists()

def test_run(test_generator, caplog):
    with caplog.at_level(logging.INFO):
        test_generator.run()
        assert "No files changed." in caplog.text
```