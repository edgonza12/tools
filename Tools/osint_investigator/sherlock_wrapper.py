import subprocess
import json
import os
from pathlib import Path

def run_sherlock(username):
    sherlock_path = Path(__file__).resolve().parent / 'sherlock' / 'sherlock.py'
    output_file = Path(__file__).resolve().parent / 'results' / f'{username}.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    command = [
        'python3', str(sherlock_path),
        username,
        '--print-found',
        '--timeout', '15',
        '--json',
        '--output', str(output_file)
    ]

    try:
        subprocess.run(command, check=True)
        with open(output_file, 'r') as f:
            data = json.load(f)
        return data.get(username, {})
    except Exception as e:
        return {'error': str(e)}