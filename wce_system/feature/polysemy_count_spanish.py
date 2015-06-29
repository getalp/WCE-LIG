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

"""
Buoc 1:
    input: file output cua TreeTagger doi voi tung ngon ngu (EN, FR, ES, VI ...)
    output: file voi moi dong co dang
        stemmed_word NOUN/VERB/ADJECTIVE/ADVERB/OTHER

Buoc 2: Tinh so luong nghia cua tu (goi ham dem so luong nghia bang babelnet)

Buoc 3: Xoa cac dong khong can thiet; Thay the cac doan khong dung; Loc cac dong chua du lieu can thiet

********************************
--> Phan chung: da so cac ham
--> Phan rieng: khai bao dict tagset cho tung ngon ngu khac nhau (Doi voi TreeTagger). Dung dict & list de bieu dien mang 2 chieu doi voi yeu cau o buoc 1.
"""
import os
import sys

#from common_functions import *
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from feature.polysemy_count_common import convert_format_treetagger_to_format_babelnet, feature_polysemy_count_language, filter_number_of_polysemy
from common_module.cm_config import load_configuration
#**************************************************************************#
#tagset for spanish
dict_tagset_spanish = {"NOUN":["NC", "NMEA", "NP", "PPX", "PPC"], \
"ADJECTIVE":["ADJ"], \
"ADVERB":["ADV"], \
"VERB":["VCLIger","VCLIinf","VCLIfin","VEadj","VEfin","VEger","VEinf", \
"VHadj","VHfin","VHger","VHinf","VLadj","VLfin","VLger","VLinf","VMadj", \
"VMfin","VMger","VMinf","VSadj","VSfin","VSger","VSinf","VBfin","VBinf", \
"VBadj"]} # "OTHER":["OTHER"]

#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    #print (dict_tagset_spanish)
    #print (dict_tagset_spanish["NOUN"]) #keyword = NOUN

    #Test case:
    #get_pos_in_format_babelnet(pos_treetager, dict_tagset_language)

    #-> NOUN
    #result = get_pos_in_format_babelnet("PPC", dict_tagset_spanish)
    #print(result)

    #VHger -> VERB
    #result = get_pos_in_format_babelnet("VHger", dict_tagset_spanish)
    #print(result)

    #VHger_new -> OTHER
    #result = get_pos_in_format_babelnet("VHger_new", dict_tagset_spanish)
    #print(result)

    #Test case: checking the function
    #convert_format_treetagger_to_format_babelnet(file_input_path, dict_tagset_language, file_output_path)
    #convert_format_treetagger_to_format_babelnet('../corpus/target.test.POS.txt',dict_tagset_spanish,'../corpus/target.test.POS.babelnet.txt')

    current_config = load_configuration()

    """
    #Buoc 1 : Tao file phu hop voi BabelNet
    #convert_format_treetagger_to_format_babelnet(current_config.BABEL_NET_INPUT_CORPUS_ES,dict_tagset_spanish,current_config.BABEL_NET_CORPUS_ES)
    convert_format_treetagger_to_format_babelnet( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, dict_tagset_spanish, current_config.BABEL_NET_CORPUS_ES)

    #Buoc nay chay rat lau, phu thuoc vao Target-Language
    #100 tu khong phai OTHER thi chay khoang 2 phut
    #Can chu y buoc nay

    #Test case: Buoc 2 *** Chu y: Thay doi Target-Language cho phu hop
    #old version
    #feature_polysemy_count_spanish(current_config.BABEL_NET_CORPUS, current_config.BABEL_NET_OUTPUT_CORPUS)

    #feature_polysemy_count_language(file_input_path, target_language, file_output_path)
    #feature_polysemy_count_language(current_config.BABEL_NET_CORPUS_ES,current_config.LANGUAGE_SPANISH, current_config.BABEL_NET_OUTPUT_CORPUS_ES)
    feature_polysemy_count_language(current_config.BABEL_NET_CORPUS_ES, current_config.LANGUAGE_SPANISH, current_config.BABEL_NET_OUTPUT_CORPUS_ES)

    #Buoc 3: Loc du lieu phu hop
    #filter_number_of_polysemy(file_input_path, file_output_path):
    #filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_ES, current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    #filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_ES, current_config.BABEL_NET_OUTPUT_CORPUS_ES_LAST)
    filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_ES, current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    #neu lam voi OAR hay chay tren nhieu server thi phai co file trung gian co ten khac nhau va result la: BABEL_NET_OUTPUT_CORPUS_TGT_PATTERN
    """

    print ('OK')

