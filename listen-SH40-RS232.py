#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 20:47:03 2025

@author: lw

V0.1

This is the main script which will execute a query loop to periodically get SH40 actuals.
Potential upload to an influxd instance following later.

"""

import serial
import time
import pandas as pd
from datetime import datetime

        

def string_to_hex(s):
    hex_output = ''.join(format(ord(char), '02x') for char in s)
    return hex_output

def string_to_hex2(s):
    hex_output = ''.join(f'0x{format(ord(char), "02x")}' for char in s)
    return hex_output

temp_directory = {'Kessel': ('0x08', '0x00', '8'),
                  'Abgas': ('0x08', '0x00', '15'),
                  'Boiler': ('0x08', '0x00', '13'),
                  'Pufferladezustand': ('0x08', '0x00', '75'),
                  'Puffer_oben': ('0x08', '0x00', '12'),
                  'Puffer_mitte': ('0x08', '0x00', '11'),
                  'Puffer_unten': ('0x08', '0x00', '10'),
                  'Kesselruecklauf': ('0x08', '0x00', '9'),
                  'Aussentemp': ('0x08', '0x00', '70'),
                  'Vorlauf_MK1': ('0x08', '0x00', '68')}   

temps_selected = []  # names of values to request go here

packet_STOP = '{ME00}'
packet_start = '{MC'
interval = '0x0a' 
packet_end = '}'

length = '0' + str(1 + 3 * len(temps_selected)) if (1 + 3 * len(temps_selected)) < 10 else str(1 + 3 * len(temps_selected))


# style: STARTbyte + length + checksum + interval + __payload__ + ENDbyte
# string_to_hex('{ME00}')
# string_to_hex2('{ME00}')


packet = (
    string_to_hex2(packet_start)
    + length
    # + checksum --- TODO!!
    + interval
    + ''.join(temp_directory['Boiler'])
    + string_to_hex2(packet_end))








#Configuration for serial connection
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
        rs232.write(b"{ME00}")
        rs232.close()
        
stop_data_subscription()

