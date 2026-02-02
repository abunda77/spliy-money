#!/usr/bin/env python3
"""
Script untuk setup virtual environment dan install dependencies
"""

import os
import sys
import subprocess
import venv


def create_virtual_environment():
    """Buat virtual environment jika belum ada"""
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"Virtual environment sudah ada di {venv_path}")
        return venv_path
    
    print(f"Membuat virtual environment di {venv_path}...")
    venv.create(venv_path, with_pip=True)
    print("Virtual environment berhasil dibuat!")
    
    return venv_path


def get_pip_command(venv_path):
    """Dapatkan command pip untuk virtual environment"""
    if sys.platform == "win32":
        return os.path.join(venv_path, "Scripts", "pip")
    else:
        return os.path.join(venv_path, "bin", "pip")


def install_dependencies(venv_path):
    """Install dependencies dari requirements.txt"""
    pip_cmd = get_pip_command(venv_path)
    
    print("Menginstall dependencies...")
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("Dependencies berhasil diinstall!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    
    return True


def main():
    """Main function"""
    print("=== Money Splitter Environment Setup ===")
    
    # Create virtual environment
    venv_path = create_virtual_environment()
    
    # Install dependencies
    if install_dependencies(venv_path):
        print("\n=== Setup Berhasil! ===")
        print("Untuk mengaktifkan virtual environment:")
        if sys.platform == "win32":
            print(f"  {venv_path}\\Scripts\\activate")
        else:
            print(f"  source {venv_path}/bin/activate")
        print("\nUntuk menjalankan aplikasi:")
        print("  python main.py")
        print("\nUntuk menjalankan tests:")
        print("  pytest")
    else:
        print("\n=== Setup Gagal! ===")
        print("Silakan periksa error di atas dan coba lagi.")


if __name__ == "__main__":
    main()