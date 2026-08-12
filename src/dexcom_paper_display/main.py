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
    print("clear")
    epd.init(epd.PART_UPDATE)
    epd.Clear(0xFF)
    rootDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'ext')

    font15 = ImageFont.truetype(os.path.join(rootDir, '0xProtoNerdFontMono-Regular.ttf'), 15)
    
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    draw.rectangle([(0,0),(50,50)],outline = 0)
    draw.rectangle([(55,0),(100,50)],fill = 0)
    draw.line([(0,0),(50,50)], fill = 0,width = 1)
    draw.line([(0,50),(50,0)], fill = 0,width = 1)
    draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
    draw.ellipse((55, 60, 95, 100), outline = 0)
    draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
    draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
    draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
    draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
    draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
    epd.display(epd.getbuffer(image))
    epd.sleep()
