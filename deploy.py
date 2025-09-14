#!/usr/bin/env python3
"""
Deployment script for Marketing Intelligence Dashboard
Supports multiple deployment options
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def create_dockerfile():
    """Create Dockerfile for containerized deployment"""
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "marketing_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    print("✅ Dockerfile created")

def create_docker_compose():
    """Create docker-compose.yml for easy deployment"""
    compose_content = """version: '3.8'

services:
  marketing-dashboard:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(compose_content)
    print("✅ docker-compose.yml created")

def create_heroku_files():
    """Create files needed for Heroku deployment"""
    # Procfile
    with open('Procfile', 'w') as f:
        f.write('web: streamlit run marketing_dashboard.py --server.port=$PORT --server.address=0.0.0.0')
    print("✅ Procfile created")
    
    # runtime.txt
    with open('runtime.txt', 'w') as f:
        f.write('python-3.9.18')
    print("✅ runtime.txt created")

def create_streamlit_config():
    """Create Streamlit configuration file"""
    config_dir = Path.home() / '.streamlit'
    config_dir.mkdir(exist_ok=True)
    
    config_content = """[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
    
    config_file = config_dir / 'config.toml'
    with open(config_file, 'w') as f:
        f.write(config_content)
    print("✅ Streamlit config created")

def create_github_workflow():
    """Create GitHub Actions workflow for automated deployment"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Deploy Marketing Dashboard

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
        python -c "import pandas; print('Pandas version:', pandas.__version__)"
        python -c "import plotly; print('Plotly version:', plotly.__version__)"
    
    - name: Deploy to Streamlit Cloud
      uses: streamlit/streamlit-cloud-action@v1
      with:
        streamlit-cloud-url: ${{ secrets.STREAMLIT_CLOUD_URL }}
        streamlit-cloud-token: ${{ secrets.STREAMLIT_CLOUD_TOKEN }}
"""
    
    workflow_file = workflow_dir / 'deploy.yml'
    with open(workflow_file, 'w') as f:
        f.write(workflow_content)
    print("✅ GitHub workflow created")

def create_vercel_config():
    """Create Vercel configuration for deployment"""
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "marketing_dashboard.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "marketing_dashboard.py"
            }
        ]
    }
    
    with open('vercel.json', 'w') as f:
        json.dump(vercel_config, f, indent=2)
    print("✅ Vercel config created")

def main():
    """Main deployment setup function"""
    print("🚀 Setting up Marketing Intelligence Dashboard for deployment...")
    
    # Create deployment files
    create_dockerfile()
    create_docker_compose()
    create_heroku_files()
    create_streamlit_config()
    create_github_workflow()
    create_vercel_config()
    
    print("\n✅ All deployment files created!")
    print("\n📋 Deployment Options:")
    print("1. Local: python run_dashboard.py")
    print("2. Docker: docker-compose up")
    print("3. Heroku: git push heroku main")
    print("4. Streamlit Cloud: Connect GitHub repository")
    print("5. Vercel: vercel --prod")
    
    print("\n🔧 Next Steps:")
    print("1. Ensure all CSV files are in the project directory")
    print("2. Test locally: python run_dashboard.py")
    print("3. Choose your deployment method")
    print("4. Follow the specific deployment instructions")

if __name__ == "__main__":
    main()
