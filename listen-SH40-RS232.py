#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 20:47:03 2025

@author: lw

V0.2

This is the main script which will execute a query loop to periodically get SH40 actuals.
Potential upload to an influxd instance following later.

"""

import serial
import time
import pandas as pd
from datetime import datetime

        


#%% dictionary and functions to correctly assemple the querystring


def string_to_hex(s):
    hex_output = ''.join(format(ord(char), '02x') for char in s)
    return hex_output

def string_to_hex2(s):
    hex_output = ''.join(f'0x{format(ord(char), "02x")}' for char in s)
    return hex_output

def calculate_checksum(length_byte, payload):
    checksum = (int(length_byte, 16) + sum(int(byte, 16) for byte in payload)) % 256
    return checksum

temp_directory = {'Kessel': ('0x08', '0x00', '8'),
                  'Abgas': ('0x08', '0x00', '15'),
                  'Boiler': ('0x08', '0x00', '13'), #13 != SH20 guide
                  'Pufferladezustand': ('0x08', '0x00', '75'),
                  'Puffer_oben': ('0x08', '0x00', '12'),
                  'Puffer_mitte': ('0x08', '0x00', '11'),
                  'Puffer_unten': ('0x08', '0x00', '10'),
                  'Kesselruecklauf': ('0x08', '0x00', '9'),
                  'Aussentemp': ('0x08', '0x00', '70'),
                  'Vorlauf_MK1': ('0x08', '0x00', '68')}  

 
temps_selected = ['Boiler', 'Aussentemp'] 
payload = [temp_directory[temp][i] for temp in temps_selected for i in range(3)]

packet_STOP = '{ME00}'
packet_start = '{MC'
interval = '0x0a' 
packet_end = '}'

length = '0' + str(1 + 3 * len(temps_selected)) if (1 + 3 * len(temps_selected)) < 10 else str(1 + 3 * len(temps_selected))

payload = ''.join(temp_directory['Boiler', 'Aussentemp'])

# style: STARTbyte + length + checksum + interval + __payload__ + ENDbyte


packet = (
    string_to_hex2(packet_start)
    + length
    + calculate_checksum('0x0a', payload)
    + interval
    + payload
    + string_to_hex2(packet_end))



#%% connecting and listening

      
# Configuration for serial connection
rs232 = serial.Serial(
    port='COM1',
    baudrate='19200',
    parity=serial.PARITY_NONE,
    timeout=3
)  
      

rs232.write(packet)


        
while True:
    response = rs232.read()
    print(response)
    time.sleep(30)
           

def stop_data_subscription():
        # stop: {ME00}
        rs232.write(string_to_hex2('{ME00}'))
        rs232.close()
        
stop_data_subscription()


#%% two strings for testing that should work

teststring_boiler = '{MC 04 31 0x0a 0x08 0x00 0x0d}'
teststring_boiler_aussentemp = '{MC 07 109 0x0a 0x08 0x00 0x0d 0x08 0x00 70}'

#%% testing the checksum calculation method

# Example payloads
payload_boiler = ['0x08', '0x00', '0x0d']
payload_boiler_aussentemp = ['0x08', '0x00', '0x0d', '0x08', '0x00', '0x46']

# Length byte based on the number of data points (1 for Boiler, 2 for Boiler and Aussentemperatur)
length_byte_boiler = '0x0a'  # 7 for Boiler (1 + 3*1 + 1)
length_byte_boiler_aussentemp = '0x0a'  # 10 for Boiler and Aussentemperatur (1 + 3*2 + 1)

# Calculate checksums for examples
checksum_boiler = calculate_checksum(length_byte_boiler, payload_boiler)
checksum_boiler_aussentemp = calculate_checksum(length_byte_boiler_aussentemp, payload_boiler_aussentemp)

print(f"Checksum for Boiler (should be 31): {checksum_boiler}")
print(f"Checksum for Boiler and Aussentemperatur (should be 109): {checksum_boiler_aussentemp}")
