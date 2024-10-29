import minimalmodbus
from .utilities.modbus_registers import HoldingRegister, InputRegister
from enum import IntEnum


class OxyLc(minimalmodbus.Instrument):
    """
    Main object for OxyLC communication

    :param minimalmodbus: Child of minimalmodbus to use all included methods as standard
    """

    def __init__(self, portname: str, slaveaddress: int):
        """
        Initialiser for OxyLC communication. This should setup the connection to the device at the required protocol.

        :param portname: Portname for the connection. Likely "COM*" on windows or "/dev/ttyUSB*" in Linux
        :type portname: str
        :param slaveaddress: Slave address of the device. Unless changed by the user this defaults to 1 on new products.
        :type slaveaddress: int
        """
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = 9600

    @property
    def o2_average(self) -> float:
        """
        Get live sensor reading - O2 Average

        :return: Current averaged O2 reading from the sensor
        :rtype: float
        """
        o2_reading = self.read_register(InputRegister.O2_AVERAGE, functioncode=4)
        return o2_reading / 100

    @property
    def o2_raw(self) -> float:
        """
        Get live sensor reading - O2 raw

        :return: Current raw O2 reading from the sensor
        :rtype: float
        """
        o2_reading = self.read_register(InputRegister.O2_RAW, functioncode=4)
        return o2_reading / 100

    @property
    def asymmetry(self) -> float:
        """
        Get live sensor reading - O2 asymmetry

        :return: Current asymmetry of the sensor
        :rtype: float
        """
        asymmetry_reading = self.read_register(InputRegister.ASYMMETRY, functioncode=4)
        return asymmetry_reading / 1000

    class StatusValues(IntEnum):
        IDLE = 0
        START_UP = 1
        OPERATING = 2
        SHUT_DOWN = 3
        STANDBY = 4

    @property
    def status(self) -> StatusValues:
        """
        Get live sensor reading - current device status
        Returned as Enum from StatusValues

        :return: Current status of the device
        :rtype: StatusValues
        """
        status = self.read_register(InputRegister.SYSTEM_STATUS, functioncode=4)
        return self.StatusValues(status)

    class SensorState(IntEnum):
        OFF = 0
        ON = 1
        STANDBY = 2

    @property
    def sensor_state(self) -> SensorState:
        """
        Get live sensor reading - Sensor State

        :return: Current state of the sensor
        :rtype: SensorState
        """
        _sensor_state = self.read_register(HoldingRegister.SENSOR_STATE, functioncode=6)
        return self.SensorState(_sensor_state)

    @sensor_state.setter
    def set_sensor_state(self, state: SensorState) -> None:
        """
        Set the current state of the sensor

        :param state: State option from Enum SensorState
        :type state: SensorState
        """
        self.write_register(HoldingRegister.SENSOR_STATE, state)

    class HeaterOptions(IntEnum):
        Heater_4V0 = 0
        Heater_4V2 = 1
        Heater_4V35 = 2
        Heater_4V55 = 3

    class SaveAndApply(IntEnum):
        Idle = 0
        Apply = 1

    @property
    def heater_voltage(self) -> float:
        """
        Get sensor setting - heater voltage

        :return: Current set heater voltage of the sensor
        :rtype: float
        """
        _heater_Voltage = self.read_register(
            InputRegister.HEATER_VOLTAGE, functioncode=4
        )
        return _heater_Voltage / 100

    @heater_voltage.setter
    def heater_voltage(self, set_voltage: HeaterOptions) -> None:
        """
        Set the current heater voltage for the sensor

        :param state: State option from Enum HeaterOptions
        :type state: HeaterOptions
        """
        self.write_register(HoldingRegister.HEATER_VOLTAGE, set_voltage)
        self.write_register(
            HoldingRegister.HEATER_VOLTAGE_SAVE, self.SaveAndApply.Apply
        )
