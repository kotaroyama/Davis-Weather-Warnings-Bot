from os import environ
from os.path import abspath, dirname

from jinja2 import Environment, PackageLoader, select_autoescape
import imgkit


CURRENT_DIR = dirname(abspath(__file__))

def create_html(weather_data):
    env = Environment(
        loader = PackageLoader('script', 'templates'),
        autoescape = select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    html_output = template.render(weather_data=weather_data)

    # Save the output to alert.html
    with open(f'{CURRENT_DIR}/templates/alert.html', 'w') as f:
        f.write(html_output)
        print("Output successfully saved to alert.html")

def html_to_img(html_file):
    output_file = 'out.jpg'
    options = {
        "width": "900",
        "height": "700",
    }
    imgkit.from_file(f'{CURRENT_DIR}/templates/{html_file}', f'{CURRENT_DIR}/templates/{output_file}', options=options);
    with open(f'{CURRENT_DIR}/templates/{output_file}', 'r') as output:
        print('Successfully saved to out.jpg')
