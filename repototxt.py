import os
from tqdm import tqdm
import ast
import zipfile
import mimetypes

def is_binary_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and not mime_type.startswith('text/')

def get_repo_contents(repo_path):
    repo_contents = ""
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path) and not is_binary_file(file_path):  # Skip symbolic links and binary files
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
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                if not os.path.islink(file_path) and not is_binary_file(file_path):  # Skip symbolic links and binary files
                    zipf.write(file_path, os.path.relpath(file_path, project_path))

def parse_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)
    return ast.unparse(tree)

def process_project(project_path):
    project_name = os.path.basename(project_path)
    print(f"Analyzing Ruby on Rails project: {project_name}\n")
    
    zip_file_path = f"{project_name}.zip"
    print(f"Creating ZIP file for: {project_name}")
    create_project_zip(project_path, zip_file_path)
    
    repo_contents = get_repo_contents(project_path)
    
    python_files = [file for file in os.listdir(project_path) if file.endswith(".py")]
    for python_file in python_files:
        python_file_path = os.path.join(project_path, python_file)
        parsed_code = parse_python_file(python_file_path)
        repo_contents += f"File: {python_file_path}\nParsed Code:\n{parsed_code}\n\n"
    
    output_file = f"{project_name}_contents.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(repo_contents)
    
    print(f"\nRepository contents saved to: {output_file}")
    print("Analysis completed.")

if __name__ == "__main__":
    project_path = input("Please enter the path to the local Ruby on Rails project (or '.' for the current directory): ")
    
    if project_path == '.':
        project_path = os.getcwd()
    
    if os.path.exists(project_path):
        process_project(project_path)
    else:
        print("The specified project path does not exist.")
