#!/usr/bin/python

import debug


if debug.RELAY_TEST == 0:
    import RPi.GPIO as GPIO
else:
    import DUMMY_GPIO as GPIO
    print "DEBUG RELAY"


class Relay(object):
    OFF = 0
    ON = 1
    FOFF = 2
    FON = 3
    UNKNOWN = 4

    def __init__(self, pin):
        super(Relay, self).__init__()
        self.pin = pin
        self.controller = None
        self.controller_or = None
        self.controller_and = None
#        self._logger = logg.TankLog()
        self.avg = []
        self.moving_total = 0.0
        self.controller_state = 99
        self.current_state = Relay.UNKNOWN

    def init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.turn_relay_off()

    def turn_relay_on(self):
        if self.current_state != Relay.ON:
            GPIO.output(self.pin, GPIO.LOW)
        self.current_state = Relay.ON

    def turn_relay_off(self):
        if self.current_state != Relay.OFF:
            GPIO.output(self.pin, GPIO.HIGH)
        self.current_state = Relay.OFF
