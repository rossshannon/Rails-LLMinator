import os
from tqdm import tqdm
import zipfile
from pathlib import Path

def get_repo_contents(repo_path):
    repo_contents = ""
    
    # Include everything under app/
    app_path = Path(repo_path) / "app"
    if app_path.exists():
        for file_path in app_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".rb", ".erb", ".haml", ".slim", ".yml", ".yaml", ".css", ".scss", ".sass", ".js", ".jsx"]:
                repo_contents += f"File: {file_path}\n"
    
    # Include everything under config/
    config_path = Path(repo_path) / "config"
    if config_path.exists():
        for file_path in config_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".rb", ".yml", ".yaml"]:
                repo_contents += f"File: {file_path}\n"
    
    # Include everything under lib/
    lib_path = Path(repo_path) / "lib"
    if lib_path.exists():
        for file_path in lib_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".rb"]:
                repo_contents += f"File: {file_path}\n"
    
    # Include everything under spec/
    spec_path = Path(repo_path) / "spec"
    if spec_path.exists():
        for file_path in spec_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".rb"]:
                repo_contents += f"File: {file_path}\n"
    
    # Include Gemfile and Gemfile.lock
    gemfile_path = Path(repo_path) / "Gemfile"
    if gemfile_path.exists():
        repo_contents += f"File: {gemfile_path}\n"
    
    gemfile_lock_path = Path(repo_path) / "Gemfile.lock"
    if gemfile_lock_path.exists():
        repo_contents += f"File: {gemfile_lock_path}\n"
    
    # Include package.json
    package_json_path = Path(repo_path) / "package.json"
    if package_json_path.exists():
        repo_contents += f"File: {package_json_path}\n"
    
    return repo_contents

def create_project_zip(project_path, zip_file_path):
    if os.path.exists(zip_file_path):
        print(f"Overwriting existing ZIP file: {zip_file_path}")
        os.remove(zip_file_path)
    print("Creating ZIP file...")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for directory in ["app", "config", "lib", "spec"]:
            directory_path = Path(project_path) / directory
            if directory_path.exists():
                for file_path in directory_path.rglob("*"):
                    if file_path.is_file() and file_path.suffix in [".rb", ".erb", ".haml", ".slim", ".yml", ".yaml", ".css", ".scss", ".sass", ".js", ".jsx"]:
                        zipf.write(file_path, file_path.relative_to(project_path))
        
        # Include Gemfile, Gemfile.lock, and package.json
        for file_name in ["Gemfile", "Gemfile.lock", "package.json"]:
            file_path = Path(project_path) / file_name
            if file_path.exists():
                zipf.write(file_path, file_path.relative_to(project_path))

def analyze_rails_project(project_path):
    print("Analyzing Ruby on Rails project...")

    # Analyze decorators
    decorators_path = Path(project_path) / "app" / "decorators"
    if decorators_path.exists():
        print("Decorators:")
        for decorator_file in decorators_path.glob("*.rb"):
            print(f"  - {decorator_file.name}")

    # Analyze helpers
    helpers_path = Path(project_path) / "app" / "helpers"
    if helpers_path.exists():
        print("Helpers:")
        for helper_file in helpers_path.glob("*.rb"):
            print(f"  - {helper_file.name}")

    # Analyze i18n files
    i18n_path = Path(project_path) / "config" / "locales"
    if i18n_path.exists():
        print("I18n files:")
        for i18n_file in i18n_path.glob("*.yml"):
            print(f"  - {i18n_file.name}")

    # Analyze spec files
    spec_path = Path(project_path) / "spec"
    if spec_path.exists():
        print("Spec files:")
        for spec_file in spec_path.rglob("*_spec.rb"):
            print(f"  - {spec_file.relative_to(spec_path)}")

    # Analyze Gemfile and Gemfile.lock
    gemfile_path = Path(project_path) / "Gemfile"
    if gemfile_path.exists():
        print("Gemfile:")
        with open(gemfile_path, "r") as gemfile:
            print(gemfile.read())
    
    gemfile_lock_path = Path(project_path) / "Gemfile.lock"
    if gemfile_lock_path.exists():
        print("Gemfile.lock:")
        with open(gemfile_lock_path, "r") as gemfile_lock:
            print(gemfile_lock.read())
    
    # Analyze package.json
    package_json_path = Path(project_path) / "package.json"
    if package_json_path.exists():
        print("package.json:")
        with open(package_json_path, "r") as package_json:
            print(package_json.read())

def process_project(project_path, create_zip=True):
    project_name = os.path.basename(project_path)
    print(f"Processing Ruby on Rails project: {project_name}\n")

    if create_zip:
        zip_file_path = f"{project_name}.zip"
        print(f"Creating ZIP file for: {project_name}")
        create_project_zip(project_path, zip_file_path)

    repo_contents = get_repo_contents(project_path)

    analyze_rails_project(project_path)

    instructions = f"Prompt: Analyze the {project_name} repository to understand its structure, purpose, and functionality. Follow these steps to study the Ruby on Rails codebase:\n\n"
    instructions += "1. Read the README file to gain an overview of the project, its goals, and any setup instructions.\n\n"
    instructions += "2. Examine the repository structure to understand how the files and directories are organized in a typical Ruby on Rails project.\n\n"  
    instructions += "3. Identify the main entry point of the application (typically config/routes.rb) and start analyzing the code flow from there.\n\n"
    instructions += "4. Study the Gemfile to understand the dependencies and libraries used in the project, including Ruby gems and other external tools.\n\n"
    instructions += "5. Analyze the core functionality of the project by examining the models, controllers, and views in the app directory.\n\n"
    instructions += "6. Look for configuration files (e.g., config/database.yml, config/application.rb) to understand how the project is configured and what settings are available.\n\n"
    instructions += "7. Investigate the test directory to see how the project ensures code quality and handles different scenarios using testing frameworks like RSpec or Minitest.\n\n"
    instructions += "8. Review any documentation or inline comments to gather insights into the codebase and its intended behavior.\n\n"
    instructions += "9. Identify any potential areas for improvement, optimization, or further exploration based on your analysis, considering Ruby on Rails best practices and conventions.\n\n"
    instructions += "10. Provide a summary of your findings, including the project's purpose, key features, and any notable observations or recommendations related to the Ruby on Rails implementation.\n\n"
    instructions += "Use the files and contents provided below to complete this analysis:\n\n"

    output_file = f"{project_name}_contents.txt"
    if os.path.exists(output_file):
        print(f"Overwriting existing output file: {output_file}")
        os.remove(output_file)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
            f.write('\n\n')
            f.write(repo_contents)
        print(f"Repository structure saved to '{output_file}'.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check the repository URL and try again.")

    print("Processing completed.")

if __name__ == "__main__":
    project_path = input("Please enter the path to the local Ruby on Rails project (or '.' for the current directory): ")

    if project_path == '.':
        project_path = os.getcwd()

    create_zip_input = input("Do you want to create a ZIP file of the project? (Y/N): ")
    create_zip = create_zip_input.lower() == 'y'

    if os.path.exists(project_path):
        process_project(project_path, create_zip)
    else:
        print("The specified project path does not exist.")
