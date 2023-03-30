from os import environ
from os.path import abspath, dirname

from jinja2 import Environment, PackageLoader, select_autoescape


CURRENT_DIR = dirname(abspath(__file__))

def create_html(weather_data):
    env = Environment(
        loader = PackageLoader('script', 'templates'),
        autoescape = select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    html_output = template.render(weather_data=weather_data)

    # Save the output to alert.html
    with open(f'{CURRENT_DIR}/templates/index.html', 'w') as f:
        f.write(html_output)
        print("Output successfully saved to index.html")
