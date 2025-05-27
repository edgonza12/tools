import subprocess
import tempfile
import json
import os

def run_sherlock(username):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmpfile:
        output_file = tmpfile.name

    try:
        # Ejecutar Sherlock
        result = subprocess.run(
            ['python3', 'osint_investigator/sherlock/sherlock_project/sherlock.py', username, '--json', output_file],
            capture_output=True,
            text=True,
            timeout=90  # tiempo máximo de espera
        )

        if result.returncode != 0:
            return {
                "error": "Error al ejecutar Sherlock",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            }

        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        found = data.get(username, {}).get("accounts", {})

        return {"results": {site: acc.get("url", "") for site, acc in found.items()}}

    except subprocess.TimeoutExpired:
        return {"error": "Tiempo de espera agotado al ejecutar Sherlock"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)