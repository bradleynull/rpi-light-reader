#! /usr/bin/python2.7
import LightReader
import time
import signal
import sys

def SignalHandler(signal, frame):
    """
    Handle SIGINT by setting the global running value to false. This creates
    a symbiotic relationship with Run() but its the best I could come up with.
    """
    global running
    running = False

def Run():
    """ 
    Read the light readers light diode then flash the lights based on the
    output. The more lights the less light and vice versa. 
    """
    # Set up to handle SIGINT (ctrl-c)
    global running 
    running = True
    signal.signal(signal.SIGINT, SignalHandler)

    # Create the light reader and turn the lights on for a second
    light_reader = LightReader.LightReader()
    light_reader.TurnOnAllLed()
    time.sleep(1)
    # Run until we see a ctrl-c
    while running:
        light = light_reader.ReadLight()
        # The higher the count the less light there is in the room
        if light < 500:
            light_reader.ToggleLed(["red"], ["yellow", "green"])
        elif light < 1000:
            light_reader.ToggleLed(["red", "yellow"], ["green"])
        else:
            light_reader.ToggleLed(["red", "yellow", "green"])

if __name__ == "__main__":
    Run()
