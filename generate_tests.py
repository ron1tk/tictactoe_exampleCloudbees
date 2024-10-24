import requests
import os
import sys
import logging
from requests.exceptions import RequestException
from typing import List, Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_changed_files() -> List[str]:
    """Retrieve list of changed files passed as command-line arguments."""
    return sys.argv[1].split(' ') if len(sys.argv) > 1 else []

def detect_language(file_name: str) -> str:
    """Detect programming language based on file extension."""
    extensions = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.cs': 'C#'
    }
    _, ext = os.path.splitext(file_name)
    return extensions.get(ext, 'Unknown')

def create_prompt(file_name: str, language: str) -> Optional[str]:
    """Create a language-specific prompt for test generation based on a changed file."""
    if not file_name:
        logging.info("No changed file to generate tests for.")
        return None

    # Read the content of the changed file
    try:
        with open(file_name, 'r') as f:
            code_content = f.read()
    except Exception as e:
        logging.error(f"Error reading file {file_name}: {e}")
        return None

    language_template = {
        'Python': "Please generate detailed Python unit tests for the following code:\n",
        'JavaScript': "Please generate detailed JavaScript unit tests for the following code:\n",
        'TypeScript': "Please generate detailed TypeScript unit tests for the following code:\n",
        'Java': "Please generate detailed Java unit tests for the following code:\n",
        'C++': "Please generate detailed C++ unit tests for the following code:\n",
        'C#': "Please generate detailed C# unit tests for the following code:\n"
    }

    prompt = language_template.get(language, "Please generate unit tests for the following code:\n") + code_content
    logging.info(f"Created prompt for {language}. Length: {len(prompt)} characters")
    return prompt

def call_openai_api(prompt: str) -> Optional[str]:
    """Call OpenAI API to generate test cases based on the prompt."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logging.error("OPENAI_API_KEY environment variable is not set")
        sys.exit("OPENAI_API_KEY environment variable is not set")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),  # Default to gpt-3.5-turbo
        'messages': [
            {"role": "system", "content": "You are a helpful assistant that generates code tests."},
            {"role": "user", "content": prompt}
        ],
        'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
    }

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        # Extract the generated content
        return response.json()['choices'][0]['message']['content']
    except RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

def save_test_cases(file_name: str, test_cases: str):
    """Save generated test cases to a new file."""
    base_name = os.path.basename(file_name)
    name, ext = os.path.splitext(base_name)
    output_file = f"test_{name}{ext}"
    with open(output_file, 'w') as f:
        f.write(test_cases)
    logging.info(f"Test cases saved to {output_file}")

def main():
    changed_files = get_changed_files()
    if not changed_files:
        logging.info("No files changed.")
        return

    for file_name in changed_files:
        language = detect_language(file_name)
        prompt = create_prompt(file_name, language)
        if prompt:
            test_cases = call_openai_api(prompt)
            if test_cases:
                print(f"Generated Test Cases for {file_name}:\n{test_cases}")
                # Save the test cases to a file
                save_test_cases(file_name, test_cases)
            else:
                logging.error("Failed to generate test cases or empty response from API.")
        else:
            logging.info(f"No prompt generated for file: {file_name}")

if __name__ == '__main__':
    main()
