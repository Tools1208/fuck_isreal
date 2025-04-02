#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from shutil import which

# ---== Configuration ==---
ROOT_DIR = Path(__file__).resolve().parent
VENV_DIR = ROOT_DIR / ".venv"
REQUIREMENTS = ROOT_DIR / "requirements.txt"
SYSTEM_DEPS = ["figlet", "lolcat", "python3-venv"]

def check_system_deps():
    """Check and install system dependencies"""
    missing = [dep for dep in SYSTEM_DEPS if not which(dep)]
    if missing:
        print(f"\033[1;33m[!] Installing missing system packages: {', '.join(missing)}\033[0m")
        try:
            subprocess.run(
                ["sudo", "apt", "update"],
                check=True
            )
            subprocess.run(
                ["sudo", "apt", "install", "-y"] + missing,
                check=True
            )
        except subprocess.CalledProcessError as e:
            sys.exit(f"\033[1;31m[!] Failed to install system dependencies: {e}\033[0m")

def setup_virtualenv():
    """Create and configure virtual environment"""
    if not VENV_DIR.exists():
        print("\033[1;33m[!] Creating virtual environment...\033[0m")
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", VENV_DIR],
                check=True
            )
        except subprocess.CalledProcessError as e:
            sys.exit(f"\033[1;31m[!] Virtualenv creation failed: {e}\033[0m")

def install_python_deps():
    """Install Python dependencies from requirements.txt"""
    if not REQUIREMENTS.exists():
        sys.exit(f"\033[1;31m[!] Requirements file {REQUIREMENTS} not found!\033[0m")
        
    print("\033[1;33m[!] Installing Python dependencies...\033[0m")
    try:
        subprocess.run(
            [str(VENV_DIR / "bin" / "pip"), "install", "-r", str(REQUIREMENTS)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"\033[1;31m[!] Dependency installation failed: {e}\033[0m")

def initialize_environment():
    """Full environment setup process"""
    check_system_deps()
    setup_virtualenv()
    install_python_deps()

def run_application():
    """Execute the main application within the virtual environment"""
    try:
        # Reactivate virtualenv and run main script
        env = os.environ.copy()
        env["PATH"] = f"{VENV_DIR / 'bin'}:{env['PATH']}"
        subprocess.run(
            [str(VENV_DIR / "bin" / "python"), "-m", "main"],
            env=env,
            check=True
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"\033[1;31m[!] Application execution failed: {e}\033[0m")

if __name__ == "__main__":
    # Check if running in virtual environment
    if not os.getenv("VIRTUAL_ENV"):
        initialize_environment()
    
    # Run the application
    run_application()
