import subprocess
import os

def search_username(username):
    sherlock_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sherlock/sherlock'))
    
    try:
        result = subprocess.run(
            ['python3', sherlock_path, username, '--print-found'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "La búsqueda ha tardado demasiado tiempo."
    except Exception as e:
        return f"Error: {str(e)}"