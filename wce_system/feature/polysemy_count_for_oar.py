# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 15:40:11 2014
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

#from common_functions import *
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from feature.polysemy_count_common import convert_format_treetagger_to_format_babelnet, feature_polysemy_count_language, filter_number_of_polysemy
from common_module.cm_config import load_configuration
from feature.polysemy_count_spanish import dict_tagset_spanish
from feature.polysemy_count_english import dict_tagset_english
from feature.polysemy_count_french import dict_tagset_french
#**************************************************************************#
#**************************************************************************#
#LIST_OF_SERVER_NAME
#Split input with the number of LIST_OF_SERVER_NAME
#TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_PATTERN
#def split_input_within_given_list_of_servers(file_input_path, list_of_server_name, file_output_path_pattern)
#**************************************************************************#
#Thuc thi cac lenh danh cho polysemy voi ten trung gian cung thay doi theo Server_Name
#**************************************************************************#
#Tong hop ket qua lai
def get_polysemy_count_within_given_target_language(target_language, file_input_path, extension = ".ape"):
    #spanish_language = current_config.LANGUAGE_SPANISH # Spanish, es
    #english_language = current_config.LANGUAGE_ENGLISH # English, en
    #french_language = current_config.LANGUAGE_FRENCH # French, fr

    dict_tagset = {}

    if target_language == current_config.LANGUAGE_ENGLISH:
        dict_tagset = dict_tagset_english
    elif target_language == current_config.LANGUAGE_FRENCH:
        dict_tagset = dict_tagset_french
    elif target_language == current_config.LANGUAGE_SPANISH:
        dict_tagset = dict_tagset_spanish
    #end if

    #file_output_path_pattern_include_server_name = file_output_path_pattern + "_" + server_name
    file_output_path_pattern_include_server_name = file_input_path

    file_babel_net_corpus_temp_path = current_config.BABEL_NET_CORPUS + extension
    convert_format_treetagger_to_format_babelnet( file_output_path_pattern_include_server_name, dict_tagset, file_babel_net_corpus_temp_path)

    file_output_from_babel_net_temp_path = current_config.BABEL_NET_OUTPUT_CORPUS + extension
    feature_polysemy_count_language(file_babel_net_corpus_temp_path, target_language, file_output_from_babel_net_temp_path)

    file_result_path = current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST + extension
    filter_number_of_polysemy(file_output_from_babel_net_temp_path, file_result_path)
#**************************************************************************#
if __name__ == "__main__":
    current_config = load_configuration()
    file_output_path_pattern = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_PATTERN
    server_name = sys.argv[1]
    target_language = sys.argv[2]

    #spanish_language = current_config.LANGUAGE_SPANISH # Spanish, es
    #english_language = current_config.LANGUAGE_ENGLISH # English, en
    #french_language = current_config.LANGUAGE_FRENCH # French, fr

    dict_tagset = {}

    if target_language == current_config.LANGUAGE_ENGLISH:
        dict_tagset = dict_tagset_english
    elif target_language == current_config.LANGUAGE_FRENCH:
        dict_tagset = dict_tagset_french
    elif target_language == current_config.LANGUAGE_SPANISH:
        dict_tagset = dict_tagset_spanish
    #end if

    file_output_path_pattern_include_server_name = file_output_path_pattern + "_" + server_name

    convert_format_treetagger_to_format_babelnet( file_output_path_pattern_include_server_name, dict_tagset, current_config.BABEL_NET_CORPUS_OAR + "_" + server_name)

    feature_polysemy_count_language(current_config.BABEL_NET_CORPUS_OAR + "_" + server_name, target_language, current_config.BABEL_NET_OUTPUT_CORPUS_OAR + "_" + server_name)

    filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_OAR + "_" + server_name, current_config.BABEL_NET_OUTPUT_CORPUS_TGT_OAR_LAST + "_" + server_name)

    print ('OK')

