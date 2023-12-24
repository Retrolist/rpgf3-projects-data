import json

def apply_recategorization_mapping(recategorization_file_path, projects_all_file_path, output_file_path, filtered_output_file_path):
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

    # Load the projectsAll.json file
    with open(projects_all_file_path, 'r', encoding='utf-8') as file:
        projects_all_data = json.load(file)

    # Apply the recategorization mapping to the projects
    for project in projects_all_data:
        project_id = project.get('id')
        if project_id in recategorization_mapping:
            project['recategorization'] = recategorization_mapping2[project_id]
            project['primaryCategory'] = recategorization_mapping[project_id]

    # Save the updated full projects data
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(projects_all_data, file, indent=2)

    # Filter projects with "prelimResult": "Keep"
    filtered_projects_keep = [project for project in projects_all_data if project.get('prelimResult') == 'Keep']

    # Save the filtered projects data
    with open(filtered_output_file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_projects_keep, file, indent=2)

# Example usage
recategorization_file_path = 'recategorization.json'
projects_all_file_path = 'projectsAll.json'
output_file_path = 'projectsAll_updated.json'
filtered_output_file_path = 'projects_filtered_keep.json'

apply_recategorization_mapping(recategorization_file_path, projects_all_file_path, output_file_path, filtered_output_file_path)