import os
import sys
import subprocess
from pathlib import Path

VENV_DIR = Path(".venv")

def run(cmd, **kwargs):
    print(f"→ {cmd}")
    subprocess.run(cmd, shell=True, check=True, **kwargs)

def create_venv():
    if not VENV_DIR.exists():
        print("🔧 Creating virtual environment...")
        run(f"{sys.executable} -m venv {VENV_DIR}")
    else:
        print("✅ Virtual environment already exists.")

def install_deps():
    print("📦 Installing dependencies...")
    pip_path = VENV_DIR / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
    run(f"{pip_path} install -r requirements.txt")

def run_app():
    print("🚀 Running app...")
    python_path = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run(f"{python_path} src/main.py")

def update_deps():
    print("🔄 Updating dependencies...")
    pip_path = VENV_DIR / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
    run(f"{pip_path} install --upgrade -r requirements.txt")


def clean():
    print("🧹 Cleaning up...")
    if VENV_DIR.exists():
        if os.name == "nt":
            run(f"rmdir /s /q {VENV_DIR}")
        else:
            run(f"rm -rf {VENV_DIR}")
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                run(f"rm -rf {os.path.join(root, d)}")


def activate_shell():
    """Open an interactive shell inside the venv."""
    print("🐚 Activating virtual environment shell...")
    if os.name == "nt":
        # On Windows, prefer PowerShell if available
        ps1_path = VENV_DIR / "Scripts" / "Activate.ps1"
        bat_path = VENV_DIR / "Scripts" / "activate.bat"
        if ps1_path.exists():
            run(f'powershell -NoExit -Command "& {{ . \'{ps1_path}\' }}"')
        elif bat_path.exists():
            run(f'cmd /k "{bat_path}"')
        else:
            print("❌ Activation script not found.")
    else:
        # Linux/macOS
        activate_script = VENV_DIR / "bin" / "activate"
        run(f'bash --rcfile <(echo "source {activate_script}")', executable="/bin/bash")


if __name__ == "__main__":
    actions = {
        "setup": lambda: (create_venv(), install_deps()),
        "run": run_app,
        "clean": clean,
        "shell": activate_shell,
        "update": update_deps,
        }

    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        print("Usage: python manage.py [setup|run|clean|shell|update]")
        sys.exit(1)

    actions[sys.argv[1]]()
# Usage: python manage.py [setup|run|clean|shell|update]