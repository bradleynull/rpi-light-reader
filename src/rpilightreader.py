"""
Bradley Null 2013
"""
import RPi.GPIO as GPIO
import random
import time

class LightReader:
    """
    Class that can sample a light diode and toggle three LEDs on and off.
    """
    def __init__(self):
        """ 
        Constructor to setup the pins, variables and get the LEDs ready
        """
        # Pin setup for the LEDs and the light diode
        self._light_diode_pin = 16
        self._output_pins = {"red":11, "yellow":12, "green": 13}
        # Determine the LED was previously on or off
        self._pin_states = {"red":0, "yellow":0, "green": 0}

        # Previous reading from the light diode
        self._previous_reading = None
        # Maximum counts between each light reading to prevent infinite sampling
        self._max_light_reading = 10000
        # Filter variables for light diode. filter_a is what percentage to 
        # incorporate the current reading into the reading and filter_b is 
        # the what percentage to incorporate the previous reading
        self._light_reading_filter_a = 0.25
        self._light_reading_filter_b = 0.75

        # Setup the board and GPIO pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._output_pins["red"], GPIO.OUT)
        GPIO.setup(self._output_pins["yellow"], GPIO.OUT)
        GPIO.setup(self._output_pins["green"], GPIO.OUT)
        self.TurnOffAllLed()
    
    def __del__(self):
        """
        Clean up all the handles to the GPIO when this object is destroyed
        """
        GPIO.cleanup()

    def TurnOnLed(self, color):
        """
        Turn on a single LED.       
        @param color The color of the LED to turn on. Can be "red", "yellow", or
                "green"
        """
        if self._pin_states[color] != 1:
            GPIO.output(self._output_pins[color], True)
            self._pin_states[color] = 1

    def TurnOnAllLed(self):
        """
        Turn on all of the LEDs
        """
        for color in self._output_pins:
            self.TurnOnLed(color)

    def TurnOffLed(self, color):
        """
        Turn off a signle LED
        @param color The color of the LED to turn off. Can be "red", "yellow", 
                or "green"
        """
        if self._pin_states[color] != 0:
            GPIO.output(self._output_pins[color], False)
            self._pin_states[color] = 0

    def TurnOffAllLed(self):
        """
        Turn off all of the LEDs
        """
        for color in self._output_pins:
            self.TurnOffLed(color)

    def ToggleLed(self, colors_on=[], colors_off=[]):
        """
        Toggle on or off specific subsets of LEDs.
        @param colors_on The array of strings of colors to toggle on. The array
                can contain the strings "red", "yellow", and "green"
        """
        for color in colors_on:
            self.TurnOnLed(color)
        for color in colors_off:
            self.TurnOffLed(color)
    
    def Blink(self, colors, duration_light, duration_off=-1):
        """
        Flash a set of LEDs for a specific duration. 
        @param colors The array of strings of colors to blink. The array
                can contain the strings "red", "yellow", and "green"
        @param duration_light The amount of time to leave the LEDs on in seconds
        @param duration_off The amount of time to pause after turning off the
                LEDs. If not specified or -1, duration_off == duration_light
        """
        if duration_off < 0:
            duration_off = duration_light
        for color in colors:
            self.TurnOnLed(color)
        time.sleep(duration_light)
        for color in colors:
            self.TurnOffLed(color)
        time.sleep(duration_off)

    def ReadLight(self):
        """
        Read the light diode and return the number of counts.
        @return The number of counts read from the light diode. More counts
               indicate less light. Generally ranges from ~0-200 at full light
               and 10000 in dark. 
        """
        reading = 0
        # Pull power from the light diode to get it to charge the capacitor
        GPIO.setup(self._light_diode_pin, GPIO.OUT)
        GPIO.output(self._light_diode_pin, GPIO.LOW)
        time.sleep(0.1)

        # Start charging the diodes capacitor
        GPIO.setup(self._light_diode_pin, GPIO.IN)
        # This takes 1 millisecond per loop cycle
        while(GPIO.input(self._light_diode_pin) == GPIO.LOW):
            reading += 1
            # Prevent this thing from reading forever
            if reading > self._max_light_reading:
                break

        if self._previous_reading is not None:
            # Filter 
            reading = int(self._light_reading_filter_a*reading +\
                    self._light_reading_filter_b*self._previous_reading)

        self._previous_reading = reading
        return reading
