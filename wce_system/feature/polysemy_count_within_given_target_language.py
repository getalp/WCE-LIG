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

from common_module.cm_config import load_configuration, load_config_end_user
from feature.polysemy_count_common import convert_format_treetagger_to_format_babelnet, feature_polysemy_count_language, filter_number_of_polysemy
from common_module.cm_config import load_configuration
from common_module.cm_file import delete_file_within_given_path_and_message_error
from feature.polysemy_count_spanish import dict_tagset_spanish
from feature.polysemy_count_english import dict_tagset_english
from feature.polysemy_count_french import dict_tagset_french
#**************************************************************************#
#LIST_OF_SERVER_NAME
#Split input with the number of LIST_OF_SERVER_NAME
#TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_PATTERN
#def split_input_within_given_list_of_servers(file_input_path, list_of_server_name, file_output_path_pattern)
#**************************************************************************#
#Thuc thi cac lenh danh cho polysemy voi ten trung gian cung thay doi theo Server_Name
#**************************************************************************#
#Tong hop ket qua lai
def get_polysemy_count_within_given_target_language(target_language, file_input_path, file_output_path, extension = ""):
    #spanish_language = current_config.LANGUAGE_SPANISH # Spanish, es
    #english_language = current_config.LANGUAGE_ENGLISH # English, en
    #french_language = current_config.LANGUAGE_FRENCH # French, fr
    current_config = load_configuration()

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

    #convert_format_treetagger_to_format_babelnet( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, dict_tagset_spanish, current_config.BABEL_NET_CORPUS_ES + "_" + server_name)
    file_babel_net_corpus_temp_path = current_config.BABEL_NET_CORPUS + extension
    convert_format_treetagger_to_format_babelnet( file_output_path_pattern_include_server_name, dict_tagset, file_babel_net_corpus_temp_path)

    file_output_from_babel_net_temp_path = current_config.BABEL_NET_OUTPUT_CORPUS + extension
    str_message_error = "Verifying input corpus ... OK"
    delete_file_within_given_path_and_message_error( file_output_from_babel_net_temp_path, str_message_error)

    feature_polysemy_count_language(file_babel_net_corpus_temp_path, target_language, file_output_from_babel_net_temp_path)

    filter_number_of_polysemy(file_output_from_babel_net_temp_path, file_output_path)
#**************************************************************************#
if __name__ == "__main__":
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    target_language = config_end_user.TARGET_LANGUAGE
    file_input_path = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL
    file_output_path = current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST
    extension = ""

    get_polysemy_count_within_given_target_language(target_language, file_input_path, file_output_path)

    print ('OK')

