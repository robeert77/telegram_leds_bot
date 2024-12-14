import asyncio
from led_strip.strip_settings import StripSettings
from rpi_ws281x import *

class Strip(object):
    __instance = None
    __strip_settings = None
    _first_led = 0
    strip = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Strip, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.__strip_settings = StripSettings()

            settings = self.__strip_settings.get_leds_settings()

            self.strip = Adafruit_NeoPixel(
                settings['count'],
                settings['pin'],
                settings['freq_hz'],
                settings['dma'],
                settings['invert_signal'],
                settings['brightness'],
                settings['channel']
            )

            self.strip.begin()
            self._first_led = settings['first_led']
            self.__previous_brightness = settings['brightness']

            self.initialized = True

    def fill(self, color):
        for i in range(self._first_led, self.get_pixels_number()):
            self.set_pixel_color(i, color)
        self.show_leds()

    def set_pixel_color(self, pixel, color):
        self.strip.setPixelColor(pixel, color)

    def get_pixels_number(self):
        return self.strip.numPixels()

    def get_brightness(self):
        return self.strip.getBrightness()

    def set_brightness(self, brightness):
        self.strip.setBrightness(brightness)

    def get_previous_brightness(self):
        return self.__previous_brightness

    def set_previous_brightness(self):
        self.__previous_brightness = self.get_brightness()

    def show_leds(self):
        self.strip.show()

    async def set_brightness_fade_effect(self, brightness, wait_ms=30):
        current_brightness = self.get_brightness()

        step = 1 if current_brightness < brightness else -1

        while current_brightness != brightness:
            current_brightness += step
            self.set_brightness(current_brightness)
            self.show_leds()
            await asyncio.sleep(wait_ms / 1000.0)
