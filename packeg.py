#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil

# Color codes for beautiful output
C = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
}

def color(text, col):
    return f"{col}{text}{C['reset']}"

def print_banner():
    print(color("\n" + "="*60, C['cyan']))
    print(color("  Instagram Brute‑Force Tool – Dependency Installer", C['bold'] + C['yellow']))
    print(color("  Author : THE SILENT HACKER RAJ", C['green']))
    print(color("="*60 + "\n", C['cyan']))

def run_cmd(cmd, description):
    """Run a shell command and print status."""
    print(color(f"[*] {description} ...", C['blue']), end=" ", flush=True)
    try:
        subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(color("✓", C['green']))
        return True
    except subprocess.CalledProcessError:
        print(color("✗", C['red']))
        return False

def install_pip_package(package):
    """Install a Python package using pip."""
    if run_cmd(f"{sys.executable} -m pip install {package} --quiet", f"Installing {package}"):
        print(color(f"   → {package} installed successfully.", C['green']))
        return True
    else:
        print(color(f"   → Failed to install {package}.", C['red']))
        return False

def is_pip_package_installed(package):
    """Check if a Python package is already installed."""
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        return False

def install_system_package(pkg_name, package_manager):
    """Install a system package using pkg (Termux) or apt (Linux)."""
    cmd = f"{package_manager} install {pkg_name} -y"
    if run_cmd(cmd, f"Installing system package: {pkg_name}"):
        print(color(f"   → {pkg_name} installed.", C['green']))
        return True
    return False

def main():
    print_banner()

    # 1. Ensure pip is available
    print(color("[*] Checking pip...", C['blue']))
    pip_available = shutil.which("pip") is not None
    if not pip_available:
        print(color("[!] pip not found. Installing pip...", C['yellow']))
        run_cmd(f"{sys.executable} -m ensurepip --upgrade", "Installing pip")
    
    # 2. Install Python packages
    python_packages = ["requests", "PySocks"]
    print(color("\n[*] Checking Python packages...", C['cyan']))
    for pkg in python_packages:
        if is_pip_package_installed(pkg):
            print(color(f"   → {pkg} already installed.", C['green']))
        else:
            install_pip_package(pkg)

    # 3. Install Tor system package
    print(color("\n[*] Checking Tor...", C['cyan']))
    tor_installed = shutil.which("tor") is not None
    if tor_installed:
        print(color("   → Tor already installed.", C['green']))
    else:
        # Detect package manager
        if shutil.which("pkg"):
            pm = "pkg"
        elif shutil.which("apt"):
            pm = "apt"
        else:
            print(color("   → No supported package manager found. Please install Tor manually.", C['red']))
            sys.exit(1)
        install_system_package("tor", pm)

    # 4. Install curl (often needed for testing)
    print(color("\n[*] Checking curl...", C['cyan']))
    if shutil.which("curl"):
        print(color("   → curl already installed.", C['green']))
    else:
        if shutil.which("pkg"):
            install_system_package("curl", "pkg")
        elif shutil.which("apt"):
            install_system_package("curl", "apt")
        else:
            print(color("   → curl not found. Please install curl manually.", C['red']))

    # Final summary
    print(color("\n" + "="*60, C['cyan']))
    print(color("  All dependencies have been processed!", C['bold'] + C['green']))
    print(color("  You can now run the main tool: python3 shr_cracker.py", C['yellow']))
    print(color("="*60 + "\n", C['cyan']))

if __name__ == "__main__":
    main()
