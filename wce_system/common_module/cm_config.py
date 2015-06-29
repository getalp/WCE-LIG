# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:47:27 2015
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

#**************************************************************************#
import os
import sys
#import re
#import linecache
#import stat
#import datetime

#for call shell script
#import shlex, subprocess

#**************************************************************************#
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from config.configuration import config
from config.config_end_user import config_end_user
#**************************************************************************#
def get_absolute_path_current_module():
    """
    Get the current directory which contains this module.

    :rtype: string of absolute path of file_name
    """

    #get path to current module
    path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return path
#**************************************************************************#
def load_configuration(filename_configuration = "configuration.yml"):
    """
    Load the configuration of this project with file in format YAML

    :rtype: Object config
    """
    #get absolute path to current module
    path = get_absolute_path_current_module()

    #print (path)

    path_to_config_file = path + "/../config/" + filename_configuration

    #print(path_to_config_file)

    #str_message_if_not_existed = "Not Existed file configuration"
    #is_existed_file(path_to_config_file, str_message_if_not_existed)

    return config(path_to_config_file)
#**************************************************************************#
def load_configuration_demo_solution(filename_configuration = "configuration.yml"):
    """
    Load the configuration of this project with file in format YAML

    :rtype: Object config
    """
    #get absolute path to current module
    path = get_absolute_path_current_module()

    #print (path)

    path_to_config_file = path + "/config/" + filename_configuration

    #print(path_to_config_file)

    return config(path_to_config_file)
#**************************************************************************#
def load_config_end_user(filename_configuration = "config_end_user.yml"):
    """
    Load the configuration of this project with file in format YAML

    :rtype: Object config
    """
    #get absolute path to current module
    path = get_absolute_path_current_module()

    #print (path)

    #path_to_config_file = path + "/../config/" + filename_configuration
    path_to_config_file = path + "/../../input_data/" + filename_configuration

    #print(path_to_config_file)

    #tra ve ham khoi tao cua module thich hop
    return config_end_user(path_to_config_file)
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    print("OK")