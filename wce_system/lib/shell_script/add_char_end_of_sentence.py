#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 13:24:12 2014
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
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *

#**************************************************************************#
def add_point_end_of_sentence(file_input_path, file_output_path):
    """
    Checking the point end of each line (in file_input_path). If not existed then we should add one point

    :type file_input_path: string
    :param file_input_path: contains corpus with format from TreeTagger.

    :type file_output_path: string
    :param file_output_path: contains corpus with format from TreeTagger; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, 'w')

    default_end_of_sentence = "."
    list_char_end_of_sentence = [default_end_of_sentence, "!","?", "..."]

    number_of_sentence = 1
    sum_number_of_sentence = 0

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        line_split = line.split() #delimiter = space character

        char_lastest = line_split[len(line_split)-1]

        #if not is_in_list(char_lastest, list_char_end_of_sentence):
        if not char_lastest in list_char_end_of_sentence:
            line = line + " " + default_end_of_sentence
            sum_number_of_sentence = sum_number_of_sentence + 1
            print("Dong khong co dau ket thuc cau: %d" %number_of_sentence)


        file_writer.write(line)
        file_writer.write("\n")
        number_of_sentence = number_of_sentence + 1

    print("Tong so Dong khong co dau ket thuc cau: %d" %sum_number_of_sentence)
    #end for

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
if __name__ == "__main__":
    #Test case:

    #current_config = load_configuration()

    #add_point_end_of_sentence(current_config.SRC_REF_TEST, "../corpus/fr_en_10881_v2/SRC_FR/src-ref-tst.lc.np.tk.de_special_chars3.fr")

    #add_point_end_of_sentence(current_config.TARGET_REF_TEST, "../corpus/fr_en_10881_v2/TGT_EN/my_tgt-mt-tst.lc.np.tk.de_special_chars3.en")

    #python my_prog.py file_name.txt
    #import sys
    #print sys.argv

    #sys.argv is a list where 0 is the program name,
    #so in the above example sys.argv[1] would be "file_name.txt"
    #updated for using command line in "preprocessing/my_preprocessing.sh" 2014.Dec.14
    add_point_end_of_sentence(sys.argv[1], sys.argv[2])
