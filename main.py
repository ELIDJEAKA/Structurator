import os
import json
import argparse

# Function to read the structure of directories and files from a JSON file
def load_structure(json_file):
    if not os.path.isfile(json_file):
        print(f"Error: The path '{json_file}' is not a file or does not exist.")
        exit(1)
    
    try:
        with open(json_file, 'r') as f:
            structure = json.load(f)
        return structure
    except json.JSONDecodeError:
        print(f"Error: The file '{json_file}' is not a valid JSON file.")
        exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file '{json_file}'.")
        exit(1)

# Function to create directories and files
def create_structure(base_path, structure):
    try:
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                if not os.path.exists(path):
                    os.makedirs(path)
                create_structure(path, content)
            else:
                if not os.path.exists(path):
                    with open(path, 'w') as f:
                        f.write(content)
    except PermissionError:
        print(f"Error: Permission denied when trying to create '{path}'.")
        exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        exit(1)

# Function to generate the content of the diagram
def generate_diagram(structure, indent=0):
    diagram = ""
    for name, content in structure.items():
        if indent == 0 and name == ".env":
            diagram += "├── " + name + "\n"
        else:
            diagram += "│   " * indent + "├── " + name + "\n"
        if isinstance(content, dict):
            diagram += generate_diagram(content, indent + 1)
    return diagram

# Function to print ASCII art
def print_ascii_art():
    ascii_art = """
             /$$                                     /$$                                    /$$                        
            | $$                                    | $$                                   | $$                        
  /$$$$$$$ /$$$$$$    /$$$$$$  /$$   /$$  /$$$$$$$ /$$$$$$   /$$   /$$  /$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
 /$$_____/|_  $$_/   /$$__  $$| $$  | $$ /$$_____/|_  $$_/  | $$  | $$ /$$__  $$|____  $$|_  $$_/   /$$__  $$ /$$__  $$
|  $$$$$$   | $$    | $$  \__/| $$  | $$| $$        | $$    | $$  | $$| $$  \__/ /$$$$$$$  | $$    | $$  \ $$| $$  \__/
 \____  $$  | $$ /$$| $$      | $$  | $$| $$        | $$ /$$| $$  | $$| $$      /$$__  $$  | $$ /$$| $$  | $$| $$      
 /$$$$$$$/  |  $$$$/| $$      |  $$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$/| $$     |  $$$$$$$  |  $$$$/|  $$$$$$/| $$      
|_______/    \___/  |__/       \______/  \_______/   \___/   \______/ |__/      \_______/   \___/   \______/ |__/  
    """
    print(ascii_art)

# Main function
def main(json_path, target_folder):
    if not os.path.exists(target_folder):
        print(f"Error: The target folder '{target_folder}' does not exist.")
        exit(1)
    if not os.path.isdir(target_folder):
        print(f"Error: The target folder '{target_folder}' is not a directory.")
        exit(1)

    # Load the structure
    structure = load_structure(json_path)

    # Create the directory and file structure
    create_structure(target_folder, structure)

    # Generate and write the diagram to diagram.md
    diagram_content = os.path.basename(target_folder) + "/\n" + generate_diagram(structure)
    diagram_path = os.path.join(target_folder, "diagram.md")
    try:
        with open(diagram_path, 'w') as diagram_file:
            diagram_file.write(diagram_content)
    except PermissionError:
        print(f"Error: Permission denied when trying to write the file '{diagram_path}'.")
        exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred while writing the file '{diagram_path}': {e}")
        exit(1)

    print("Directory and file structure created successfully and diagram.md updated.")
    print_ascii_art()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate directory structure from a JSON file.')
    parser.add_argument('json_path', type=str, help='Path to the JSON file defining the structure')
    parser.add_argument('target_folder', type=str, help='Path to the target folder where the structure will be created')
    
    args = parser.parse_args()
    main(args.json_path, args.target_folder)
