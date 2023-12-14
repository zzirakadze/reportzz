from jinja2 import Environment, FileSystemLoader
import json
import os


def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


with open(os.path.join(get_root_dir(), 'XM', 'aggregated_test_report.json')) as file:
    report = file.read()

    test_data = json.loads(report)

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')

    output = template.render(tests=test_data)

    with open('output_report.html', 'w') as file:
        file.write(output)
