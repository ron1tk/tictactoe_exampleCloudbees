import requests
import os
import sys
import logging
import json
from pathlib import Path
from requests.exceptions import RequestException
from typing import List, Optional, Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TestGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

    def get_changed_files(self) -> List[str]:
        """Retrieve list of changed files passed as command-line arguments."""
        if len(sys.argv) <= 1:
            return []
        return [f.strip() for f in sys.argv[1].split() if f.strip()]

    def detect_language(self, file_name: str) -> str:
        """Detect programming language based on file extension."""
        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp':'C++',
            '.cs': 'C#'
        }
        _, ext = os.path.splitext(file_name)
        return extensions.get(ext.lower(), 'Unknown')

    def get_test_framework(self, language: str) -> str:
        """Get the appropriate test framework based on language."""
        frameworks = {
            'Python': 'pytest',
            'JavaScript': 'jest',
            'TypeScript': 'jest',
            'Java': 'JUnit',
            'C++': 'Google Test',
            'C#': 'NUnit'
        }
        return frameworks.get(language, 'unknown')

    def create_prompt(self, file_name: str, language: str) -> Optional[str]:
        """Create a language-specific prompt for test generation."""
        try:
            with open(file_name, 'r') as f:
                code_content = f.read()
        except Exception as e:
            logging.error(f"Error reading file {file_name}: {e}")
            return None

        framework = self.get_test_framework(language)
        
        prompt = f"""Generate comprehensive unit tests for the following {language} code using {framework}.

Requirements:
1. Include edge cases, normal cases, and error cases
2. Use mocking where appropriate for external dependencies
3. Include setup and teardown if needed
4. Add descriptive test names and docstrings
5. Follow {framework} best practices
6. Ensure high code coverage
7. Test both success and failure scenarios

Code to test:

{code_content}

Generate only the test code without any explanations."""

        logging.info(f"Created prompt for {language} using {framework}. Length: {len(prompt)} characters")
        return prompt

    def call_openai_api(self, prompt: str) -> Optional[str]:
        """Call OpenAI API to generate test cases."""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {"role": "system", "content": "You are a senior software engineer specialized in writing comprehensive test suites."},
                {"role": "user", "content": prompt}
            ],
            'max_tokens': self.max_tokens,
            'temperature': 0.7  # Balance between creativity and consistency
        }

        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            generated_text = response.json()['choices'][0]['message']['content']
            # Replace curly quotes with straight quotes
            normalized_text = generated_text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
            return normalized_text
        except RequestException as e:
            logging.error(f"API request failed: {e}")
            return None


    def save_test_cases(self, file_name: str, test_cases: str, language: str):
        """Save generated test cases to appropriate directory structure."""
        # Create tests directory if it doesn't exist
        tests_dir = Path('tests')
        tests_dir.mkdir(exist_ok=True)

        # Create language-specific subdirectory
        lang_dir = tests_dir / language.lower()
        lang_dir.mkdir(exist_ok=True)

        # Generate test file name
        base_name = Path(file_name).stem
        extension = '.py' if language == 'Python' else Path(file_name).suffix
        test_file = lang_dir / f"test_{base_name}{extension}"

        try:
            with open(test_file, 'w', encodings='utf-8') as f:
                f.write(test_cases)
            logging.info(f"Test cases saved to {test_file}")
        except Exception as e:
            logging.error(f"Error saving test cases to {test_file}: {e}")

    def run(self):
        """Main execution method."""
        changed_files = self.get_changed_files()
        if not changed_files:
            logging.info("No files changed.")
            return

        for file_name in changed_files:
            try:
                language = self.detect_language(file_name)
                if language == 'Unknown':
                    logging.warning(f"Unsupported file type: {file_name}")
                    continue

                logging.info(f"Processing {file_name} ({language})")
                prompt = self.create_prompt(file_name, language)
                
                if prompt:
                    # Generate test cases from the API
                    test_cases = self.call_openai_api(prompt)
                    
                    # Clean up quotation marks if test cases were generated
                    if test_cases:
                        test_cases = test_cases.replace("“", '"').replace("”", '"')
                        self.save_test_cases(file_name, test_cases, language)
                    else:
                        logging.error(f"Failed to generate test cases for {file_name}")
            except Exception as e:
                logging.error(f"Error processing {file_name}: {e}")


if __name__ == '__main__':
    try:
        generator = TestGenerator()
        generator.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)