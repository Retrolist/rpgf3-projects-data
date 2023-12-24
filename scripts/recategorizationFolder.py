import json
import os

def apply_recategorization_mapping_to_file(input_file_path, recategorization_mapping, recategorization_mapping2, output_folder):
    # Load the input JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        project = json.load(file)

    # Apply the recategorization mapping to the project
    project_id = project.get('id').split('|')[1]
    if project_id in recategorization_mapping:
        project['primaryCategory'] = recategorization_mapping[project_id]
        project['recategorization'] = recategorization_mapping2[project_id]

    # Save the updated data to a new file in the output folder
    output_file_path = os.path.join(output_folder, os.path.basename(input_file_path))
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(project, file, indent=2)

def process_folder(folder_path, recategorization_file_path, output_folder):
    # Load the recategorization JSON file
    with open(recategorization_file_path, 'r', encoding='utf-8') as file:
        recategorization_data = json.load(file)

    # Create the recategorization mapping
    recategorization_mapping = {}
    recategorization_mapping2 = {}
    for collection in recategorization_data:
        collection_name = collection['name']
        for category in collection['ranking']:
            category_name = category['name']
            for project in category['ranking']:
                recategorization_mapping[project['id']] = collection_name
                recategorization_mapping2[project['id']] = category_name

    # Process each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            apply_recategorization_mapping_to_file(file_path, recategorization_mapping, recategorization_mapping2, output_folder)

# Example usage
folder_path = 'projects'
recategorization_file_path = 'recategorization.json'
output_folder = 'projectsOut'

process_folder(folder_path, recategorization_file_path, output_folder)