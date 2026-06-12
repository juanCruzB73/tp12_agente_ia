import subprocess
import sys


def ejecutar_codigo(codigo: str) -> str:
    """Ejecuta un fragmento de código Python y devuelve el output o el error producido."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", codigo],
            capture_output=True,
            text=True,
            timeout=10,
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        if out and err:
            return f"{out}\nError:\n{err}"
        return out or err or "(sin output)"
    except subprocess.TimeoutExpired:
        return "Error: el código tardó más de 10 segundos y fue detenido."
    except Exception as e:
        return f"Error al ejecutar: {e}"
