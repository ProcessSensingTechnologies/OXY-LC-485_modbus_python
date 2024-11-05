from oxy_lc import oxy_lc
from time import sleep

device = oxy_lc.OxyLc("COM7")

device.sensor_state = device.SensorState.ON

sleep(2)

print(f"System Status = {device.status}")
print(f"Serial Number = {device.serial_number}")
print(f"Date of manufacture = {device.day_of_manufacture}:{device.year_of_manufacture}")
print(f"Current Heater voltage = {device.heater_voltage}")


while device.status == device.StatusValues.START_UP:
    print(f"Waiting for device to start. Current Status: {device.status.name}")
    sleep(5)


while True:
    o2_average = device.o2_average
    asymmetry = device.asymmetry
    td_average = device.td_average
    pressure = device.pressure
    warnings_bits = device.warnings
    print(f"{o2_average = }\t{asymmetry = }\t{td_average = }\t{pressure = }")
    sleep(2)
    
    warnings_bool = device.display_warnings()
    
    if any(warnings_bool[k] for k in warnings_bool):
        print(warnings_bool)
        break

