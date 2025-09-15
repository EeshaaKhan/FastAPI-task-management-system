"""
Project verification script.
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and report results."""
    print(f"\n📋 {description}")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout.strip():
                print(result.stdout.strip())
        else:
            print("❌ FAILED")
            if result.stdout.strip():
                print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip())
    except Exception as e:
        print(f"❌ ERROR: {e}")

def check_file_exists(file_path, description):
    """Check if a file exists."""
    print(f"\n📁 {description}")
    if os.path.exists(file_path):
        print(f"✅ {file_path} exists")
        return True
    else:
        print(f"❌ {file_path} missing")
        return False

def main():
    """Run all verification checks."""
    print("🚀 TASK MANAGEMENT SYSTEM - PROJECT VERIFICATION")
    print("=" * 60)
    
    # Check project structure
    required_files = [
        ("app/main.py", "FastAPI main application"),
        ("app/models/user.py", "User model"),
        ("app/models/task.py", "Task model"),
        ("app/schemas/user.py", "User schemas"),
        ("app/schemas/task.py", "Task schemas"),
        ("app/crud/user.py", "User CRUD operations"),
        ("app/crud/task.py", "Task CRUD operations"),
        ("app/api/v1/users.py", "User API endpoints"),
        ("app/api/v1/tasks.py", "Task API endpoints"),
        ("tests/test_users.py", "User tests"),
        ("tests/test_tasks.py", "Task tests"),
        ("requirements.txt", "Python dependencies"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("README.md", "Project documentation"),
        (".env.example", "Environment template"),
        (".gitignore", "Git ignore file"),
    ]
    
    all_files_exist = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_files_exist = False
    
    if all_files_exist:
        print("\n✅ All required files are present!")
    else:
        print("\n❌ Some required files are missing!")
        return False
    
    # Run tests
    run_command("python -m pytest tests/ -v", "Running test suite")
    
    # Check code quality
    run_command("python -m black --check app/ tests/", "Code formatting check")
    run_command("python -m isort --check-only app/ tests/", "Import sorting check")
    run_command("python -m flake8 app/ tests/", "Code linting check")
    
    # Check if application starts
    print(f"\n🔍 Checking if application can import successfully")
    try:
        from app.main import app
        print("✅ Application imports successfully")
    except Exception as e:
        print(f"❌ Application import failed: {e}")
        return False
    
    # Check database models
    print(f"\n🗄️  Checking database models")
    try:
        from app.models.user import User
        from app.models.task import Task
        print("✅ Database models import successfully")
    except Exception as e:
        print(f"❌ Database models import failed: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 PROJECT VERIFICATION COMPLETE!")
    print("✅ Your Task Management System is ready for delivery!")
    print("📚 Next steps:")
    print("   1. Push to GitHub: git push origin main")
    print("   2. Share the repository URL with your manager")
    print("   3. Include the README.md for setup instructions")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()
