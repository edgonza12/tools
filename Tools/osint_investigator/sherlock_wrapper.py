import subprocess
import os
import tempfile

def search_username(username):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        output_file = temp_file.name

    try:
        result = subprocess.run(
            ['python3', 'sherlock/sherlock_project/sherlock.py', username, '--print-found', '--timeout', '5', '--output', output_file],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Sherlock execution failed: {result.stderr}")

        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        results = [line.strip() for line in lines if username in line]
        return results

    finally:
        os.remove(output_file)