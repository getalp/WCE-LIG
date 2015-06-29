# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 10:54:27 2014
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
from common_module.cm_file import get_list_from_file, is_existed_file
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_util import  is_in_list
#**************************************************************************#
def feature_stop_word(file_input_path, file_list_stop_word_path, file_output_path):
    """
    Checking each word (w) of each line (in file_input_path) and list of stop-words (in file_list_stop_word_path)
    if w in list:
        return 1
    else:
        return 0

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :type file_list_stop_word_path: string
    :param file_list_stop_word_path: contains the stop-words with format "each line is a stop word"

    :type file_output_path: string
    :param file_output_path: contains corpus with format each "word" in each line is 1 or 0; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    if not os.path.exists(file_list_stop_word_path):
        raise TypeError('Not Existed file List Of Stop-words')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file List Of Stop-words"
    is_existed_file(file_list_stop_word_path, str_message_if_not_existed)

    #get list of stop-words
    list_of_stop_words = get_list_from_file(file_list_stop_word_path)

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
        elif is_in_list(line, list_of_stop_words):#check existed line in list of stop-words --> True
            file_writer.write('1\n')
        else:
            file_writer.write('0\n')

    #close 2 files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
def get_feature_stop_word(file_input_path, target_language, file_output_path):
    current_config = load_configuration()

    file_list_stop_word_path = ""
    if target_language == current_config.LANGUAGE_SPANISH:
        file_list_stop_word_path = current_config.LIST_STOP_WORDS_ES
    elif target_language == current_config.LANGUAGE_ENGLISH:
        file_list_stop_word_path = current_config.LIST_STOP_WORDS_EN
    #end if

    feature_stop_word(file_input_path, file_list_stop_word_path, file_output_path)
#**************************************************************************#
if __name__ == "__main__":
    #Test case 1: Check function get_list_of_stop_words
    #result: passed
    #list = get_list_from_file("../lib/english_stop_words.txt")
    #print(list)

    #Test case 2:
    #feature_stop_word(file_input_path, file_list_stop_word_path, file_output_path)
    #feature_stop_word('../corpus/corpus.lc.en.column.txt','../lib/english_stop_words.txt','../extracted_features/corpus.lc.en.column.feature_stop_word.txt')


    current_config = load_configuration()
    #target_language = current_config.LANGUAGE_SPANISH

    config_end_user = load_config_end_user()

    #You should update target language
    target_language = config_end_user.TARGET_LANGUAGE

    #print('List of Stop_Words')
    #list = get_list_from_file(current_config.LIST_STOP_WORDS)
    #print(list)

    #feature_stop_word(current_config.RAW_CORPUS,current_config.LIST_STOP_WORDS, current_config.STOP_WORD)
    #for spanish
    #feature_stop_word( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.LIST_STOP_WORDS_ES, current_config.STOP_WORD)

    get_feature_stop_word( current_config.TARGET_REF_TEST_FORMAT_COL, target_language, current_config.STOP_WORD)

    print ('OK')

    #BEGIN - Added Codes - 2014/12/03
    #Purpose: Read and creating "a_full_stopwords_en.txt" that combines from 4 files such as "bnc_stopwords_en.txt", "english_stop_words.txt", "stopwords_en.txt", "stopwords_online_en.txt" in directory "/lib/stopwords"

    """
    ref: http://www.warriorforum.com/search-engine-optimization/907577-stop-words-keyword-url.html

    #Most search engines do not consider extremely common words in order to speed up search results. So if your keyword is a stop word this isnt good

    #1 Stop words in URLs
It is best to remove stop words from your URLs.
Benefit: shorter URLs
For example: Wordpress SEO plugin by Yoast is removing them automatically.

#2 Stop words in content and titles
Yes. It look natural when you are using stop words.
Remember that all keywords from Google Keyword Planner do not have stop words because Google is removing them since they are irrelevant. Bu you should use it in natural way in your content.

#3 Stop words in anchor text in backlinks
Also very good to mix them into anchor texts to make it more natural and not so optimized.
Also study by SearchMetrics:
SEO Ranking Factors - Rank Correlation 2013 for Google USA 2013
shown that websites that are using stop words in their backlinks are ranking higher (of course this is only statistica data, but still interesting)
    """

    """
    #Read and creating a_full_stopwords_en.txt that combines from 4 files such as "bnc_stopwords_en.txt", "english_stop_words.txt", "stopwords_en.txt", "stopwords_online_en.txt" in directory "/lib/stopwords"

    #y tuong: dua tat ca cac file vao 4 list
    list1 = get_list_from_file("../lib/stopwords/bnc_stopwords_en.txt")
    #print(list1)
    list2 = get_list_from_file("../lib/stopwords/english_stop_words.txt")
    list3 = get_list_from_file("../lib/stopwords/stopwords_en.txt")
    list4 = get_list_from_file("../lib/stopwords/stopwords_online_en.txt")

    list_result = [] # empty list
    #kiem tra da co trong list chua. Neu chua co thi them vao

    print("0 So luong phan tu trong list hien tai: %s " % str(len(list_result)) )

    #list 1
    for item in list1:
        if not is_in_list(item, list_result):
            list_result.append(item)
        else:
            print(item)

    print("1 So luong phan tu trong list hien tai: %s " % str(len(list_result)) )

    #list 2
    for item in list2:
        if not is_in_list(item, list_result):
            list_result.append(item)

    print("2 So luong phan tu trong list hien tai: %s " % str(len(list_result)) )

    #list 3
    for item in list3:
        if not is_in_list(item, list_result):
            list_result.append(item)

    print("3 So luong phan tu trong list hien tai: %s " % str(len(list_result)) )

    #list 4
    for item in list4:
        if not is_in_list(item, list_result):
            list_result.append(item)

    print("4 So luong phan tu trong list hien tai: %s " % str(len(list_result)) )

    #ghi list vao file khac
    file_writer = open("../lib/stopwords/a_full_stopwords_en.txt", 'w')

    #read data in openned file
    for line in list_result:
        file_writer.write(line)
        file_writer.write('\n')


    #close files
    file_writer.close()

    print ('OK')
    """
    #END - Added Codes - 2014/12/03