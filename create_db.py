import subprocess
import sys


subprocess.run(
    [sys.executable, "-m", "flask", "--app", "run.py", "db", "upgrade"],
    check=True,
)

print("Migracoes aplicadas com sucesso")
