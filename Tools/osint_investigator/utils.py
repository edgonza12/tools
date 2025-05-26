import subprocess
import os

def run_sherlock(username):
    sherlock_path = os.path.join(os.path.dirname(__file__), 'sherlock/sherlock_project/sherlock.py')  # Actualiza esta ruta
    command = ['python3', sherlock_path, username, '--print-found']
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar Sherlock: {e.stderr}"