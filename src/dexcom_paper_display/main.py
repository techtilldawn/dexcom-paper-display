import os, time

from pydexcom import Dexcom
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V3

class Credentials:
    def __init__(self):
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

def main():
    load_dotenv()

    credentials = Credentials()
    dexcom = Dexcom(
        username=credentials.username,
        password=credentials.password,
        region="ous"
        )

    glucose_reading = dexcom.get_current_glucose_reading()

    print(glucose_reading)

    epd = epd2in13_V3.EPD()
    print("clear")
    epd.init()
    epd.Clear(0xFF)
    rootDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'ext')

    font15 = ImageFont.truetype(os.path.join(rootDir, '0xProtoNerdFontMono-Regular.ttf'), 100)
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), str(glucose_reading), font = font15, fill = 0)

    epd.display(epd.getbuffer(image))
    time.sleep(5)
    epd.sleep()
