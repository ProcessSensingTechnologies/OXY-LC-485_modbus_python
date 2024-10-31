import minimalmodbus
from .utilities.modbus_registers import HoldingRegister, InputRegister
from .utilities.conversions import twos_compliment
from enum import IntEnum
from time import sleep

# region Errors


class ValueRangeError(Exception):
    """Exception raised for value range error scenarios.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# endregion


class OxyLc(minimalmodbus.Instrument):
    """
    Main object for OxyLC communication

    :param minimalmodbus: Child of minimalmodbus to use all included methods as standard
    """

    def __init__(self, portname: str, slaveaddress: int = 1):
        """
        Initialiser for OxyLC communication. This should setup the connection to the device at the required protocol.

        :param portname: Portname for the connection. Likely "COM*" on windows or "/dev/ttyUSB*" in Linux
        :type portname: str
        :param slaveaddress: Slave address of the device. Unless changed by the user this defaults to 1 on new products.
        :type slaveaddress: int
        """
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = 9600

    # region enums

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

    class HeaterOptions(IntEnum):
        HEATER_4V0 = 0
        HEATER_4V2 = 1
        HEATER_4V35 = 2
        HEATER_4V55 = 3

    class SaveAndApply(IntEnum):
        IDLE = 0
        APPLY = 1

    class CalibrationStatus(IntEnum):
        IDLE = 0
        IN_PROGRESS = 1
        COMPLETED = 2

    class CalibrationControl(IntEnum):
        DEFAULT = 0
        ACTIVATE = 1
        RESET = 2

    class BaudRates(IntEnum):
        _2400 = 0
        _4800 = 1
        _9600 = 2
        _19200 = 3
        _38400 = 4
        _57600 = 5
        _115200 = 6

    class Parity(IntEnum):
        NONE = 0
        ODD = 1
        EVEN = 2

    class StopBits(IntEnum):
        _1 = 0
        _2 = 1

    class RS485ApplyChanges(IntEnum):
        IDLE = 0
        APPLY = 1

    # endregion

    # region Properties

    @property
    def o2_average(self) -> float:
        """
        Get live sensor reading - O2 Average

        :return: Current averaged O2 reading from the sensor (%)
        :rtype: float
        """
        o2_reading = self.read_register(InputRegister.O2_AVERAGE, functioncode=4)
        return o2_reading / 100

    @property
    def o2_raw(self) -> float:
        """
        Get live sensor reading - O2 raw

        :return: Current raw O2 reading from the sensor (%)
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

    @property
    def sensor_state(self) -> SensorState:
        """
        Get live sensor reading - Sensor State

        :return: Current state of the sensor
        :rtype: SensorState
        """
        _sensor_state = self.read_register(HoldingRegister.SENSOR_STATE, functioncode=3)
        return self.SensorState(_sensor_state)

    @sensor_state.setter
    def sensor_state(self, state: SensorState) -> None:
        """
        Set the current state of the sensor

        :param state: State option from Enum SensorState
        :type state: SensorState
        """
        self.write_register(HoldingRegister.SENSOR_STATE, state)

    @property
    def heater_voltage(self) -> float:
        """
        Get sensor setting - heater voltage

        :return: Current set heater voltage of the sensor (Volts)
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

    @property
    def warnings(self) -> dict[str:bool]:
        """
        Reads and decodes the warnings and returns a dictionary with each warning/error with a corresponding boolean

        :return: Warning states for each of the representative bits
        :rtype: dict[str: bool]
        """
        warning_states = {
            "Pump Error": False,
            "Heater Voltage Error": False,
            "Asymmetry Warning": False,
            "O2 Low Warning": False,
            "Pressure Sensor Warning": False,
            "Pressure Sensor Error": False,
        }
        warnings_hex = self.read_register(InputRegister.WARNINGS, functioncode=4)

        decode_to_bits = f"{warnings_hex:08b}"

        for count, state in enumerate(warning_states):
            if decode_to_bits[::-1][count] == 1:
                warning_states[state] = True

        return warning_states

    @property
    def td_average(self) -> float:
        """
        Get live sensor TD average

        :return: TD Average (ms)
        :rtype: float
        """
        td_average = self.read_register(InputRegister.TD_AVERAGE, functioncode=4)
        return td_average / 10

    @property
    def td_raw(self) -> float:
        """
        Get live sensor TD raw

        :return: TD raw (ms)
        :rtype: float
        """
        td_raw = self.read_register(InputRegister.TD_RAW, functioncode=4)
        return td_raw / 10

    @property
    def tp(self) -> float:
        """
        Get live sensor TP

        :return: TP (ms)
        :rtype: float
        """
        tp = self.read_register(InputRegister.TP, functioncode=4)
        return tp / 10

    @property
    def t1(self) -> float:
        """
        Get live sensor T1

        :return: T1 (ms)
        :rtype: float
        """
        t1 = self.read_register(InputRegister.T1, functioncode=4)
        return t1 / 10

    @property
    def t2(self) -> float:
        """
        Get live sensor T2

        :return: T2 (ms)
        :rtype: float
        """
        t2 = self.read_register(InputRegister.T2, functioncode=4)
        return t2 / 10

    @property
    def t4(self) -> float:
        """
        Get live sensor T4

        :return: T4 (ms)
        :rtype: float
        """
        t4 = self.read_register(InputRegister.T4, functioncode=4)
        return t4 / 10

    @property
    def t5(self) -> float:
        """
        Get live sensor T5

        :return: T5 (ms)
        :rtype: float
        """
        t5 = self.read_register(InputRegister.T5, functioncode=4)
        return t5 / 10

    @property
    def pp_o2_real(self) -> float:
        """
        Get live ppO2 Real

        :return: ppO2 Real
        :rtype: float
        """
        pp_o2 = self.read_register(InputRegister.PPO2_REAL, functioncode=4)
        return pp_o2 / 10

    @property
    def pp_o2_raw(self) -> float:
        """
        Get live ppO2 raw

        :return: ppO2 raw
        :rtype: float
        """
        pp_o2 = self.read_register(InputRegister.PPO2_RAW, functioncode=4)
        return pp_o2 / 10

    @property
    def pressure(self) -> float:
        """
        Get live pressure

        :return: pressure (mbar)
        :rtype: float
        """
        _pressure = self.read_register(InputRegister.PRESSURE, functioncode=4)
        return _pressure

    @property
    def pressure_sens_temperature(self) -> float:
        """
        Get live temperature of the pressure sensor

        :return: temperature (°C)
        :rtype: float
        """
        temp_decimal = self.read_register(
            InputRegister.PRESSURE_SENS_TEMP, functioncode=4
        )

        converted_temperature = twos_compliment(temp_decimal, 16)

        return converted_temperature

    @property
    def calibration_status(self) -> CalibrationStatus:
        """
        Get current calibration status of the sensor

        :return: calibration status
        :rtype: CalibrationStatus
        """
        _cal_status = self.read_register(
            InputRegister.CALIBRATION_STATUS, functioncode=4
        )
        return self.CalibrationStatus(_cal_status)

    @property
    def year_of_manufacture(self) -> int:
        """
        Get Year of Manufacture

        :return: Year of Manufacture (YYYY)
        :rtype: int
        """
        _year_of_manufacture = self.read_register(InputRegister.YOM, functioncode=4)
        return _year_of_manufacture

    @property
    def day_of_manufacture(self) -> int:
        """
        Get Day of Manufacture

        :return: Day of Manufacture (DDD)
        :rtype: int
        """
        _day_of_manufacture = self.read_register(InputRegister.DOM, functioncode=4)
        return _day_of_manufacture

    @property
    def serial_number(self) -> int:
        """
        Get Serial Number

        :return: Serial Number (XXXXX)
        :rtype: int
        """
        _serial_number = self.read_register(InputRegister.SERIAL_NO, functioncode=4)
        return _serial_number

    @property
    def software_revision(self) -> int:
        """
        Get Software Revision

        :return: Software Revision (RRR)
        :rtype: int
        """
        _software_revision = self.read_register(
            InputRegister.SOFTWARE_REV, functioncode=4
        )
        return _software_revision

    @property
    def calibration_value(self) -> float:
        """
        Return current calibration value

        :return: calibration (%)
        :rtype: float
        """
        _calibration_value = self.read_register(HoldingRegister.CALIBRATION_PERCENT)
        return _calibration_value / 100

    @calibration_value.setter
    def calibration_value(self, value: float) -> None:
        """
        Set the calibration value for the sensor

        :param value: Calibration value between 0% and 100%
        :type value: float
        :raises self.ValueRangeError: Value out of range
        """
        if (value < 0) or (value > 100):
            raise ValueRangeError(
                f"Calibration value {value} out of range. Value Must be between 0 and 100"
            )

        self.write_register(HoldingRegister.CALIBRATION_PERCENT, int(value * 100))

    @property
    def calibration_control(self) -> CalibrationControl:
        """
        Current Calibration control setting

        :return: calibration control
        :rtype: CalibrationControl
        """
        _calibration_control = self.read_register(HoldingRegister.CALIBRATION_CONTROL)
        return self.CalibrationControl(_calibration_control)

    @calibration_control.setter
    def calibration_control(self, control_setting: CalibrationControl) -> None:
        """
        Set calibration control

        :param control_setting: Control setting
        :type control_setting: CalibrationControl
        """
        self.write_register(HoldingRegister.CALIBRATION_CONTROL, control_setting)

    @property
    def address(self) -> int:
        """
        Get device address

        :return: Address (1-247)
        :rtype: int
        """
        _address = self.read_register(HoldingRegister.ADDRESS)
        return _address

    @address.setter
    def address(self, new_address: int) -> None:
        """
        Set new device Address

        :param new_address: between 1 & 247
        :type new_address: int
        :raises ValueRangeError: Address out of range
        """
        if (new_address < 1) or (new_address > 247):
            raise ValueRangeError("Address must be between 1 and 247")

        self.write_register(HoldingRegister.ADDRESS, new_address)

    @property
    def parity(self) -> Parity:
        """
        Get device parity

        :return: parity
        :rtype: Parity
        """
        _parity = self.read_register(HoldingRegister.PARITY)
        return self.Parity(_parity)

    @parity.setter
    def parity(self, new_parity: Parity) -> None:
        """
        Set new device parity

        :param new_parity: new parity from enum
        :type new_parity: Parity
        """
        self.write_register(HoldingRegister.PARITY, new_parity)

    # endregion

    # region Methods

    def calibrate(self, calibration_value: float | None) -> bool:
        """
        Calibrate the sensor to the given percent value

        :param calibration_precent: O2 percent for calibration, defaults to 20.7
        :type calibration_precent: float, optional
        :return: boolean indication of success
        :rtype: bool
        """
        if self.status != self.StatusValues.OPERATING:
            print("Sensor must be in operation to calibrate")
            return False

        if calibration_value:
            try:
                self.calibration_value(calibration_value)
            except ValueRangeError as e:
                print(e)
                return False

        self.calibration_control(self.CalibrationControl.ACTIVATE)

        count = 0
        timeout = 5
        while (self.calibration_status != self.CalibrationStatus.COMPLETED) and (
            count != timeout
        ):
            sleep(1)
            count += 1

        self.write_register(
            HoldingRegister.CALIBRATION_CONTROL, self.CalibrationControl.RESET
        )

        if count == timeout:
            print("calibration timeout")
            return False
        else:
            return True

    def clear_error_flags(self) -> None:
        """
        Clears error flags on the device
        """
        self.write_register(HoldingRegister.CLEAR_FLAGS, 1)

    def set_and_apply_heater_voltage(self, set_voltage: HeaterOptions | None) -> None:
        """
        Set the current heater voltage for the sensor

        :param state: State option from Enum HeaterOptions
        :type state: HeaterOptions
        """
        if set_voltage:
            self.heater_voltage = set_voltage

        # MinimalModbus will throw a NoResonseError when this register is written.
        # It must be passed or it will crash the program
        try:
            self.write_register(
                HoldingRegister.HEATER_VOLTAGE_SAVE, self.SaveAndApply.APPLY
            )
        except minimalmodbus.NoResponseError:
            sleep(2)

        self.sensor_state = self.SensorState.ON

    # endregion
