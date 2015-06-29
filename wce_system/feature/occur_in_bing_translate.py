# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 16:36:44 2014
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
from common_module.cm_util import is_in_string
from common_module.cm_file import is_existed_file
from common_module.cm_config import load_configuration

#**************************************************************************#
def feature_occur_in_bing_translate(file_input_path, file_bing_translate_path, file_output_path):
    """
    Checking each word (w) of each line (in file_input_path) that exists in respectively line in file_bing_translate

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :type file_bing_translate_path: string
    :param file_bing_translate_path: contains output from bing Translator of the same Source Language Corpus. In this file, each line contains the word sequence that is translated by bing Translator System

    :type file_output_path: string
    :param file_output_path: contains the frequency of each word in each line.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    if not os.path.exists(file_bing_translate_path):
        raise TypeError('Not Existed file file_google_translate with format - line. Each line contains the word sequence.')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file file_bing_translate_path with format - line."
    is_existed_file(file_bing_translate_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for reading: file_bing_translate_path
    file_reader_bing_translate = open(file_bing_translate_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #number of sentences
    number_of_sentences = 1

    #read data in openned file
    #read 1st line in bing tranlator system
    line_bing_translate = file_reader_bing_translate.readline().strip()

    #print(line_bing_translate)

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #print(line)

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')

            #read next line in bing translator system file
            line_bing_translate = file_reader_bing_translate.readline().strip()

            #print(line_bing_translate)

            if len(line_bing_translate)==0:
                #print("End of File - bing Translate")
                break

            number_of_sentences = number_of_sentences + 1

            continue

        #print(line)
        #print(line_bing_translate)

        #lowercasing line of bing translate
        line_bing_translate = line_bing_translate.lower()

        if is_in_string(line, line_bing_translate):
            file_writer.write('1\n')
        else:
            file_writer.write('0\n')
        #end if
    #end for

    print("input bing: %s" %file_input_path)
    print("output bing: %s" %file_output_path)
    print("Number of sentences is traversed: %d " % number_of_sentences)

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#

if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()

    feature_occur_in_bing_translate( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.BING_TRANSLATE_CORPUS, current_config.OCCUR_IN_BING_TRANSLATE)


    print ('OK')