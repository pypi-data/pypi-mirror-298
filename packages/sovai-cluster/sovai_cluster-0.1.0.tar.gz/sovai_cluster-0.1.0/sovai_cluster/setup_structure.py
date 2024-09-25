import os

# Define the folder structure
folder_structure = {
    "sovai-cluster": {
        "pyproject.toml": "",
        "README.md": "",
        "sovai_cluster": {
            "__init__.py": "",
            "data_processing.py": "",
            "clustering.py": "",
            "visualization.py": "",
            "utils.py": ""
        },
        "tests": {
            "__init__.py": ""
        }
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

# Create the folder structure
create_structure('.', folder_structure)