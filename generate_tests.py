import requests
import os
import sys
import logging
from requests.exceptions import RequestException, HTTPError
from typing import List, Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_changed_files() -> List[str]:
    """Retrieve list of changed files passed as command-line arguments."""
    return sys.argv[1].split(' ') if len(sys.argv) > 1 else []

def detect_language(file_name: str) -> str:
    """Detect programming language based on file extension."""
    if file_name.endswith('.py'):
        return 'Python'
    elif file_name.endswith('.js'):
        return 'JavaScript'
    elif file_name.endswith('.ts'):
        return 'TypeScript'
    elif file_name.endswith('.java'):
        return 'Java'
    elif file_name.endswith('.cpp'):
        return 'C++'
    elif file_name.endswith('.cs'):
        return 'C#'
    return 'Unknown'

def create_prompt(changed_files: List[str], language: str) -> Optional[str]:
    """Create a language-specific prompt for test generation based on changed files."""
    if not changed_files:
        logging.info("No changed files to generate tests for.")
        return None

    language_template = {
        'Python': "Please generate detailed Python unit tests for the following changes:\n",
        'JavaScript': "Please generate detailed JavaScript unit tests for the following changes:\n",
        'TypeScript': "Please generate detailed TypeScript unit tests for the following changes:\n",
        'Java': "Please generate detailed Java unit tests for the following changes:\n",
        'C++': "Please generate detailed C++ unit tests for the following changes:\n",
        'C#': "Please generate detailed C# unit tests for the following changes:\n"
    }

    changes_summary = '\n'.join(f"- {file}" for file in changed_files)
    prompt = language_template.get(language, "Please generate unit tests for the following code changes:\n") + changes_summary
    logging.info(f"Created prompt for {language}. Length: {len(prompt)} characters")
    return prompt

def call_openai_api(prompt: str) -> Optional[Dict[str, Any]]:
    """Call OpenAI API to generate test cases based on the prompt with retry mechanism."""
    api_key = os.getenv('OPENAI_API_KEY')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': os.getenv('OPENAI_MODEL', 'gpt-4'),
        'prompt': prompt,
        'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
    }

    try:
        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        logging.error(f"Request failed: {req_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
    return None

def main():
    changed_files = get_changed_files()
    if not changed_files:
        logging.info("No files changed.")
        return

    language = detect_language(' '.join(changed_files))
    prompt = create_prompt(changed_files, language)
    if prompt:
        response = call_openai_api(prompt)
        if response and 'choices' in response and response['choices']:
            test_cases = response['choices'][0]['text']
            print(f"Generated Test Cases for {changed_files}:\n{test_cases}")
        else:
            logging.error("Failed to generate test cases or empty response from API.")
    else:
        logging.info("No prompt generated for the files.")

if __name__ == '__main__':
    main()
