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
            output += '- ' + '\n- '.join([item['description'] for item in items]) + '\n\n'

    return output

yaml_dict = {}

directory = "changelog/kong"
process_yaml_directory(directory, yaml_dict)

directory = "changelog/kong-ee"
process_yaml_directory(directory, yaml_dict)

def write_output_to_file(output, filename):
    with open(filename, 'w') as file:
        file.write(output)

print(generate_markdown_output(yaml_dict))
