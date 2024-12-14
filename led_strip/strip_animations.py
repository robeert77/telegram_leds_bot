from led_strip.strip import Strip
from rpi_ws281x import *
import time
import threading

class StripAnimations(Strip):
    def __init__(self):
        super().__init__()
        self.__animation_running = False

    def __wheel(self, position):
        if position < 85:
            return Color(position * 3, 255 - position * 3, 0)
        elif position < 170:
            position -= 85
            return Color(255 - position * 3, 0, position * 3)
        else:
            position -= 170
            return Color(0, position * 3, 255 - position * 3)

    def __rainbow(self, wait_ms=30):   
        while self.__animation_running:
            for j in range(256):
                if not self.__animation_running:
                    break
                
                for i in range(self._first_led, self.get_pixels_number()):
                    self.set_pixel_color(i, self.__wheel((i + j) & 255))

                self.show_leds()
                time.sleep(wait_ms / 1000.0)

    async def rainbow_animation(self):
        if not hasattr(self, '__rainbow_animation') or not self.__rainbow_animation.is_alive():
            await self.set_brightness_fade_effect(self.get_previous_brightness())
            self.__animation_running = True
            self.__rainbow_animation = threading.Thread(target=self.__rainbow) 
            self.__rainbow_animation.start()

    async def fade_out(self, wait_ms=40):
        self.set_previous_brightness()
        await self.set_brightness_fade_effect(0, wait_ms)  
        self.__animation_running = False  
        self.fill(Color(0, 0, 0))

    async def change_brightness(self, brightness, wait_ms=40):
        await self.set_brightness_fade_effect(brightness, wait_ms)
        self.set_previous_brightness()

