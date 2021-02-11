#! python3
# coding: utf-8
import logging
import os

def _get_name(line):
    return line.split(':')[0].upper()

def _get_value(line):
    return float( line.split('=')[1].split(' ')[0] )

def pars_log_file(file):
    data = dict()
        
    with open(os.path.normpath(file), encoding="ansi") as log_file:
        for line in log_file:
            if 'FROM' in line:
                data[_get_name(line)] = _get_value(line) 
                
    logging.info('pars finished!')
    return data

   
       