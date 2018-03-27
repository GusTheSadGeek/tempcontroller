import datetime
import temp_sensor
import time
import relay


def main():
    sensor = temp_sensor.TempSensor.new(sensor='/sys/bus/w1/devices/28-041501b016ff/w1_slave')
    r = relay.Relay(37) # pin 37,35,33
    r.init()

    relay_state = 0
    now = 0
    while True:
        while time.time() < now:
            time.sleep(1)
        now = time.time()+10
        sensor.tick()
        sensor.current_value
        if sensor.current_value < 24:
            relay_state = 1
            r.turn_relay_on()
        if sensor.current_value > 25:
            relay_state = 0
            r.turn_relay_off()
        "time:{time}\ttemp:{t}\trelay:{r}".format(time=datetime.datetime.now().isoformat(),t=sensor.current_value, r=relay_state)
        log_fname = r'/home/gus/git/tempcontroller/temp/temp.log'
        try:
            with open(log_fname, 'a') as f:
                f.write("time:{time}\ttemp:{t}\trelay:{r}\n".format(time=datetime.datetime.now().isoformat(),t=sensor.current_value, r=relay_state))
        except IOError as e:
            print str(e)
            print "Error writing to temp file {f}".format(log_fname)


if __name__ == '__main__':
    main()

