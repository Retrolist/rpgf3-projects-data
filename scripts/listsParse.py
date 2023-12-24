import json
import os

def apply_list_mapping(input_file_path, project_lists_mapping, output_folder):
    # Load the input JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        project = json.load(file)

    # Apply the recategorization mapping to the project
    project_id = project['id'].split('|')[1]
    if project_id in project_lists_mapping:
        project['lists'] = project_lists_mapping[project_id]
    else:
        project['lists'] = []

    # Save the updated data to a new file in the output folder
    output_file_path = os.path.join(output_folder, os.path.basename(input_file_path))
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(project, file, indent=2)

def transform_header(item):
    return {
        "id": item.get("id"),
        "listName": item.get("listName", ""),
        "impactEvaluationType": item.get("impactEvaluationType", ""),
        "categories": item.get("categories", []),
        "projectsMetadata": list(map(lambda project: {
            "id": project.get("id"),
            "displayName": project.get("displayName"),
            "profileImageUrl": project.get("profileImageUrl", None),
        }, item.get("projectsMetadata", [])))
    }

def process_folder(folder_path, lists_file_path, output_folder):
    # Load the recategorization JSON file
    with open(lists_file_path, 'r', encoding='utf-8') as file:
        lists = json.load(file)

    project_lists_mapping = {}

    for list in lists:
        for project in list['projectsMetadata']:
            if not project['id'] in project_lists_mapping:
                project_lists_mapping[project['id']] = []
            project_lists_mapping[project['id']].append(transform_header(list))

    # Process each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            apply_list_mapping(file_path, project_lists_mapping, output_folder)

# Example usage
folder_path = 'projects'
lists_file_path = '../rpgf3-lists-data/lists.json'
output_folder = 'projectsOut'

process_folder(folder_path, lists_file_path, output_folder)