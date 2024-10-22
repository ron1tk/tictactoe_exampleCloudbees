import requests
import os
import time
import logging
import sys
from requests.exceptions import RequestException
from typing import List, Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_changed_files() -> List[str]:
    """Retrieve list of changed files passed as command-line arguments."""
    if len(sys.argv) > 1:
        return sys.argv[1].split(' ')
    return []

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
    return 'Unknown'

def create_prompt(changed_files: List[str]) -> Optional[str]:
    """Create a prompt for test generation based on changed files."""
    if not changed_files:
        logging.info("No changed files to generate tests for.")
        return None
        
    changes_summary = '\n'.join(changed_files)
    prompt = f"Generate comprehensive test cases for the following code changes:\n{changes_summary}"
    logging.info(f"Created prompt. Length: {len(prompt)} characters")
    return prompt

def call_openai_api(prompt: str) -> Optional[Dict[str, Any]]:
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
        'model': 'gpt-4',
        'prompt': prompt,
        'max_tokens': 2000
    }
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    try:
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

def main():
    changed_files = get_changed_files()
    if not changed_files:
        logging.info("No files changed.")
        return

    for file_name in changed_files:
        language = detect_language(file_name)
        prompt = create_prompt([file_name])
        if prompt:
            response = call_openai_api(prompt)
            if response and 'choices' in response and response['choices']:
                test_cases = response['choices'][0]['text']
                print(f"Generated Test Cases for {file_name}:\n{test_cases}")
            else:
                logging.error("Failed to generate test cases or empty response from API.")
        else:
            logging.info("No prompt generated for file: " + file_name)

if __name__ == '__main__':
    main()
