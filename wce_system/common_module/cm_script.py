# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:47:59 2015
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
import stat
#import datetime

#for call shell script
import shlex, subprocess

#**************************************************************************#
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from config.configuration import *
#from config.config_end_user import *
from common_module.cm_config import load_configuration, load_config_end_user
#**************************************************************************#
def execute_script(command_line, path_to_script, current_working_directory):
    #print("Command line:")
    #print(command_line)

    args = shlex.split(command_line)
    #print("args")
    #print(args)

    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    #current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(path_to_script))

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
#**************************************************************************#
def run_chmod(path_to_script):
    #command_line = "chmod -R +x *"
    #execute_script(command_line, path_to_script)
    #os.chmod(path, mode)
    #ref: http://www.tutorialspoint.com/python/os_chmod.htm
    st = os.stat(path_to_script)
    os.chmod(path_to_script, st.st_mode |  stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
#**************************************************************************#
def call_script(command_line, path_to_script):
    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    """
    try:
        current_working_directory = os.getcwd()
    except OSError:
        os.chdir("..")
        current_working_directory = os.getcwd()

    print("current_working_directory")
    print(os.getcwd())
    print("current_working_directory")

    Solution: Remove all of directory of in eval_agent. Then, copy again :)
    """
    current_working_directory = os.getcwd()

    #chmod execute for script
    run_chmod(path_to_script)

    #print("Just for testing :) - BEGIN")
    #print(command_line)
    #print(path_to_script)
    #print("Just for testing :) - END")

    execute_script(command_line, path_to_script, current_working_directory)
#**************************************************************************#
####--> Khong hieu qua vi sau khi export bien moi truong va thoat ra thi bien moi truong bi mat
# --> chuyen ham nay vao trong code shell, ly do: khong the de o level cua python duoc :(
def call_script_included_export(command_line, path_to_script, variable_name, str_current_directory):
    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory

    #variable_name : bien dung de export cac bien moi truong truoc khi thuc hien
    #tam thoi chi chung 1 bien string
    #neu ve sau nhieu bien moi truong thi nen dung dict de xu ly vu nay :)

    #str_current_directory : neu de rong thi export thu muc chua script; neu ".." thi chuyen ra 1 cap; nguoc lai "../../bin" thi export dung string do tinh tu path cua script

    current_working_directory = os.getcwd()

    #chmod execute for script
    run_chmod(path_to_script)

    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    #current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(path_to_script))

    #doi voi constituent FR -bonsai version 3.2
    #export BONSAI=/home/lent/Téléchargements/a_moses/bonsai_v3.2
    new_working_directory = os.getcwd()
    str_command_line_export = "export " + variable_name + "="

    current_config = load_configuration()
    str_visite_precedent = current_config.VISITE_PRECEDENT

    if len(str_current_directory) == 0:
        str_command_line_export += new_working_directory
    elif str_current_directory == str_visite_precedent:
        str_command_line_export += new_working_directory
        str_command_line_export += "/../"
    else:
        str_command_line_export += new_working_directory
        str_command_line_export += str_current_directory

    #run command export
    #print("export command: %s" %str_command_line_export)

    """
    args = shlex.split(str_command_line_export)
    p = subprocess.Popen(args)
    output, err = p.communicate()
    """
    #generate shell script, roi goi lenh chay script
    #generate shell script
    list_of_commands = []

    list_of_commands.append(str_command_line_export)
    create_script_temp(list_of_commands)

    #goi lenh chay
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)

    ##########################################################################################
    ####--> Khong hieu qua vi sau khi export bien moi truong va thoat ra thi bien moi truong bi mat
    # --> chuyen ham nay vao trong code shell, ly do: khong the de o level cua python duoc :(

    #run main script
    args = shlex.split(command_line)
    #print("args")
    #print(args)

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
#**************************************************************************#
def create_script_temp(command_lines):
    """
    Creating script temp for generate shell script from program python

    :type command_line: string
    :param command_line: contains list of command lines
    """
    current_config = load_configuration()

    script_temp_path = current_config.SCRIPT_TEMP

    #open file:
    #for writing: file_output_path
    file_writer = open(script_temp_path, mode = 'w', encoding = 'utf-8')#, 'w')

    file_writer.write("#!/bin/bash")
    file_writer.write("\n") #empty line

    file_writer.write("#Authors: Tien Ngoc LE & Tan Ngoc LE \n")
    file_writer.write("\n") #empty line

    if len(command_lines) == 0:
        raise Exception("You should add command lines list...")

    for item in command_lines:
        file_writer.write(item)
        file_writer.write("\n") #empty line

    #close file
    file_writer.close()
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    print("OK")