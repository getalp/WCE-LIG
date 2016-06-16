# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 16:08:33 2014
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
def feature_occur_in_translators(file_input_path, file_output_from_translator_path, file_output_path):
    """
    Checking each word (w) of each line (in file_input_path) that exists in respectively line in file_google_translate

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :type file_output_from_translator_path: string
    :param file_output_from_translator_path: contains output from Google/Bing Translator of the same Source Language Corpus. In this file, each line contains the word sequence that is translated by Google Translator System

    :type file_output_path: string
    :param file_output_path: contains the frequency of each word in each line.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file output from translator with format - line."
    is_existed_file(file_output_from_translator_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for reading: file_output_from_translator_path
    file_reader_translator = open(file_output_from_translator_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #number of sentences
    number_of_sentences = 1

    #read data in openned file
    #read 1st line in google tranlator system
    line_translator = file_reader_translator.readline().strip()

    #print(line_translator)

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

            #read next line in google translator system file
            line_translator = file_reader_translator.readline().strip()

            #print(line_translator)

            if len(line_translator)==0:
                #print("End of File - Google Translate")
                break

            number_of_sentences = number_of_sentences + 1

            continue
        #end if

        #print(line)
        #print(line_translator)

        #lowercasing line of google translate
        line_translator = line_translator.lower()

        if is_in_string(line, line_translator):
            file_writer.write('1\n')
        else:
            file_writer.write('0\n')
        #end if
    #end for

    print("input translator: %s" %file_input_path)
    print("output translator: %s" %file_output_path)
    print("Number of sentences is traversed: %d " % number_of_sentences)

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#

if __name__ == "__main__":

    current_config = load_configuration()


    print ('OK')
