from machine import Pin, time_pulse_us
from micropython import const
from utime import sleep_us


class Sensor:
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):

        self.echo_timeout_us = echo_timeout_us
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def get_pulse_time(self):

        self.trigger.value(0)
        sleep_us(5)
        self.trigger.value(1)
        sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            if pulse_time < 0:
                MAX_RANGE_IN_CM = const(500)
                pulse_time = int(MAX_RANGE_IN_CM * 29.1)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:
                raise OSError('Out of range')
            raise ex

    def distance(self):

        pulse_time = self.get_pulse_time()
        result = (pulse_time / 2) / 29.1
        return result


def main():
    led = Pin(2, Pin.OUT)
    sensor = Sensor(trigger_pin=5, echo_pin=18, echo_timeout_us=1000000)

    while True:
        if sensor.distance() < 10:
            led.on()
        else:
            led.off()


main()