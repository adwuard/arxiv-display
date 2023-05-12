 
import time
from PIL import Image, ImageDraw, ImageFont

class BaseView:
    def __init__(self):
        pass

    def render(self):
        raise NotImplementedError("Subclass must implement abstract method")

 
class WifiView(BaseView):
    def __init__(self, screen_driver):
        self.screen_driver = screen_driver
        self.model = None

    def update(self, model, mesg=None):
        self.model = model
        self.mesg = mesg

    def render(self):
        if self.model == 'connecting':
            pil_image = self.connecting_screen()
        elif self.model == 'disconnected':
            pil_image = self.disconnected_screen()
        elif self.model == 'error':
            pil_image = self.error_screen()
        else:
            pil_image = self.no_wifi_screen()
        self.screen_driver.render(pil_image)

    def no_wifi_screen(self):
        new_image = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype("arial.ttf", 12)
        current_time = time.strftime("%H:%M")
        draw.text((350, 4), f'{current_time}', font=font, fill='black')
        draw.line((10, 18, 400-10, 18), fill='black', width=1)
        draw.line((10, 75-2, 400-10, 75-2), fill='black', width=1)
        return new_image

    def connecting_screen(self):
        new_image = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype("arial.ttf", 12)
        current_time = time.strftime("%H:%M")
        draw.text((350, 4), f'{current_time}', font=font, fill='black')
        draw.line((10, 18, 400-10, 18), fill='black', width=1)
        draw.line((10, 75-2, 400-10, 75-2), fill='black', width=1)
        draw.text((150, 100), 'Connecting...', font=font, fill='black')
        return new_image

    def disconnected_screen(self):
        new_image = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype("arial.ttf", 12)
        current_time = time.strftime("%H:%M")
        draw.text((350, 4), f'{current_time}', font=font, fill='black')
        draw.line((10, 18, 400-10, 18), fill='black', width=1)
        draw.line((10, 75-2, 400-10, 75-2), fill='black', width=1)
        draw.text((150, 100), 'Disconnected', font=font, fill='black')
        return new_image

    def error_screen(self):
        new_image = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype("arial.ttf", 12)
        current_time = time.strftime("%H:%M")
        draw.text((350, 4), f'{current_time}', font=font, fill='black')
        draw.line((10, 18, 400-10, 18), fill='black', width=1)
        draw.line((10, 75-2, 400-10, 75-2), fill='black', width=1)
        draw.text((150, 100), 'Error', font=font, fill='black')
        draw.text((10, 200), str(self.mesg), font=font, fill='black')

        return new_image
