import os
import glob
import subprocess
import sys
from typing import Tuple


def run_specific_agent(task: str) -> Tuple[str, int]:
    # Construct the command
    command = ['python', 'main_no_modal.py', task]
    subprocess.run(command, text=True)

def execute_generated_files():
    # Navigate to generated directory
    os.chdir('generated')

    # Iterate over every .txt file in the directory
    for file_name in glob.glob('*.txt'):
        with open(file_name, 'r') as file:
            python_code = file.read()
            python_code = python_code.replace('```python', '')
            python_code = python_code.replace('```', '')
            # Execute the code in the .txt file
            exec(python_code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <task>")
        sys.exit(1)
    task = sys.argv[1]
    run_specific_agent(task)
    execute_generated_files()
