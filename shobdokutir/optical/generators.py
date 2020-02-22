import json
from PIL import Image
from io import BytesIO
import selenium.webdriver
from shobdokutir.optical.image_utils import trim_image
from shobdokutir.web.servers import run_parrot_server
from multiprocessing import Process
from subprocess import check_output


class OpticalTextBuilder:
    """
    Definition: Optical Text Generator uses a server and a web browser to generate any unicode text.
    Assumptions: The environment must be configured properly to correctly render the text.
    """

    def __init__(self, server_port: int = 6976, server_host: str = '0.0.0.0') -> None:
        """
        Starts a parrot server and a web browser
        """
        self.server_host = server_host
        self.server_port = server_port
        self.process = Process(target=run_parrot_server, args=(self.server_host, self.server_port))
        self.process.start()
        self.driver = selenium.webdriver.Firefox()

    def clear_all(self) -> None:
        """
        Tears down both the server and the client
        """
        self.process.terminate()
        self.driver.close()
        self.driver.quit()

    def get_text_image(self, txt: str, font_size: int = None, font_name: str = None,) -> Image:
        """
        Get an image of the text in the specified font_name and font_size
        """
        if font_size:
            font_size_text = f"&size={font_size}"
        else:
            font_size_text = ""
        if font_name:
            font_name_text = f"&font={font_name}"
        else:
            font_name_text = ""
        url = f"http://{self.server_host}:{str(self.server_port)}" \
            f"?message={json.dumps(txt)}{font_name_text}{font_size_text}"
        print(url)
        self.driver.get(url)
        data = self.driver.get_full_page_screenshot_as_png()
        img = Image.open(BytesIO(data))
        return trim_image(img)


def get_font_details():
    font_list = check_output(["fc-list"]).decode("unicode-escape").split("\n")
    font_details = {}
    for a_font in font_list:
        if not a_font.strip():
            continue
        font_entry = [a_col.strip().split("=")[1] if i == 2 else a_col.strip()
                      for i, a_col in enumerate(a_font.split(":"))]
        font_entry[2] = set(font_entry[2].split(",")) if "," in font_entry[2] else {font_entry[2]}
        font_details.setdefault(font_entry[1], {'path': [], 'style': []})['path'].append(font_entry[0])
        font_details[font_entry[1]]['style'].append(font_entry[2])
    return font_details
