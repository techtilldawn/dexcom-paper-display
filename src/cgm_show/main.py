import os

from pydexcom import Dexcom
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V2

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

    epd = epd2in13_V2.EPD()
    epd.init()
    epd.Clear(0xFF)

    image = Image.new("1", (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "Standard UV Layout!", fill=0)

    epd.display(epd.getbuffer(image))
    epd.sleep()

if __name__ == "__main__":
    main()
