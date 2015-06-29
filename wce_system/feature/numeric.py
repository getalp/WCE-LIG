# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 11:31:44 2014
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

import os
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
from common_module.cm_file import is_existed_file
from common_module.cm_config import load_configuration
from common_module.cm_util import  is_numeric
#**************************************************************************#
def feature_numeric(file_input_path, file_output_path):
    """
    Checking each word (w) of each line (in file_input_path)
    if w is a number:
        return 1
    else:
        return 0

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :type file_output_path: string
    :param file_output_path: contains corpus with format each "word" in each line is 1 or 0; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
        elif is_numeric(line):#check line is a numeric or not
            file_writer.write('1\n')
        else:
            file_writer.write('0\n')

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    #feature_numeric(file_input_path, file_output_path)
    #feature_numeric('../corpus/corpus.lc.en.column.txt','../extracted_features/corpus.lc.en.column.feature_numeric.txt')

    current_config = load_configuration()

    print('raw corpus')
    print (current_config.TARGET_REF_TEST_FORMAT_COL)

    print('output')
    print(current_config.NUMERIC)

    feature_numeric( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.NUMERIC)

    print ('OK')