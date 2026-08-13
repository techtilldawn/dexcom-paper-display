import os, time
import epaper

from pydexcom import Dexcom
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


UNICODE_ARROWS_MAP = {
    # If pydexcom returns string names
    "DoubleUp": "\uf062\uf062",
    "SingleUp": "\uf062",
    "FortyFiveUp": "\uf176",
    "Flat": "\uf061",
    "FortyFiveDown": "\uf175",
    "SingleDown": "\uf063",
    "DoubleDown": "\uf063\uf063",
}

class Credentials:
    def __init__(self):
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

class Display:
    def __init__(self, display_type):
        self.epd = epaper.epaper(display_type).EPD()

    def size(self) -> list[int]:
        return [self.epd.height, self.epd.width]

    def clear(self) -> None:
        self.epd.init()
        self.epd.Clear(0xFF)

    def display(self, image: Image) -> None:
        self.epd.display(self.epd.getbuffer(image))

    def sleep(self) -> None:
        self.epd.sleep()
        

def get_dexcom_data() -> dict:
    load_dotenv()
    credentials = Credentials()
    dexcom = Dexcom(
        username=credentials.username,
        password=credentials.password,
        region="ous"
        )
    current_reading = dexcom.get_current_glucose_reading()
    # TODO: Error handling, if return trend name doesn't fit mapping...
    trend_arrow_unicode = UNICODE_ARROWS_MAP[current_reading.trend_direction] if current_reading.trend_direction in UNICODE_ARROWS_MAP else "\uf128"
    return {
        "glucose_reading": str(current_reading.value),
        "trend_arrow": str(trend_arrow_unicode)
    }

def get_ext_folder() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')

def main():
    data = get_dexcom_data()
    epd = Display('epd2in13_V3')
    epd.clear()
    rootDir = get_ext_folder()
    font15 = ImageFont.truetype(os.path.join(rootDir, '0xProtoNerdFontMono-Regular.ttf'), 75)
    image = Image.new('1', epd.size(), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "{0} {1}".format(data["glucose_reading"],data["trend_arrow"]), font = font15, fill = 0)

    epd.display(image)
    epd.sleep()
    time.sleep(5)
