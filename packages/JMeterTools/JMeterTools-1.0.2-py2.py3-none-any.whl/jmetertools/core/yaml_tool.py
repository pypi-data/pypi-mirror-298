import yaml


def read_yaml(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as file:
        test_data = yaml.safe_load(file)
    return test_data
