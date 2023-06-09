#!/usr/bin/python3
import os
import yaml

def process_yaml_directory(directory, result):

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                parse_yaml_file(filepath, result)

def parse_yaml_file(filepath, result):
    with open(filepath, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if isinstance(data, list):
                interpret_yaml_data(data, result)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {filepath}")
            print(e)

def generate_jira_link(jira_ticket):
    base_url = 'https://konghq.atlassian.net/browse/'
    return base_url + jira_ticket

def generate_github_link(repo, issue):
    base_url = 'https://github.com/'
    return base_url + repo + '/issues/' + str(issue)

def interpret_yaml_data(data, result):
    for item in data:
        change_type = item.get('change-type')
        subsystem = item.get('sub-system')
        description = item.get('description')

        if not change_type or not subsystem or not description:
            raise ValueError("Invalid YAML item. Missing 'change-type', 'sub-system', or 'description'.")

        if change_type not in result:
            result[change_type] = {}

        if subsystem not in result[change_type]:
            result[change_type][subsystem] = []

        result[change_type][subsystem].append(item)

def generate_markdown_output(result):
    output = ''

    for change_type, subsystems in result.items():
        output += f'## {change_type}\n\n'
        for subsystem, items in subsystems.items():
            output += f'### {subsystem}\n\n'
            for item in items:
                description = item['description']
                jira_links = item.get('jira-links', [])
                github_refs = item.get('github-refs', [])

                if jira_links:
                    links = ' '.join([f'[{link}]({generate_jira_link(link)})' for link in jira_links])
                    description += f' {links}'

                if github_refs:
                    for ref in github_refs:
                        repo = ref['repo']
                        issue = ref['issue']
                        link = generate_github_link(repo, issue)
                        description += f' [{repo}#{issue}]({link})'
                output += f'- {description}\n'

            output += '\n'

    return output

yaml_dict = {}

directory = "changelog/unreleased/kong"
process_yaml_directory(directory, yaml_dict)

directory = "changelog/unreleased/kong-ee"
process_yaml_directory(directory, yaml_dict)

def write_output_to_file(output, filename):
    with open(filename, 'w') as file:
        file.write(output)

print(generate_markdown_output(yaml_dict))
