import os
from tqdm import tqdm
import zipfile
import mimetypes
import fnmatch

def is_excluded(path, base_path, exclusion_patterns):
    rel_path = os.path.relpath(path, base_path)
    for pattern in exclusion_patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

def get_repo_contents(repo_path, exclusion_patterns):
    repo_contents = ""
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), repo_path, exclusion_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path) and not is_excluded(file_path, repo_path, exclusion_patterns):
                file_contents = get_file_contents(file_path)
                repo_contents += f"File: {file_path}\nContent:\n{file_contents}\n\n"
    return repo_contents

def get_file_contents(file_path):
    file_contents = ""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as file:
                file_contents = file.read()
        except UnicodeDecodeError:
            file_contents = "Error: Unable to decode file contents"
    return file_contents

def create_project_zip(project_path, zip_file_path, exclusion_patterns):
    if os.path.exists(zip_file_path):
        print(f"Overwriting existing ZIP file: {zip_file_path}")
        os.remove(zip_file_path)
    print("Parsing and counting files in the project...")
    file_list = []
    file_count = 0
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), project_path, exclusion_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path) and not is_excluded(file_path, project_path, exclusion_patterns):
                file_list.append((file_path, os.path.relpath(file_path, project_path)))
                file_count += 1
                print(f"Files counted: {file_count}", end="\r")
    print("\nCreating ZIP file...")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        with tqdm(total=len(file_list), desc="Adding files to ZIP", unit="file", ncols=100, leave=False) as pbar:
            for file_path, file_name in file_list:
                zipf.write(file_path, file_name)
                pbar.update(1)

def analyze_rails_project(project_path, exclusion_patterns):
    print("Analyzing Ruby on Rails project...")

    # Analyze controllers
    controllers_path = os.path.join(project_path, "app", "controllers")
    if os.path.exists(controllers_path):
        print("Controllers:")
        for controller_file in os.listdir(controllers_path):
            if controller_file.endswith(".rb") and not is_excluded(os.path.join(controllers_path, controller_file), project_path, exclusion_patterns):
                print(f"  - {controller_file}")

    # Analyze routes
    routes_path = os.path.join(project_path, "config", "routes.rb")
    if os.path.exists(routes_path) and not is_excluded(routes_path, project_path, exclusion_patterns):
        print("Routes:")
        with open(routes_path, "r") as routes_file:
            routes_content = routes_file.read()
            print(routes_content)

    # Analyze models
    models_path = os.path.join(project_path, "app", "models")
    if os.path.exists(models_path):
        print("Models:")
        for model_file in os.listdir(models_path):
            if model_file.endswith(".rb") and not is_excluded(os.path.join(models_path, model_file), project_path, exclusion_patterns):
                print(f"  - {model_file}")

    # Analyze views
    views_path = os.path.join(project_path, "app", "views")
    if os.path.exists(views_path):
        print("Views:")
        for root, dirs, files in os.walk(views_path):
            dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), project_path, exclusion_patterns)]
            for file in files:
                if file.endswith((".html.erb", ".html.haml", ".html.slim")) and not is_excluded(os.path.join(root, file), project_path, exclusion_patterns):
                    print(f"  - {os.path.relpath(os.path.join(root, file), views_path)}")

def process_project(project_path, exclusion_file):
    project_name = os.path.basename(project_path)
    print(f"Processing Ruby on Rails project: {project_name}\n")

    with open(exclusion_file, "r") as file:
        exclusion_patterns = [line.strip() for line in file.readlines()]

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

    if os.path.exists(project_path) and os.path.exists(exclusion_file):
        process_project(project_path, exclusion_file)
    else:
        print("The specified project path or exclusion file does not exist.")
