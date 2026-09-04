"""
EchoCrew Setup Script 🚀
Automated environment initialization and virtual environment check.
"""

import os
import sys
import shutil
import subprocess

def run_setup():
    print("==========================================")
    print("       EchoCrew Environment Setup         ")
    print("==========================================")

    # 1. Environment file check
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(root_dir, ".env")
    env_example = os.path.join(root_dir, ".env.example")

    if not os.path.exists(env_file) and os.path.exists(env_example):
        shutil.copyfile(env_example, env_file)
        print("[+] Created .env file from .env.example template.")
    elif os.path.exists(env_file):
        print("[✓] .env file already exists.")

    # 2. Virtual environment verification
    venv_dir = os.path.join(root_dir, ".venv")
    if not os.path.exists(venv_dir):
        print("[!] Creating Python virtual environment in .venv...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        print("[✓] Virtual environment created successfully.")
    else:
        print("[✓] Virtual environment .venv exists.")

    print("\n[SUCCESS] Setup complete! Run 'pip install -r requirements-dev.txt' inside your environment.")

if __name__ == "__main__":
    run_setup()
