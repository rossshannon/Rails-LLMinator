# Rails LLMinator

Rails LLMinator is a Python script that analyzes a local Ruby on Rails project and generates a zip file containing the relevant project files along with analysis instructions. This tool is designed to help you understand the structure, purpose, and functionality of a Ruby on Rails project.

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- Python 3.x
- `gitpython` library
- `rubyparser` library
- `tqdm` library

You can install the required libraries using pip:

```
pip install gitpython rubyparser tqdm
```

## Usage

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory where the `repototxt.py` script is located.

3. Run the script using the following command:

```
python repototxt.py
```

4. When prompted, enter the path to your local Ruby on Rails project.

5. The script will analyze the project and generate a zip file named `<project_name>_contents.zip` in the same directory as the script.

6. The zip file will contain the relevant project files and a set of instructions to guide you in analyzing the project.

## Output

The script will provide the following output:

- Project summary: A summary of the project, including its structure, dependencies, and key components.
- Zip file: A zip file containing the relevant project files for further analysis.
- Analysis instructions: A set of instructions to guide you in understanding the project's purpose, functionality, and potential areas for improvement.

## Customization

If you want to customize the analysis or extract additional information from the Ruby on Rails project, you can modify the `analyze_rails_project` function in the `repototxt.py` script. This function is responsible for extracting relevant information from the project's controllers, models, views, routes, and dependencies.

## Limitations

- The script currently supports analyzing Ruby on Rails projects only.
- The accuracy and completeness of the analysis depend on the implementation of the `analyze_rails_project` function. You may need to adapt it based on your specific project structure and requirements.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

Rails LLMinator is originally forked from https://github.com/Doriandarko/RepoToTextForLLMs/ by https://github.com/Doriandark

## License

This project is licensed under the [MIT License](LICENSE).
