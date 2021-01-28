from jinja2 import Environment, PackageLoader, select_autoescape

from script import get_weather_warning, get_lat_and_long 


def create_html(weather_data):
    env = Environment(
        loader = PackageLoader('script', 'templates'),
        autoescape = select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    html_output = template.render(weather_data=weather_data)

    print(html_output)

    # Save the output to alert.html
    with open('templates/alert.html', 'w') as f:
        f.write(html_output)
        print("Output successfully saved to alert.html")


if __name__ == '__main__':
    city = 'Davis'
    state = 'CA'
    location = get_lat_and_long(city, state) 
    weather_data = get_weather_warning(location['latitude'], location['longitude'])
    create_html(weather_data)
