import os
from tqdm import tqdm
import zipfile
import mimetypes

def is_hidden(path):
    return os.path.basename(path).startswith('.')

def is_local_yml(path):
    return path.endswith('.local.yml')

def is_binary_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and not mime_type.startswith('text/')

def get_repo_contents(repo_path):
    repo_contents = ""
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not is_hidden(d)]  # Ignore hidden directories
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path) and not is_binary_file(file_path) and not is_hidden(file_path) and not is_local_yml(file_path):  # Skip symbolic links, binary files, hidden files, and .local.yml files
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

def create_project_zip(project_path, zip_file_path):
    if os.path.exists(zip_file_path):
        print(f"Overwriting existing ZIP file: {zip_file_path}")
        os.remove(zip_file_path)
    file_list = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not is_hidden(d)]  # Ignore hidden directories
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path) and not is_binary_file(file_path) and not is_hidden(file_path) and not is_local_yml(file_path):  # Skip symbolic links, binary files, hidden files, and .local.yml files
                file_list.append((file_path, os.path.relpath(file_path, project_path)))
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path, file_name in tqdm(file_list, desc="Creating ZIP file", unit="file"):
            zipf.write(file_path, file_name)

def analyze_rails_project(project_path):
    print("Analyzing Ruby on Rails project...")

    # Analyze controllers
    controllers_path = os.path.join(project_path, "app", "controllers")
    if os.path.exists(controllers_path):
        print("Controllers:")
        for controller_file in os.listdir(controllers_path):
            if controller_file.endswith(".rb") and not is_hidden(controller_file) and not is_local_yml(controller_file):
                print(f"  - {controller_file}")

    # Analyze routes
    routes_path = os.path.join(project_path, "config", "routes.rb")
    if os.path.exists(routes_path) and not is_hidden(routes_path) and not is_local_yml(routes_path):
        print("Routes:")
        with open(routes_path, "r") as routes_file:
            routes_content = routes_file.read()
            print(routes_content)

    # Analyze models
    models_path = os.path.join(project_path, "app", "models")
    if os.path.exists(models_path):
        print("Models:")
        for model_file in os.listdir(models_path):
            if model_file.endswith(".rb") and not is_hidden(model_file) and not is_local_yml(model_file):
                print(f"  - {model_file}")

    # Analyze views
    views_path = os.path.join(project_path, "app", "views")
    if os.path.exists(views_path):
        print("Views:")
        for root, dirs, files in os.walk(views_path):
            dirs[:] = [d for d in dirs if not is_hidden(d)]  # Ignore hidden directories
            for file in files:
                if file.endswith((".html.erb", ".html.haml", ".html.slim")) and not is_hidden(file) and not is_local_yml(file):
                    print(f"  - {os.path.relpath(os.path.join(root, file), views_path)}")

def process_project(project_path):
    project_name = os.path.basename(project_path)
    print(f"Processing Ruby on Rails project: {project_name}\n")

    zip_file_path = f"{project_name}.zip"
    print(f"Creating ZIP file for: {project_name}")
    create_project_zip(project_path, zip_file_path)

    repo_contents = get_repo_contents(project_path)

    output_file = f"{project_name}_contents.txt"
    if os.path.exists(output_file):
        print(f"Overwriting existing output file: {output_file}")
        os.remove(output_file)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(repo_contents)

    print(f"\nRepository contents saved to: {output_file}")

    analyze_rails_project(project_path)

    print("Processing completed.")

if __name__ == "__main__":
    project_path = input("Please enter the path to the local Ruby on Rails project (or '.' for the current directory): ")

    if project_path == '.':
        project_path = os.getcwd()

    if os.path.exists(project_path):
        process_project(project_path)
    else:
        print("The specified project path does not exist.")
