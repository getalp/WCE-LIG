# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 16:17:05 2014
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
#from config.configuration import *
from common_module.cm_config import load_configuration
from common_module.cm_file import count_number_of_words_in_sentences, verify_result_old_and_new

#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    current_config = load_configuration()


    #Copy from "count_number_of_words_in_sentences.py"
    print("*"*57)
    print("*"*57)

    file_input_path_ref = current_config.PUNCTUATION
    file_output_path_ref = "/home/lent/Develops/Solution/ce_system/ce_system/preprocessing/kiem_tra_thieu_dong/PUNCTUATION.txt"

    print('input')
    print (file_input_path_ref)
    print('output')
    print(file_output_path_ref)
    count_number_of_words_in_sentences(file_input_path_ref, file_output_path_ref)

    file_input_path_test = current_config.ALIGNMENT_FEATURES
    file_output_path_test = "/home/lent/Develops/Solution/ce_system/ce_system/preprocessing/kiem_tra_thieu_dong/ALIGNMENT_FEATURES.txt"

    print('input')
    print (file_input_path_test)
    print('output')
    print(file_output_path_test)
    count_number_of_words_in_sentences(file_input_path_test, file_output_path_test)

    print("*"*57)
    print("*"*57)

    file_output_path = current_config.VERIFY_RESULT_OLD_AND_NEW

    print('output')
    print(file_output_path)

    verify_result_old_and_new(file_output_path_ref, file_output_path_test, file_output_path)

    print ('OK')
