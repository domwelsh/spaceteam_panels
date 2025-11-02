"""
Chromatek RGB Push Button Switch Controller
Controls an RGB LED switch via WS2812B protocol and reads button state
"""

from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO


class ChromatekSwitch:
    """
    Controller for Chromatek RGB push button switch

    Hardware connections:
    - VDD -> 5V
    - Data In -> GPIO 18 (PWM)
    - Ground -> GND
    - C (Common) -> GND
    - NO (Normally Open) -> GPIO 23
    """

    # LED strip configuration
    LED_COUNT = 1          # Number of LED pixels (1 for single button)
    LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM)
    LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10           # DMA channel to use for generating signal
    LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False     # True to invert the signal
    LED_CHANNEL = 0        # Set to '1' for GPIOs 13, 19, 41, 45 or 53

    # Button configuration
    BUTTON_PIN = 23        # GPIO pin for button state

    def __init__(self, brightness=255):
        """
        Initialize the Chromatek switch controller

        Args:
            brightness (int): LED brightness (0-255), default 255
        """
        self.LED_BRIGHTNESS = brightness

        # Initialize LED strip
        self.strip = PixelStrip(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL
        )
        self.strip.begin()

        # Initialize button GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Callback storage
        self._press_callbacks = []
        self._release_callbacks = []
        self._button_event_added = False

    def set_color(self, red, green, blue):
        """
        Set the LED to a specific RGB color

        Args:
            red (int): Red value (0-255)
            green (int): Green value (0-255)
            blue (int): Blue value (0-255)
        """
        color = Color(red, green, blue)
        self.strip.setPixelColor(0, color)
        self.strip.show()

    def turn_on(self, red=255, green=255, blue=255):
        """
        Turn on the LED (default: white)

        Args:
            red (int): Red value (0-255), default 255
            green (int): Green value (0-255), default 255
            blue (int): Blue value (0-255), default 255
        """
        self.set_color(red, green, blue)

    def turn_off(self):
        """Turn off the LED"""
        self.set_color(0, 0, 0)

    def set_brightness(self, brightness):
        """
        Set LED brightness

        Args:
            brightness (int): Brightness level (0-255)
        """
        self.strip.setBrightness(brightness)
        self.strip.show()

    def get_button_state(self):
        """
        Read the current button state

        Returns:
            bool: True if button is pressed, False if released
        """
        # GPIO.LOW (0) when pressed because NO contact pulls to GND
        return GPIO.input(self.BUTTON_PIN) == GPIO.LOW

    def on_button_press(self, callback):
        """
        Register a callback for button press events

        Args:
            callback: Function to call when button is pressed
        """
        self._press_callbacks.append(callback)
        self._setup_button_events()

    def on_button_release(self, callback):
        """
        Register a callback for button release events

        Args:
            callback: Function to call when button is released
        """
        self._release_callbacks.append(callback)
        self._setup_button_events()

    def _setup_button_events(self):
        """Set up GPIO event detection for button (internal use)"""
        if not self._button_event_added:
            GPIO.add_event_detect(
                self.BUTTON_PIN,
                GPIO.BOTH,
                callback=self._button_event_handler,
                bouncetime=200  # 200ms debounce
            )
            self._button_event_added = True

    def _button_event_handler(self, channel):
        """Handle button events (internal use)"""
        if self.get_button_state():
            # Button pressed
            for callback in self._press_callbacks:
                callback()
        else:
            # Button released
            for callback in self._release_callbacks:
                callback()

    def cleanup(self):
        """Clean up GPIO resources"""
        self.turn_off()
        GPIO.cleanup()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
