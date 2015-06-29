# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 15:16:14 2014
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
#tagset for french
dict_tagset_french = {"NOUN":["DET:POS","NAM","NOM","PRO","PRO:DEM","PRO:IND","PRO:PER","PRO:POS","PRO:REL"], \
"ADJECTIVE":["ADJ"], \
"ADVERB":["ADV"], \
"VERB":["VER:cond","VER:futu","VER:impe","VER:impf","VER:infi", \
"VER:pper","VER:ppre","VER:pres","VER:simp","VER:subi","VER:subp","VER"]} # "OTHER":["OTHER"]

#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    #print (dict_tagset_french)
    #print (dict_tagset_french["NOUN"]) #keyword = NOUN

    #Test case:
    #get_pos_in_format_babelnet(pos_treetager, dict_tagset_language)

    #-> NOUN
    #result = get_pos_in_format_babelnet("PPC", dict_tagset_french)
    #print(result)

    #VHger -> VERB
    #result = get_pos_in_format_babelnet("VHger", dict_tagset_french)
    #print(result)

    #VHger_new -> OTHER
    #result = get_pos_in_format_babelnet("VHger_new", dict_tagset_french)
    #print(result)

    #Test case: checking the function
    #convert_format_treetagger_to_format_babelnet(file_input_path, dict_tagset_language, file_output_path)
    #convert_format_treetagger_to_format_babelnet('../corpus/target.test.POS.txt',dict_tagset_french,'../corpus/target.test.POS.babelnet.txt')

    current_config = load_configuration()

    #Buoc 1 : Tao file phu hop voi BabelNet *** Chu y: Thay doi dict_tagset cho phu hop
    convert_format_treetagger_to_format_babelnet(current_config.BABEL_NET_INPUT_CORPUS_FR_IT_DU_LIEU,dict_tagset_french,current_config.BABEL_NET_CORPUS_FR)

    #Buoc nay chay rat lau, phu thuoc vao Target-Language
    #100 tu khong phai OTHER thi chay khoang 2 phut
    #Can chu y buoc nay

    #Test case: Buoc 2 *** Chu y: Thay doi Target-Language cho phu hop
    #feature_polysemy_count_language(file_input_path, target_language, file_output_path)
    feature_polysemy_count_language(current_config.BABEL_NET_CORPUS_FR,current_config.LANGUAGE_FRENCH, current_config.BABEL_NET_OUTPUT_CORPUS_FR)

    #Buoc 3: Loc du lieu phu hop
    #filter_number_of_polysemy(file_input_path, file_output_path):
    #filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_FR, current_config.BABEL_NET_OUTPUT_CORPUS_FR_LAST)
    filter_number_of_polysemy(current_config.BABEL_NET_OUTPUT_CORPUS_FR, current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST)

    print ('OK')