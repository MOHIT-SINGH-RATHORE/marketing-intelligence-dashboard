#!/usr/bin/env python3
"""
Marketing Intelligence Dashboard Runner
This script provides an easy way to run the dashboard with different configurations
"""

import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    return True

def check_data_files():
    """Check if all required data files exist"""
    required_files = [
        'business.csv',
        'Facebook.csv',
        'Google.csv',
        'TikTok.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing data files: {', '.join(missing_files)}")
        print("Please ensure all CSV files are in the current directory")
        return False
    return True

def run_dashboard(port=8501, host="localhost"):
    """Run the Streamlit dashboard"""
    if not check_dependencies():
        sys.exit(1)
    
    if not check_data_files():
        sys.exit(1)
    
    print("Starting Marketing Intelligence Dashboard...")
    print(f"Dashboard will be available at: http://{host}:{port}")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "marketing_dashboard.py",
            "--server.port", str(port),
            "--server.address", host
        ])
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error running dashboard: {e}")

def main():
    """Main function to run the dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Marketing Intelligence Dashboard")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the dashboard on")
    parser.add_argument("--host", default="localhost", help="Host to run the dashboard on")
    parser.add_argument("--check-only", action="store_true", help="Only check dependencies and data files")
    
    args = parser.parse_args()
    
    if args.check_only:
        deps_ok = check_dependencies()
        data_ok = check_data_files()
        if deps_ok and data_ok:
            print("All dependencies and data files are ready!")
            sys.exit(0)
        else:
            sys.exit(1)
    
    run_dashboard(port=args.port, host=args.host)

if __name__ == "__main__":
    main()
