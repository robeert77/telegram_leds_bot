from settings.settings import Settings


class StripSettings(Settings):
    def __init__(self):
        super().__init__('led_strip/config.json')

    def get_leds_settings(self):
        leds_settings = self._get_from_json_file_by_key('leds_settings') or {}

        leds_settings.setdefault('count', 300)
        leds_settings.setdefault('pin', 18)
        leds_settings.setdefault('freq_hz', 800000)
        leds_settings.setdefault('dma', 10)
        leds_settings.setdefault('brightness', 60)
        leds_settings.setdefault('invert_signal', False)
        leds_settings.setdefault('channel', 0)
        leds_settings.setdefault('first_led', 0)

        return leds_settings
