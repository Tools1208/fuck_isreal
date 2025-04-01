#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from time import sleep

# ---== تهيئة البيئة ==---
ROOT_DIR = Path(__file__).resolve().parent
VENV_DIR = ROOT_DIR / "venv"
PYTHON = VENV_DIR / "bin" / "python"
PIP = VENV_DIR / "bin" / "pip"
REQUIREMENTS = ROOT_DIR / "requirements.txt"

def install_system_deps():
    """تثبيت الاعتمادات النظامية"""
    deps = ["figlet", "lolcat", "python3-venv"]
    missing = []
    for dep in deps:
        result = subprocess.run(
            ["dpkg", "-s", dep],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            missing.append(dep)
    
    if missing:
        print(f"\033[1;33m[!] Installing system packages: {', '.join(missing)}\033[0m")
        subprocess.run(
            ["sudo", "apt", "update"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        subprocess.run(
            ["sudo", "apt", "install", "-y"] + missing,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def create_virtualenv():
    """إنشاء البيئة الافتراضية"""
    if not VENV_DIR.exists():
        print("\033[1;33m[!] Creating virtual environment...\033[0m")
        subprocess.run(
            [sys.executable, "-m", "venv", VENV_DIR],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def install_python_deps():
    """تثبيت الاعتمادات البرمجية"""
    if REQUIREMENTS.exists():
        print("\033[1;33m[!] Installing Python dependencies...\033[0m")
        subprocess.run(
            [PIP, "install", "--no-warn-script-location", "-r", REQUIREMENTS],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    else:
        print(f"\033[1;31m[!] Requirements file {REQUIREMENTS} not found!\033[0m")
        sys.exit(1)

def check_environment():
    """التحقق من إعداد البيئة"""
    try:
        install_system_deps()
        create_virtualenv()
        install_python_deps()
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31m[!] Setup failed: {e}\033[0m")
        sys.exit(1)

def run_in_virtualenv():
    """إعادة التشغيل داخل البيئة الافتراضية"""
    args = [PYTHON, __file__] + sys.argv[1:]
    os.execv(PYTHON, args)

if __name__ == "__main__":
    # تحقق من البيئة عند التشغيل الأول
    if not os.getenv("VIRTUAL_ENV"):
        check_environment()
        run_in_virtualenv()
    else:
        # تشغيل التطبيق الرئيسي
        from app import main
        main()
