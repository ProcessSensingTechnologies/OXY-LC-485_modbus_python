import minimalmodbus
from utilities import ModbusRegisters
from enum import IntEnum, auto


class StatusValues(IntEnum):
    IDLE = 0
    START_UP = 1
    OPERATING = 2
    SHUT_DOWN = 3
    STANDBY = 4


class SensorState(IntEnum):
    OFF = 0
    ON = 1
    STANDBY = 2


class OxyLc(minimalmodbus.Instrument):
    """
    Instrument class for SST OXY-LC-485.

    Args:
        portname (str): PortName of the device windows example: "COM3"
        slaveaddress (int): Slave address of the device
    """

    def __init__(self, portname: str, slaveaddress: int):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = 9600
        self._heater_Voltage = None

    def get_o2_average(self) -> float:
        o2_reading = self.read_register(
            ModbusRegisters.InputRegister.O2_AVERAGE, functioncode=4
        )
        return o2_reading / 100

    def get_o2_raw(self) -> float:
        o2_reading = self.read_register(
            ModbusRegisters.InputRegister.O2_RAW, functioncode=4
        )
        return o2_reading / 100

    def get_asymmetry(self) -> float:
        asymmetry_reading = self.read_register(
            ModbusRegisters.InputRegister.ASYMMETRY, functioncode=4
        )
        return asymmetry_reading / 1000

    class StatusValues(IntEnum):
        IDLE = 0
        START_UP = 1
        OPERATING = 2
        SHUT_DOWN = 3
        STANDBY = 4

    def get_status(self) -> int:
        status = self.read_register(
            ModbusRegisters.InputRegister.SYSTEM_STATUS, functioncode=4
        )
        return StatusValues(status).name

    def set_sensor_state(self, state: SensorState) -> None:
        self.write_register(ModbusRegisters.HoldingRegister.SENSOR_STATE, state)

    class HeaterOptions(IntEnum):
        Heater_4V0 = 0
        Heater_4V2 = 1
        Heater_4V35 = 2
        Heater_4V55 = 3

    class SaveAndApply(IntEnum):
        Idle = 0
        Apply = 1

    @property
    def heater_voltage(self):
        self._heater_Voltage = self.read_register(
            ModbusRegisters.InputRegister.HEATER_VOLTAGE, functioncode=4
        )
        return self._heater_Voltage

    @heater_voltage.setter
    def heater_voltage(self, set_voltage: HeaterOptions):
        self.write_register(ModbusRegisters.HoldingRegister.HEATER_VOLTAGE, set_voltage)
        self.write_register(
            ModbusRegisters.HoldingRegister.HEATER_VOLTAGE_SAVE, self.SaveAndApply.Apply
        )
