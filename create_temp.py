from os import environ
from os.path import abspath, dirname
from shutil import copyfileobj

from jinja2 import Environment, PackageLoader, select_autoescape
import requests

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
    HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
    # Retrieve these from https://htmlcsstoimage.com/dashboard
    HCTI_API_USER_ID = environ['HCTI_API_USER_ID']
    HCTI_API_KEY = environ['HCTI_API_KEY']
    
    # Read alert.html
    with open(html_file, 'r') as f:
        html_content = f.read()
        data = {
            'html': html_content,
            'viewport_height': 700,
            'viewport_width': 900,
            'google_fonts': 'Roboto'
        }
        image = requests.post(
            url=HCTI_API_ENDPOINT,
            data=data,
            auth=(HCTI_API_USER_ID, HCTI_API_KEY)
        )

        # Check if the POST request was successful
        if image.status_code != requests.codes.ok:
            image.raise_for_status()

        # Write to template/out.jpg
        url = image.json()['url']
        r = requests.get(url, stream=True)
        image_file = f'{CURRENT_DIR}/templates/out.jpg'
        with open(image_file, 'wb') as output:
            copyfileobj(r.raw, output)
            print('Successfully saved to out.jpg')
