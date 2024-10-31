from oxy_lc import oxy_lc
from time import sleep

device = oxy_lc.OxyLc("COM7")

device.sensor_state = device.SensorState.ON

device.StatusValues.OPERATING

while device.status == device.StatusValues.START_UP:
    print(f"starting up: {device.status}")
    sleep(5)

print(f"System Status = {device.status}")
print(f"Serial Number = {device.serial_number}")
print(f"Date of manufacture = {device.day_of_manufacture}:{device.year_of_manufacture}")
print(f"Current Heater voltage = {device.heater_voltage}")



while True:
    o2_average = device.o2_average
    asymmetry = device.asymmetry
    td_average = device.td_average
    pressure = device.pressure
    print(f"{o2_average = }\t{asymmetry = }\t{td_average = }\t{pressure = }")
    sleep(2)
    
    if any(device.warnings[k] for k in device.warnings):
        print(device.warnings)
        break

