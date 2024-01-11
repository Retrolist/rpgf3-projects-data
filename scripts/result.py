import csv
import json
import os

categoryOP = {}
projectsMetadata = {}

def process_csv_and_json(csv_file_path, approveAttestationMapping):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rowindex = 0
        for row in csv_reader:
            rowindex = rowindex + 1
            project_id = approveAttestationMapping[row['project_id']]
            votes_count = int(row['votes_count'])
            scaled_amount = float(row['scaled_amount'])

            json_file_path = f"projects/{project_id}.json"
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)

                projectId = data['id'].split('|')[1]

                data['includedInBallots'] = votes_count
                data['totalOP'] = scaled_amount
                data['rank'] = rowindex

                projectsMetadata[projectId] = {
                    'includedInBallots': votes_count,
                    'totalOP': scaled_amount,
                    'rank': rowindex,
                }

                if data['primaryCategory'] not in categoryOP:
                    categoryOP[data['primaryCategory']] = {
                        'total': 0,
                        'projects': {},
                    }
                categoryOP[data['primaryCategory']]['total'] += scaled_amount
                categoryOP[data['primaryCategory']]['projects'][projectId] = scaled_amount

                if data['recategorization'] not in categoryOP:
                    categoryOP[data['recategorization']] = {
                        'total': 0,
                        'projects': {},
                    }
                categoryOP[data['recategorization']]['total'] += scaled_amount
                categoryOP[data['recategorization']]['projects'][projectId] = scaled_amount

                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, indent=4)
            else:
                print(f"JSON file for project ID {project_id} not found.")

# Example usage
csv_file_path = 'rpgf3_allocation_final.csv'

with open('approveAttestationMapping.json', 'r', encoding='utf-8') as file:
    approveAttestationMapping = json.load(file)

process_csv_and_json(csv_file_path, approveAttestationMapping)

with open('categoryOP.json', 'w', encoding='utf-8') as json_file:
    json.dump(categoryOP, json_file, indent=4)

for filename in ['projects.json', 'projectsAll.json']:
    with open(filename, 'r', encoding='utf-8') as file:
        projects = json.load(file)
        for project in projects:
            if project['id'] in projectsMetadata:
                project['includedInBallots'] = projectsMetadata[project['id']]['includedInBallots']
                project['totalOP'] = projectsMetadata[project['id']]['totalOP']
                project['rank'] = projectsMetadata[project['id']]['rank']
            else:
                if filename == 'projects.json':
                    print('Project not found', project['id'])
        with open(filename+'new.json', 'w', encoding='utf-8') as json_file:
            json.dump(projects, json_file, indent=4)