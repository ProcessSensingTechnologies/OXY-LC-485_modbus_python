from oxy_lc import oxy_lc
from time import sleep

device = oxy_lc.OxyLc("COM4", 1)

device.set_sensor_state(oxy_lc.SensorState.ON)

while device.get_status() == oxy_lc.StatusValues.START_UP:
    print(f"starting up: {device.get_status()}")
    sleep(5)


while True:
    o2_average = device.get_o2_average()
    print(f"{o2_average = }")
    sleep(2)
