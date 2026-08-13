import epaper
from PIL import Image, ImageDraw, ImageFont
from .browsing import get_font_path

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

    def create_text_image(self, text: str, font_size: int = 75) -> Image:
        font = ImageFont.truetype(get_font_path(), font_size)
        image = Image.new('1', self.size(), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font = font, fill = 0)
        return image

    def display_image(self, text: str, font_size: int = 75):
        self.clear()
        self.display(self.create_text_image(text, font_size))
        self.sleep()
