# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 14:36:31 2014
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

import sys
import os

#from common_functions import *
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from feature.polysemy_count_common import convert_format_treetagger_to_format_babelnet, feature_polysemy_count_language, filter_number_of_polysemy
from common_module.cm_config import load_configuration
#**************************************************************************#
#tagset for english
dict_tagset_english = {"NOUN":["NC","NNS","NN","PP","PP$","NPS","NP","WP","WDT","WP$"], \
"ADJECTIVE":["JJ","JJR","JJS","POS","ADJC"], \
"ADVERB":["RB","RBR","RBS","WRB","ADVC","UH"], \
"VERB":['VBG', 'MD', 'VBN', 'VBD', 'VBP', 'VBZ', 'VB', 'PRT', 'VC', 'VVD', 'VVN', 'VHD', 'VVG', 'VV', 'VHP', 'VVP', 'VVZ', 'VHN', 'VHZ', 'VHG', 'VH']} # "OTHER":["OTHER"]

#**************************************************************************#
if __name__ == "__main__":

    current_config = load_configuration()

    #convert_format_treetagger_to_format_babelnet(current_config.BABEL_NET_INPUT_CORPUS_EN,dict_tagset_english,current_config.BABEL_NET_CORPUS_EN)
    convert_format_treetagger_to_format_babelnet( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, dict_tagset_english, current_config.BABEL_NET_CORPUS_EN)


    #feature_polysemy_count_language(file_input_path, target_language, file_output_path)
    feature_polysemy_count_language( current_config.BABEL_NET_CORPUS_EN, current_config.LANGUAGE_ENGLISH, current_config.BABEL_NET_OUTPUT_CORPUS_EN)

    #Buoc 3: Loc du lieu phu hop
    #filter_number_of_polysemy(file_input_path, file_output_path):
    #filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_EN, current_config.BABEL_NET_OUTPUT_CORPUS_EN_LAST)
    filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_EN, current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    print ('OK')
