import subprocess

def run_sherlock(username):
    try:
        command = [
            'python3',
            'osint_investigator/sherlock/sherlock_project/sherlock.py',  # Ajusta esta ruta si está en otro lado
            username,
            '--print-found',
            '--timeout', '20',
            '--no-color',
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=90
        )

        if result.returncode != 0 and not result.stdout.strip():
            return {
                "error": "❌ Sherlock devolvió error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            }

        # Procesar resultados desde stdout
        output_lines = result.stdout.splitlines()
        found_sites = []

        for line in output_lines:
            if line.startswith("[+]"):
                # Ejemplo de línea: [+] Twitter: https://twitter.com/edgonza12
                parts = line.split(":", 1)
                if len(parts) == 2:
                    platform = parts[0].replace("[+]", "").strip()
                    url = parts[1].strip()
                    found_sites.append({"platform": platform, "url": url})

        return {
            "success": True,
            "results": found_sites
        }

    except subprocess.TimeoutExpired:
        return {"error": "⏱ Tiempo de espera agotado al ejecutar Sherlock"}