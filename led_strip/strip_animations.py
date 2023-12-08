from led_strip.strip import Strip
from rpi_ws281x import *
import time

class StripAnimations(Strip):
    def __init__(self):
        super().__init__()

    def __wheel(self, position):
        if position < 85:
            return Color(position * 3, 255 - position * 3, 0)
        elif position < 170:
            position -= 85
            return Color(255 - position * 3, 0, position * 3)
        else:
            position -= 170
            return Color(0, position * 3, 255 - position * 3)

    def __rainbow(self, wait_ms=20):
        for j in range(256):
            for i in range(self._first_led, self.get_pixels_number()):
                self.set_pixel_color(i, self.__wheel((i + j) & 255))
            self.show_leds()
            time.sleep(wait_ms / 1000.0)

    async def turn_leds_on(self):
        self.__rainbow()

    async def fade_out(self, wait_ms=40):
        await self.set_brightness_fade_effect(0, wait_ms)

    async def change_brightness(self, brightness, wait_ms=40):
        await self.set_brightness_fade_effect(brightness, wait_ms)

