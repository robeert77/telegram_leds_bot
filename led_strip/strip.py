import asyncio
from led_strip.strip_settings import StripSettings
from rpi_ws281x import *

class Strip(object):
    __strip_settings = None
    _strip = None
    _first_led = 0

    def __init__(self):
        if Strip.__strip_settings is None:
            Strip.__strip_settings = StripSettings()

        if Strip._strip is None:
            settings = Strip.__strip_settings.get_leds_settings()
            Strip._strip = Adafruit_NeoPixel(
                settings['count'],
                settings['pin'],
                settings['freq_hz'],
                settings['dma'],
                settings['brightness'],
                settings['invert_signal'],
                settings['channel'],
                settings['count'],
            )

            Strip._strip.begin()
            self._first_led = settings['first_led']

    def set_pixel_color(self, pixel, color):
        Strip._strip.setPixelColor(pixel, color)

    def get_pixels_number(self):
        return Strip._strip.numPixels()

    def get_brightness(self):
        return Strip._strip.getBrightness()

    def set_brightness(self, brightness):
        Strip._strip.setBrightness(brightness)

    def show_leds(self):
        Strip._strip.show()

    async def set_brightness_fade_effect(self, brightness, wait_ms=40):
        current_brightness = self.get_brightness()

        step = 1 if current_brightness < brightness else -1

        while current_brightness != brightness:
            current_brightness += step
            self.set_brightness(current_brightness)
            self.show_leds()
            await asyncio.sleep(wait_ms / 1000.0)
