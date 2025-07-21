import os
from pathlib import Path

# Define base project directory (current directory in this case)
BASE_DIR = Path.cwd()

# Define folders to create
folders = [
    BASE_DIR / ".vscode",
    BASE_DIR / ".github" / "workflows",
    BASE_DIR / "src",
    BASE_DIR / "notebooks",
    BASE_DIR / "tests",
    BASE_DIR / "scripts"
]

# Define files to create with their full paths
files = {
    BASE_DIR / ".vscode" / "settings.json": "",
    BASE_DIR / ".github" / "workflows" / "unittests.yml": "",
    BASE_DIR / ".gitignore": "",
    BASE_DIR / "requirements.txt": "",
    BASE_DIR / "README.md": "",
    BASE_DIR / "notebooks" / "__init__.py": "",
    BASE_DIR / "notebooks" / "README.md": "",
    BASE_DIR / "tests" / "__init__.py": "",
    BASE_DIR / "scripts" / "__init__.py": "",
    BASE_DIR / "scripts" / "README.md": ""
}

# Create folders
for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)

# Create files
for file_path, content in files.items():
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directories exist
    with open(file_path, 'w') as f:
        f.write(content)

print("Folder structure created successfully.")
