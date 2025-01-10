#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 20:40:03 2025

@author: lw

The main class to handle all communication with the heating system.

"""

import serial
import numpy as np
import pandas as pd
from datetime import datetime

class SH40():
    def __init__(self,
                 port,                                
                 baud_rate,                          
                 n_param,                               
                 HighByte,                              
                 interval,                            
                 node,                                  
                 start_byte,
                 end_byte,
                 params):
        
        self.port = 1,
        self.baud_rate = 19200,
        self.n_param = 11                               
        self.HighByte = 0                          
        self.interval = 60                             
        self.node = 8                                
        self.start_byte = '{MC'
        self.end_byte = '}'
        self.params = {'time': datetime.now(),
          'kessel': 8,
          'kesselruecklauf': 9,
          'puffer_unten': 10,
          'puffer_mitte': 11,
          'puffer_oben': 12,
          'boiler': 13,
          'abgas': 15,
          'vorlauf_MK1': 68,
          'aussen_temp': 70,
          'pufferladezustand': 75}

    
    def create_checksum(self):
      pass

    def build_querry_string(self):
      pass
  
    def querry_temperatures(self):
      pass
    
    def decode_response(self):
      pass
