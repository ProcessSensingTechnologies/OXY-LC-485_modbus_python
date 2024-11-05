# OXY-LC-485 Modbus Communication with Python

See UG-004_OXY-LC-User-Guide for full implementation details for modbus with OXY-LC

This repository provides Python code for interacting with an OXY-LC-485 oxygen sensor using the Modbus RTU protocol.

## Getting Started

### Prerequisites

- Python 3.11 or newer (https://www.python.org/downloads/)
    - Older Python revisions are untested but may work.
- A Python library for Modbus communication:
    - Recommended: minimalmodbus (lightweight, easy-to-use) - https://minimalmodbus.readthedocs.io/en/stable/
- A USB-to-RS485 converter compatible with your system and the OXY-LC-485.
    - Recommended: RS-485 FTDI cable, USB-RS485-WE-1800-BT
- Suitable power supply for OXY-LC-485
- SST Zirconia Oxygen sensor connected to OXY-LC-485


### Installation

#### Clone this repository:


```bash
git clone https://github.com/ProcessSensingTechnologies/OXY-LC-485_Modbus_Python.git
```

#### Install dependencies:

*It is highly recommended to use a virtual environment to isolate your project's dependencies and avoid conflicts with other Python projects.*
```Bash
cd OXY-LC-485_Modbus_Python

python -m pip install -r requirements.txt
```
## Usage
Import OXY-LC-485 into the main script and initialise the device providing the portname and slave address. Use the provided methods to get/set data to and from the device.

Detailed documentation can be found [here](https://processsensingtechnologies.github.io/OXY-LC-485_modbus_python/oxy_lc.html)

For a detailed example of how to use this library, please refer to the provided script example_1.py. This script demonstrates how to connect to the OXY-LC-485, read sensor data, and perform other common tasks.

To run the example from the root folder it can be run as a module: `python -m examples.example_1`

## Additional Notes

Refer to the OXY-LC-485 Modbus register map in UG-004_OXY-LC-User-Guide for details on available registers for reading/writing data.

This is a basic example. You can modify the script to handle specific sensor data parsing, error handling,  and other functionalities as needed.

## Contributing

Please feel free to open issues for support or to suggest changes.

## License

This repository is licensed under the BSD 3-Clause License. See the LICENSE file for details.
