#!/usr/bin/env python
import datetime
import temp_sensor
import time
import relay


def main():
    sensor = temp_sensor.TempSensor.new(sensor='/sys/bus/w1/devices/28-041501b016ff/w1_slave')
    r = relay.Relay(33) # pin 37,35,33
    r.init()

    relay_state = 0
    now = 0
    lastOn = time.time()
    last_temp = 30.0
    while True:
        while time.time() < now:
            time.sleep(1)
        now = time.time()+60
        sensor.tick()
        sensor.current_value
	
        if sensor.current_value < 21.75:
            if relay_state == 0:
                print("ON "+str(lastOn))
                relay_state = 1
                lastOn = time.time()
                r.turn_relay_on()
                

        if sensor.current_value > 22.00 or last_temp < sensor.current_value:
            print("OFF "+str(lastOn)+" "+str(time.time()))
            relay_state = 0
            #lastOn = time.time()
            r.turn_relay_off()

#        print("XXX "+str(lastOn+130)+" "+str(time.time()))

        last_temp = sensor.current_value

        tm=datetime.datetime.utcnow().isoformat('T')+"000Z"
#        "time:{time}\ttemp:{t}\trelay:{r}".format(time=datetime.datetime.now().isoformat(),t=sensor.current_value, r=relay_state)
        log_fname = r'/var/log/temps/temp.log'
        try:
            with open(log_fname, 'a') as f:
                f.write("time:{time}\ttemp:{t}\trelay:{r}\n".format(time=tm,t=sensor.current_value, r=relay_state))
#                f.write("time:{time}\ttemp:{t}\trelay:{r}\n".format(time=datetime.datetime.now().isoformat(),t=sensor.current_value, r=relay_state))
        except IOError as e:
            print str(e)
            print "Error writing to temp file {f}".format(log_fname)


if __name__ == '__main__':
    main()

