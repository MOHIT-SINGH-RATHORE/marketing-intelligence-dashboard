#!/usr/bin/env python3
"""
GitHub Setup Helper Script
This script helps you prepare your project for GitHub deployment
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e.stderr}")
        return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        'marketing_dashboard.py',
        'advanced_analysis.py', 
        'requirements.txt',
        'README.md',
        'Business.csv',
        'Facebook.csv',
        'Google.csv',
        'TikTok.csv'
    ]
    
    print("📋 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        print("Please ensure all CSV files and Python files are in the current directory.")
        return False
    
    print("\n✅ All required files present!")
    return True

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local

# Streamlit
.streamlit/

# Data files (optional - remove if you want to include CSVs)
# *.csv
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore file")

def setup_git():
    """Initialize git repository"""
    commands = [
        ("git init", "Initializing git repository"),
        ("git add .", "Adding all files to git"),
        ("git commit -m 'Initial commit: Marketing Intelligence Dashboard'", "Creating initial commit")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Marketing Intelligence Dashboard - GitHub Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('marketing_dashboard.py'):
        print("❌ Please run this script from the project directory containing marketing_dashboard.py")
        sys.exit(1)
    
    # Step 1: Check files
    if not check_files():
        print("\n❌ Setup failed: Missing required files")
        sys.exit(1)
    
    # Step 2: Create .gitignore
    create_gitignore()
    
    # Step 3: Setup git
    if not setup_git():
        print("\n❌ Git setup failed")
        sys.exit(1)
    
    print("\n🎉 GitHub setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Go to GitHub.com and create a new repository")
    print("2. Copy the repository URL")
    print("3. Run these commands:")
    print("   git remote add origin YOUR_REPOSITORY_URL")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n4. Deploy to Streamlit Cloud:")
    print("   - Go to share.streamlit.io")
    print("   - Connect your GitHub repository")
    print("   - Deploy your dashboard")
    
    print(f"\n📁 Current directory: {os.getcwd()}")
    print("✅ Ready for GitHub deployment!")

if __name__ == "__main__":
    main()
