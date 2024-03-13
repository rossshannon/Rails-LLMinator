import os
from tqdm import tqdm
import zipfile
from pathlib import Path

def is_excluded(path, project_root, exclusion_patterns):
    relative_path = path.relative_to(project_root).as_posix()
    for pattern in exclusion_patterns:
        if relative_path.startswith(pattern):
            return True
    return False

def get_repo_contents(repo_path, exclusion_patterns):
    repo_contents = ""
    for file_path in Path(repo_path).rglob("*"):
        if file_path.is_file() and not file_path.is_symlink() and not is_excluded(file_path, repo_path, exclusion_patterns) and not file_path.name.startswith(".") and "node_modules" not in file_path.parts:
            repo_contents += f"File: {file_path}\n"
    return repo_contents

def create_project_zip(project_path, zip_file_path, exclusion_patterns):
    if os.path.exists(zip_file_path):
        print(f"Overwriting existing ZIP file: {zip_file_path}")
        os.remove(zip_file_path)
    print("Parsing and counting files in the project...")
    file_list = []
    file_count = 0
    with tqdm(total=len(list(Path(project_path).rglob("*"))), desc="Counting files", unit="file", ncols=100) as pbar:
        for file_path in Path(project_path).rglob("*"):
            if file_path.is_file() and not file_path.is_symlink() and not is_excluded(file_path, project_path, exclusion_patterns) and not file_path.name.startswith(".") and "node_modules" not in file_path.parts:
                file_list.append(file_path)
                file_count += 1
            pbar.update(1)
    print(f"\nFound {file_count:,} files.")
    print("Creating ZIP file...")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        with tqdm(total=len(file_list), desc="Adding files to ZIP", unit="file", ncols=100) as pbar:
            for file_path in file_list:
                zipf.write(file_path, file_path.relative_to(project_path))
                pbar.update(1)

def analyze_rails_project(project_path, exclusion_patterns):
    print("Analyzing Ruby on Rails project...")

    # Analyze controllers
    controllers_path = Path(project_path) / "app" / "controllers"
    if controllers_path.exists():
        print("Controllers:")
        for controller_file in controllers_path.glob("*.rb"):
            if not is_excluded(controller_file, project_path, exclusion_patterns):
                print(f"  - {controller_file.name}")

    # Analyze routes
    routes_path = Path(project_path) / "config" / "routes.rb"
    if routes_path.exists() and not is_excluded(routes_path, project_path, exclusion_patterns):
        print("Routes:")
        with open(routes_path, "r") as routes_file:
            routes_content = routes_file.read()
            print(routes_content)

    # Analyze models
    models_path = Path(project_path) / "app" / "models"
    if models_path.exists():
        print("Models:")
        for model_file in models_path.glob("*.rb"):
            if not is_excluded(model_file, project_path, exclusion_patterns):
                print(f"  - {model_file.name}")

    # Analyze views
    views_path = Path(project_path) / "app" / "views"
    if views_path.exists():
        print("Views:")
        for view_file in views_path.rglob("*"):
            if view_file.is_file() and view_file.suffix in [".html.erb", ".html.haml", ".html.slim"] and not is_excluded(view_file, project_path, exclusion_patterns):
                print(f"  - {view_file.relative_to(views_path)}")

def process_project(project_path, exclusion_file, create_zip=True):
    project_name = os.path.basename(project_path)
    print(f"Processing Ruby on Rails project: {project_name}\n")

    with open(exclusion_file, "r") as file:
        exclusion_patterns = [line.strip() for line in file.readlines()]

    if create_zip:
        zip_file_path = f"{project_name}.zip"
        print(f"Creating ZIP file for: {project_name}")
        create_project_zip(project_path, zip_file_path, exclusion_patterns)

    repo_contents = get_repo_contents(project_path, exclusion_patterns)

    output_file = f"{project_name}_contents.txt"
    if os.path.exists(output_file):
        print(f"Overwriting existing output file: {output_file}")
        os.remove(output_file)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(repo_contents)

    print(f"\nRepository contents saved to: {output_file}")

    analyze_rails_project(project_path, exclusion_patterns)

    print("Processing completed.")

if __name__ == "__main__":
    exclusion_file = "file-exclusions.txt"
    project_path = input("Please enter the path to the local Ruby on Rails project (or '.' for the current directory): ")

    if project_path == '.':
        project_path = os.getcwd()

    create_zip_input = input("Do you want to create a ZIP file of the project? (Y/N): ")
    create_zip = create_zip_input.lower() == 'y'

    if os.path.exists(project_path) and os.path.exists(exclusion_file):
        process_project(project_path, exclusion_file, create_zip)
    else:
        print("The specified project path or exclusion file does not exist.")
