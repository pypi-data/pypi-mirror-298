import subprocess
import sys
import argparse
import os
import json
import threading
import time
import itertools

#External dependencies
import requests

SERVER_ENDPOINT = "https://promptiva.app"
PROMPTIVA_INFO = """
Environment Variables:
  PROMPTIVA_API_KEY: Your Promptiva API key

To set your API key, use:
  export PROMPTIVA_API_KEY=your_api_key_here

Visit https://promptiva.app/settings to obtain your API key.
\n\n
"""

class Spinner:
    def __init__(self):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.running = False
        self.spinner_thread = None

    def spin(self):
        sys.stdout.write('\n')
        while self.running:
            sys.stdout.write(f"\rGenerating your prompt {next(self.spinner)}\r")
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self):
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write('\r' + ' ' * 30 + '\r')  # Clear the spinner line
        sys.stdout.flush()
        sys.stdout.write('\n')


def validate_prompt(prompt):
    if not prompt or prompt.strip() == "":
        print("Error: Prompt cannot be empty.")
        sys.exit(1)

def make_api_request(prompt, api_key):
    api_url = SERVER_ENDPOINT + "/api/cli/generate"

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        if response.status_code == 400:
            error_data = response.json()
            print(f"API Error: {error_data.get('error', 'Unknown error')}")
        elif response.status_code == 401:
            error_data = response.json()
            print(f"API Error: {error_data.get('error', 'Unknown error')}")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Error decoding JSON response from the server")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    
def run_command(prompt):
    api_key = os.environ.get('PROMPTIVA_API_KEY')
    if not api_key:
        print("""Error: PROMPTIVA_API_KEY environment variable is not set. \n
              If you dont have the API key, you can get it from https://promptiva.app/settings""")
        sys.exit(1)
    
    validate_prompt(prompt)

    spinner = Spinner()
    spinner.start()

    try:
        result = make_api_request(prompt, api_key)
    finally:
        spinner.stop()

    # Print the result
    if not result:
        sys.exit(1)
    
    print(json.dumps(result, indent=2))

def main():
    # parser = argparse.ArgumentParser(description="Run Promptiva cli")
    parser = argparse.ArgumentParser(
        description="Promptiva CLI - Optimize your prompts using AI",
        epilog=PROMPTIVA_INFO,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-p', '--prompt', required=True, help='The text prompt to optimize')
    args = parser.parse_args()

    run_command(args.prompt)

if __name__ == "__main__":
    main()