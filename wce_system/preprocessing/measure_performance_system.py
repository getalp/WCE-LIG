# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 18:02:06 2015
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
import datetime

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from feature.common_functions import *
from config.configuration import *
#**************************************************************************#
def get_duration(datetime_start, datetime_end):
    dt1 = datetime.datetime.strptime(datetime_start, '%Y-%m-%d %H:%M:%S.%f')
    dt2 = datetime.datetime.strptime(datetime_end, '%Y-%m-%d %H:%M:%S.%f')

    duration = dt2-dt1
    return duration
#**************************************************************************#
"""
noruego	NOUN
de	OTHER
"""
def count_num_of_words_for_polysemy_count_target(file_input_path):
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    #end if

    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    num_of_words_all = 0
    num_of_words_other = 0

    str_other = "OTHER"
    for line in file_reader:
        line = line.strip()

        if len(line) == 0:
            continue
        #end if

        num_of_words_all += 1

        items = split_string_to_list_delimeter_tab(line)
        if items[1].strip() == str_other:
            num_of_words_other += 1
        #end if
    #end for

    #close file
    file_reader.close()

    num_of_words_result = num_of_words_all - num_of_words_other

    print("num_of_words_all = %d" %num_of_words_all)
    print("num_of_words_result = %d" %num_of_words_result)

#**************************************************************************#
def convert_from_second_to_format_h_m_s(num_of_second):
    m, s = divmod(num_of_second, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("d:h:m:s = %d:%d:%02d:%02d" % (d, h, m, s))
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()

    datetime_start="2015-03-31 20:09:23.282432"
    datetime_end="2015-04-01 00:25:42.996360"

    dt = get_duration(datetime_start, datetime_end)

    print(dt)

    file_input_path = current_config.BABEL_NET_CORPUS_ES
    count_num_of_words_for_polysemy_count_target(file_input_path)

    convert_from_second_to_format_h_m_s(449369)

    print ('OK')