#!/usr/bin/env python


"""

.. moduleauthor:: Paul Paukstelis <shocksofmighty@gmail.com>

Driver for SolarEdge inverter, for communication via the Modbus RTU protocol and the SunSpec standard.
This is a read-only driver.


"""

import minimalmodbus
import serial
import time

__author__  = "Paul Paukstelis"
__email__   = "shocksofmighty@gmail.com"
__license__ = "Apache License, Version 2.0"


class SolarEdge( minimalmodbus.Instrument ):
    """Instrument class for SolarEdge Inverter. 
    
    Communicates via Modbus RTU protocol (via RS485), using the *MinimalModbus* Python module.    

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    Implemented with these function codes (in decimal):
        
    ==================  ====================
    Description         Modbus function code
    ==================  ====================
    Read registers      3
    ==================  ====================

    """

    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)

    #default for my SolarEdge with wireless RS485, may need to change
    serial.baudrate = 38400
    serial.timeout = 1.5     #seconds
    
    ## Process value
    
    def get_lifetime(self):
        """Return lifetime production in Watts. Scale factor not yet used"""
        return self.read_long(93)
        
    def get_power(self):
	"""Return the current AC power in Watts using Scale factor which sets decimal point"""
	reg = self.read_registers(83,2)
	scale = minimalmodbus._twoByteStringToNum(minimalmodbus._numToTwoByteString(reg[1]), signed=True)
	power = minimalmodbus._twoByteStringToNum(minimalmodbus._numToTwoByteString(reg[0]), abs(scale), signed=True)
	return power


    def get_power_scale(self):
	return self.read_register(84, signed=True)

    def get_status(self):
        """Return the process value for activity. According to documentation, 1=off, 2=sleep, 4=active"""
        return self.read_register(107)

    def is_active(self):
        """Simple check, see above"""
	status = self.read_register(107)
	if status == 4:
		return True

    def get_serial(self):
        """Return the serial number as a string"""
        return self.read_string(52)

    def get_model(self):
        """Return the inverter model as a string"""
        return self.read_string(20)

