from oxy_lc import oxy_lc
from time import sleep

device = oxy_lc.OxyLc("COM4")

device.sensor_state = device.SensorState.ON

device.StatusValues.OPERATING

while device.status() == device.StatusValues.START_UP:
    print(f"starting up: {device.status}")
    sleep(5)


while True:
    o2_average = device.o2_average()
    print(f"{o2_average = }")
    sleep(2)
