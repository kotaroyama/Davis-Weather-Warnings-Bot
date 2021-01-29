from os import getcwd, path
import sys
import unittest

sys.path.insert(1, '..')
from create_temp import create_html, html_to_img

FAKE_WEATHER = {
    "active": True,
    "head": "Flash Flood Watch",
    "by": "NWS Sacramento CA",
    "where": "Southern Sacramento Valley",
    "when": "January 28 at 2:22AM PST until January 28 at 5:00PM PST",
    "what": "The Flash Flood Watch continues for\n\n* The Yolo and Solano County portion of the Hennessey Fire in the\nLNU Lightning Complex Burn Scar in northern California.\n\n* Through this afternoon\n\n* Periods of heavy rainfall and possible thunderstorms are\nforecasted over the Hennessey Fire in the LNU Lightning Complex\nBurn Scar, which may lead to flash flooding and debris flows.\n\n* Heavy rainfall and possible thunderstorms over the Hennessey Fire\nin the LNU Lightning Complex Burn Scar is expected during the\nperiod of the watch. Residents near the Hennessey Fire in the LNU\nLightning Complex Burn Scar should prepare for potential flooding\nimpacts. Be sure to stay up to date with information from local\nauthorities."
}

PARENT_DIR = path.dirname(getcwd()) 

class TestCreateTemplate(unittest.TestCase):

    def test_create_html(self):
        # Create the html template
        create_html(FAKE_WEATHER)

        # Get the file name and extension
        created_html_path = f'{PARENT_DIR}/templates/alert.html'
        created_html_ext = path.splitext(created_html_path)[1]

        self.assertTrue(path.exists(created_html_path))
        self.assertEqual(created_html_ext, '.html')


class TestCreateImage(unittest.TestCase):

    def test_html_to_jpg(self):
        # Create the html template
        create_html(FAKE_WEATHER)

        # Convert html to jpg
        html_to_img(f'{PARENT_DIR}/templates/alert.html')
        image_path = f'{PARENT_DIR}/templates/out.jpg'
        created_html_ext = path.splitext(image_path)[1]

        self.assertTrue(path.exists(image_path))
        self.assertEqual(created_html_ext, '.jpg')


if __name__ == '__main__':
    unittest.main()
