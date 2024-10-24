from OXY_LC_485 import OXY_LC_485
from time import sleep

device = OXY_LC_485.OxyLc("COM4", 1)

device.set_sensor_state(OXY_LC_485.SensorState.ON)

while device.get_status() == OXY_LC_485.StatusValues.START_UP:
    print(f"starting up: {device.get_status()}")
    sleep(5)


while True:
    o2_average = device.get_o2_average()
    print(f"{o2_average = }")
