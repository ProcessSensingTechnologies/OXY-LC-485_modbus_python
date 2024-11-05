from enum import IntEnum

class InputRegister(IntEnum):
    """
    Enum for use to convert to the device input registers

    :param IntEnum: InputRegister
    :type IntEnum
    """
    O2_AVERAGE = 30001
    O2_RAW = 30002
    ASYMMETRY = 30003
    SYSTEM_STATUS = 30004
    WARNINGS = 30005
    HEATER_VOLTAGE = 30006
    TD_AVERAGE = 30007
    TD_RAW = 30008
    TP = 30009
    T1 = 30010
    T2 = 30011
    T4 = 30012
    T5 = 30013
    PPO2_REAL = 30014
    PPO2_RAW = 30015
    PRESSURE = 30016
    PRESSURE_SENS_TEMP = 30017
    CALIBRATION_STATUS = 30018
    YOM = 30019
    DOM = 30020
    SERIAL_NO = 30021
    SOFTWARE_REV = 30022

class HoldingRegister(IntEnum):
    """
    Enum for use to convert to the device holding registers

    :param IntEnum: InputRegister
    :type IntEnum
    """
    SENSOR_STATE = 40001
    CLEAR_FLAGS = 40002
    SHUTDOWN_DELAY = 40003
    CALIBRATION_CONTROL = 40004
    CALIBRATION_PERCENT = 40005
    ADDRESS = 40006
    BAUD = 40007
    PARITY = 40008
    STOPBITS = 40009
    RS485_SETUP_SAVE = 40010
    HEATER_VOLTAGE = 40011
    HEATER_VOLTAGE_SAVE = 40012
