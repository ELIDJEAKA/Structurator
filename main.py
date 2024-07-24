import os
import json
import argparse

# Fonction pour lire la structure des dossiers et fichiers depuis un fichier JSON
def load_structure(json_file):
    with open(json_file, 'r') as f:
        structure = json.load(f)
    return structure

# Fonction pour créer les dossiers et fichiers
def create_structure(base_path, structure):
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

# Fonction pour générer le contenu du diagramme
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

# Fonction principale
def main(json_path):
    
    structure = load_structure(json_path)
    
    create_structure(".", structure)

    diagram_content = "225lol/\n" + generate_diagram(structure)
    diagram_path = os.path.join(".", "diagram.md")
    with open(diagram_path, 'w') as diagram_file:
        diagram_file.write(diagram_content)

    print("Structure des dossiers et fichiers créée avec succès et diagram.md mis à jour.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate directory structure from a JSON file.')
    parser.add_argument('json_path', type=str, help='Path to the JSON file defining the structure')
    
    args = parser.parse_args()
    main(args.json_path)
