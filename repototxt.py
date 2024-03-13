import os
import git
from tqdm import tqdm
import rubyparser
import zipfile

def clone_local_repo(repo_path):
    """
    Clone or access the local Git repository.
    """
    repo = git.Repo(repo_path)
    return repo

def analyze_rails_project(repo_path):
    """
    Analyze the Ruby on Rails project.
    """
    summary = {}

    # Extract information from controllers, models, views, routes, etc.
    # ...

    # Extract gem dependencies and versions
    # ...

    return summary

def create_project_zip(repo_path, output_path):
    """
    Create a ZIP file containing the relevant project files.
    """
    with zipfile.ZipFile(output_path, 'w') as zip_file:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, repo_path))

def get_repo_contents(repo_path):
    """
    Main function to get repository contents.
    """
    repo_name = os.path.basename(repo_path)

    print(f"Analyzing Ruby on Rails project: {repo_name}")
    project_summary = analyze_rails_project(repo_path)

    print(f"\nCreating ZIP file for: {repo_name}")
    output_filename = f'{repo_name}_contents.zip'
    create_project_zip(repo_path, output_filename)

    instructions = f"Prompt: Analyze the {repo_name} Ruby on Rails project to understand its structure, purpose, and functionality. Follow these steps to study the codebase:\n\n"
    instructions += "1. Review the project summary to gain an overview of the project, its dependencies, and key components.\n\n"
    instructions += "2. Examine the controllers, models, and views to understand the core functionality of the application.\n\n"
    instructions += "3. Study the routes defined in `config/routes.rb` to understand the available endpoints and their corresponding actions.\n\n"
    instructions += "4. Analyze the dependencies and gems used in the project, as specified in the `Gemfile`.\n\n"
    instructions += "5. Investigate any configuration files (e.g., `config/database.yml`, `config/application.rb`) to understand how the project is configured.\n\n"
    instructions += "6. Look for any tests or test directories (e.g., `spec/`, `test/`) to see how the project ensures code quality and handles different scenarios.\n\n"
    instructions += "7. Review any documentation or inline comments to gather insights into the codebase and its intended behavior.\n\n"
    instructions += "8. Identify any potential areas for improvement, optimization, or further exploration based on your analysis.\n\n"
    instructions += "9. Provide a summary of your findings, including the project's purpose, key features, and any notable observations or recommendations.\n\n"
    instructions += "Use the ZIP file and project summary provided to complete this analysis.\n\n"

    return repo_name, instructions, project_summary, output_filename

if __name__ == '__main__':
    repo_path = input("Please enter the path to the local Ruby on Rails project: ")
    try:
        repo_name, instructions, project_summary, output_filename = get_repo_contents(repo_path)
        print(f"Project summary:\n{project_summary}\n")
        print(f"Analysis instructions and project ZIP file saved to '{output_filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check the project path and try again.")
