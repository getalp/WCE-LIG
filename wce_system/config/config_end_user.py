# -*- coding: utf-8 -*-

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
import yaml

#**************************************************************************#
"""
file: 'config_end_user.yml' trong thu muc 'eval_agent/input_data'
"""

class config_end_user(object):
    """
    Declare the Constants for the projects
    """

    def __init__(self, path_of_configuration_file, language_pair = "input_data"):
        """
        Get all of the path of outputs that are extracted

        :type path_of_configuration_file: string
        :param path_of_configuration_file: path to the file configuration with format YAML.

        :type language_pair: string
        :param language_pair: language pair, default = input_data

        :raise ValueError: if the path is not existed
        """
        #get path to current module
        #path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/"
        #path = os.path.dirname(os.path.abspath(path_of_configuration_file)) + "/"
        path = os.getenv("WCE_ROOT")+ "/"
        #print("Test of the environment variable WCE_ROOT: "+path+" "+path_of_configuration_file)


        #check existed paths
        if not os.path.exists(path_of_configuration_file):
            raise TypeError('Not Existed file configuration with format YAML')

        settings_stream = open(path_of_configuration_file, 'r')
        settingsMap = yaml.load(settings_stream)

        """
        treeroot:
             branch1: branch1 text
             branch2: branch2 text

        *** To access "branch1 text" you would use:
            txt = settingsMap["treeroot"]["branch1"]
            print (txt) --> "branch1 text"
        """

        #for treeroot in settingsMap:
            #print(treeroot)

        #print(settingsMap[language_pair]['number_of_occurrences'])

        #******************************************************#
        #language_pair
        self.LANGUAGE_PAIR = language_pair

        #******************************************************#
        #language
        self.SOURCE_LANGUAGE = settingsMap[language_pair]['source_language']
        self.TARGET_LANGUAGE = settingsMap[language_pair]['target_language']

        #******************************************************#
        ##for input corpus
        self.RAW_CORPUS_SOURCE_LANGUAGE = path + settingsMap[language_pair]['raw_corpus_source_language']
        self.RAW_CORPUS_TARGET_LANGUAGE = path + settingsMap[language_pair]['raw_corpus_target_language']
        self.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE = path + settingsMap[language_pair]['post_edition_of_machine_translation_sentences_target_language']
        self.RAW_CORPUS_TRAINING_SIZE = settingsMap[language_pair]['raw_corpus_training_size']
        self.RAW_CORPUS_TEST_SIZE = settingsMap[language_pair]['raw_corpus_test_size']
        #self.RAW_CORPUS_SOURCE_LANGUAGE = settingsMap[language_pair]['raw_corpus_source_language']
        #self.RAW_CORPUS_TARGET_LANGUAGE = settingsMap[language_pair]['raw_corpus_target_language']
        #self.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE = settingsMap[language_pair]['post_edition_of_machine_translation_sentences_target_language']
        #self.LIST_OF_ID_SENTENCES_ASR = path + settingsMap[language_pair]['list_of_id_sentences_asr']
        self.LOWERCASE = settingsMap[language_pair]['lowercase']
        self.TOKENIZER = settingsMap[language_pair]['tokenizer']

        self.LANGUAGE_MODEL_SOURCE_LANGUAGE = path + settingsMap[language_pair]['language_model_source_language']
        self.LANGUAGE_MODEL_TARGET_LANGUAGE = path + settingsMap[language_pair]['language_model_target_language']
        #self.LANGUAGE_MODEL_SOURCE_LANGUAGE = settingsMap[language_pair]['language_model_source_language']
        #self.LANGUAGE_MODEL_TARGET_LANGUAGE = settingsMap[language_pair]['language_model_target_language']

        self.GOOGLE_TRANSLATOR = path + settingsMap[language_pair]['google_translator']
        self.BING_TRANSLATOR = path + settingsMap[language_pair]['bing_translator']
        #self.GOOGLE_TRANSLATOR = settingsMap[language_pair]['google_translator']
        #self.BING_TRANSLATOR = settingsMap[language_pair]['bing_translator']

        ##version moses
        self.VERSION_MOSES = settingsMap[language_pair]['version_moses']

        ##Giza++
        self.PATH_TO_TOOL_GIZA = path + settingsMap[language_pair]['path_to_tool_giza']
        self.PATH_TO_TOOL_MKCLS = path + settingsMap[language_pair]['path_to_tool_mkcls']

        ## is_has_a file that included alignment. 1: True ~ Existed; 0: False ~ not existed
        ## if not existed, we would not have some features that uses alignment file such as: Longest Source gram length, 18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming); WPP any; Max; Min; Nodes; WPP Exact
        self.IS_HAS_A_FILE_INCLUDED_ALIGNMENT = settingsMap[language_pair]['is_has_a_file_included_alignment']
		#ce_agent
        self.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT = 1
        #self.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT = 2

        self.ONE_BEST_LIST_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['one_best_list_included_alignment']
        self.N_BEST_LIST_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['n_best_list_included_alignment']

        #berkeley_parser Tool
        self.TOOL_GET_CONSTITUENT_FR = path + settingsMap[language_pair]['tool_get_constituent_fr']
        #self.TOOL_GET_CONSTITUENT_FR = settingsMap[language_pair]['tool_get_constituent_fr']
        self.VISITE_PRECEDENT = ".."
        self.TOOL_BERKELEY_PARSER_PATH = path + settingsMap[language_pair]['tool_berkeley_parser_path']
        #self.TOOL_BERKELEY_PARSER_PATH = settingsMap[language_pair]['tool_berkeley_parser_path']
        self.GRAMMAR_FR_FOR_BERKELEY_PARSER_PATH = path + settingsMap[language_pair]['grammar_fr_for_berkeley_parser_path']
        #self.GRAMMAR_FR_FOR_BERKELEY_PARSER_PATH = settingsMap[language_pair]['grammar_fr_for_berkeley_parser_path']
        self.GRAMMAR_EN_FOR_BERKELEY_PARSER_PATH = path + settingsMap[language_pair]['grammar_en_for_berkeley_parser_path']
        #self.GRAMMAR_EN_FOR_BERKELEY_PARSER_PATH = settingsMap[language_pair]['grammar_en_for_berkeley_parser_path']
        self.GRAMMAR_AR_FOR_BERKELEY_PARSER_PATH = path + settingsMap[language_pair]['grammar_ar_for_berkeley_parser_path']
        #self.GRAMMAR_AR_FOR_BERKELEY_PARSER_PATH = settingsMap[language_pair]['grammar_ar_for_berkeley_parser_path']
        self.GRAMMAR_ES_FOR_BERKELEY_PARSER_PATH = path + settingsMap[language_pair]['grammar_es_for_berkeley_parser_path']
        #self.GRAMMAR_ES_FOR_BERKELEY_PARSER_PATH = settingsMap[language_pair]['grammar_es_for_berkeley_parser_path']

        ##SRILM tool
        self.TOOL_NGRAM = path + settingsMap[language_pair]["tool_ngram"]
        self.SRILM_BIN_DIRECTORY = path + settingsMap[language_pair]["srilm_bin_directory"]

        #shell script tools - BabelNet
        self.TOOL_BABEL_NET_EN = path + settingsMap[language_pair]["tool_babel_net_en"]
        self.TOOL_BABEL_NET_FR = path + settingsMap[language_pair]["tool_babel_net_fr"]
        self.TOOL_BABEL_NET_ES = path + settingsMap[language_pair]["tool_babel_net_es"]
        self.TOOL_BABEL_NET_DIR = path + settingsMap[language_pair]["tool_babel_net_dir"]

        ##tag-file-path
        self.TAGS_FILE_PATH = path + settingsMap[language_pair]["tags_file_path"]
        #self.TAGS_FILE_PATH = settingsMap[language_pair]["tags_file_path"]

        ## TreeTagger
        self.TREE_TAGGER_PATH = path + settingsMap[language_pair]['tree_tagger_path']

        ##Tool MOSES
        #self.TOOL_MOSES = path + settingsMap[language_pair]['tool_moses']
        #self.TOOL_MOSES = settingsMap[language_pair]['tool_moses']

        ##Tool fastnc
        self.TOOL_FASTNC = path + settingsMap[language_pair]['tool_fastnc']
        self.TOOL_REFTOCTM = path + settingsMap[language_pair]['tool_RefToCtm']

        ##Terpa
        self.TOOL_JAVA = settingsMap[language_pair]['tool_java']
        self.TOOL_JAVA_MEM_PARAM = settingsMap[language_pair]['tool_java_mem_param']
        self.TOOL_TERPA_DIR = path + settingsMap[language_pair]['tool_terpa_dir']
        self.TOOL_TERPA_JAR = path + settingsMap[language_pair]['tool_terpa_jar']
        self.TOOL_TERPA_PARAM = path + settingsMap[language_pair]['tool_terpa_param']
        self.TOOL_TERPA_PARAM_LOC = path + settingsMap[language_pair]['tool_terpa_param_loc']
        self.TOOL_TERPA = path + settingsMap[language_pair]['tool_terpa']
        self.TOOL_TERPA_NO_SHIFT_COST = path + settingsMap[language_pair]['tool_terpa_no_shift_cost']
        self.TOOL_TERPA_WITHIN_TOKENIZING = path + settingsMap[language_pair]['tool_terpa_within_tokenizing']
        self.TOOL_TERP = path + settingsMap[language_pair]['tool_terp']
        self.TOOL_TERCOM = path + settingsMap[language_pair]['tool_tercom']
        self.TERCOM_JAR = path + settingsMap[language_pair]['tercom_jar']
        self.TOOL_TERCPP = path + settingsMap[language_pair]['tool_tercpp']

        ## CRF model
        self.TOOL_WAPITI = path + settingsMap[language_pair]['tool_wapiti']

        self.TOOL_FAST_ALIGN = path + settingsMap[language_pair]['tool_fast_align']

        ##MOSES
        self.TOOL_TRAIN_MODEL = path + settingsMap[language_pair]['tool_train_model']
        
        terp_loc_file = open(self.TOOL_TERPA_PARAM_LOC,"w")
        terp_loc_file.write("WordNet Database Directory (filename)    : "+ path + settingsMap[language_pair]['tool_terpa_dir'] + "/../WordNet-3.0/dict/\n")
        terp_loc_file.write("Shift Stop Word List (string)            : "+ path + settingsMap[language_pair]['tool_terpa_dir'] + "/data/shift_word_stop_list.txt\n")
        terp_loc_file.write("Phrase Database (filename)               : "+ path + settingsMap[language_pair]['tool_terpa_dir'] + "/data/phrases.db\n")
        terp_loc_file.close()
        #/tmp/tmpservan/wce_system///tools/terplus/terp.v1/data/data_loc.param
        #WordNet Database Directory (filename)    : /home/lent/Develops/Solution/tool/terplus/WordNet-3.0/dict/
        #Shift Stop Word List (string)            : /home/lent/Develops/Solution/tool/terplus/terp.v1/data/shift_word_stop_list.txt
        #Phrase Database (filename)               : /home/lent/Develops/Solution/tool/terplus/terp.v1/data/phrases.db

#**************************************************************************#
if __name__ == "__main__":
    #Test case:

    #path_file_configuration = "../../config_end_user.yml"

    #obj = config_end_user(path_file_configuration)
    """
    #print (obj.NUMBER_OF_OCCURRENCES)

    #Get absolutely directory that contains file configuration
    #path = os.path.dirname(os.path.abspath(path_file_configuration))

    #get path to current module
    path = os.path.dirname(os.path.abspath(sys.argv[0]))

    print(path)

    path_current = os.getcwd()

    print(path_current)

    print(obj.CURRENT_SOURCE_LANGUAGE)
    print(obj.CURRENT_TARGET_LANGUAGE)
    """
    print ('OK')
#**************************************************************************#
