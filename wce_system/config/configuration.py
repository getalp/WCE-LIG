# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 15:40:15 2014
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
import yaml

#**************************************************************************#
class config(object):
    """
    Declare the Constants for the projects
    """

    def __init__(self, path_of_configuration_file, language_pair = "language_pair"):
        """
        Get all of the path of outputs that are extracted

        :type path_of_configuration_file: string
        :param path_of_configuration_file: path to the file configuration with format YAML.

        :type language_pair: string
        :param language_pair: language pair, default = fr_en

        :raise ValueError: if the path is not existed
        """
        #print('Path of file-config is: %s' %path_of_configuration_file)

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

        #get path to current module
        #path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/"
        #path = os.path.dirname(os.path.abspath(path_of_configuration_file)) + "/"
        path = os.getenv("WCE_ROOT")+ "/"
        #print("Test of the environment variable WCE_ROOT: "+path)
        #print(path)

        #******************************************************#
        #Path of the tools
        TOOL_ROOT = "tools"
        self.FEATURE_LIST={}

        #language_pair
        self.LANGUAGE_PAIR = language_pair
        self.THREADS=settingsMap['options']['threads']
        self.punctuation = settingsMap['options']["punctuation"]
        self.stop_words = settingsMap['options']["stop_words"]
        self.numeric = settingsMap['options']["numeric"]
        self.proper_name = settingsMap['options']["proper_name"]
        self.unknown_lemma = settingsMap['options']["unknown_lemma"]
        self.occurence_words = settingsMap['options']["occurence_words"]
        self.occurence_stems = settingsMap['options']["occurence_stems"]
        self.google_translator = settingsMap['options']["google_translator"]
        self.bing_translator = settingsMap['options']["bing_translator"]
        self.longest_ngram_length_tgt = settingsMap['options']["longest_ngram_length_tgt"]
        self.longest_ngram_length_src = settingsMap['options']["longest_ngram_length_src"]
        self.backoff = settingsMap['options']["backoff"]
        self.alignments = settingsMap['options']["alignments"]
        self.wpp = settingsMap['options']["wpp"]
        self.wpp_any = settingsMap['options']["wpp_any"]
        self.distance_to_root = settingsMap['options']["distance_to_root"]
        self.polysemy_count_target = settingsMap['options']["polysemy_count_target"]
        self.label = settingsMap['options']["label"]

        #******************************************************#
        #language
        #self.SOURCE_LANGUAGE = settingsMap[language_pair]['source_language']
        #self.TARGET_LANGUAGE = settingsMap[language_pair]['target_language']

        self.LANGUAGE_ENGLISH = "en"
        self.LANGUAGE_FRENCH = "fr"
        self.LANGUAGE_SPANISH = "es"

        self.CURRENT_SOURCE_LANGUAGE = language_pair[0:2]
        self.CURRENT_TARGET_LANGUAGE = language_pair[3:]

        #******************************************************#
        ##for input corpus
        self.INPUT_RAW_CORPUS_SOURCE_LANGUAGE = path + settingsMap[language_pair]['input_raw_corpus_source_language']
        self.INPUT_RAW_CORPUS_TARGET_LANGUAGE = path + settingsMap[language_pair]['input_raw_corpus_target_language']
        self.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE = path + settingsMap[language_pair]['post_edition_of_machine_translation_sentences_target_language']
        self.POST_EDITION_AFTER_TOKENIZING_LOWERCASING = path + settingsMap[language_pair]['post_edition_after_tokenizing_lowercasing']
        self.PREPROCESSING_MESSAGE_OUTPUT = path + settingsMap[language_pair]['preprocessing_message_output']
        self.SOLUTION_MESSAGE_OUTPUT = path + settingsMap[language_pair]['solution_message_output']

        self.TARGET_REF_TEST_FORMAT_ROW_AFTER_ADDING_SENTENCE_ID = path + settingsMap[language_pair]['target_ref_test_format_row_after_adding_sentence_id']
        self.POST_EDITION_AFTER_TOKENIZING_LOWERCASING_AFTER_ADDING_SENTENCE_ID = path + settingsMap[language_pair]['post_edition_after_tokenizing_lowercasing_after_adding_sentence_id']

        #language_model
        #now, absolutely path to language model
        #in the future, i must change :)
        self.LANGUAGE_MODEL_SRC = path + settingsMap[language_pair]['language_model_src']
        self.LANGUAGE_MODEL_TGT = path + settingsMap[language_pair]['language_model_tgt']
        self.N_GRAM = 5

        self.GOOGLE_TRANSLATE_CORPUS = path + settingsMap[language_pair]['google_translate_corpus']
        self.BING_TRANSLATE_CORPUS = path + settingsMap[language_pair]['bing_translate_corpus']
        #******************************************************#
        ##after preprocessing
        #corpus

        #self.SRC_REF_TEST = path + settingsMap[language_pair]['src_ref_test']
        #self.SRC_REF_TEST_NUMBER_OF_WORDS = path + settingsMap[language_pair]['src_ref_test_number_of_words']
        #self.SRC_REF_TRAIN = path + settingsMap[language_pair]['src_ref_train']

        #self.TARGET_REF_TEST = path + settingsMap[language_pair]['target_ref_test']
        #self.TARGET_REF_TEST_NUMBER_OF_WORDS = path + settingsMap[language_pair]['target_ref_test_number_of_words']
        #self.TARGET_REF_TRAIN = path + settingsMap[language_pair]['target_ref_train']
        self.PATTERN_REF_TEST_FORMAT_ROW = path + settingsMap[language_pair]['pattern_ref_test_format_row']
        self.PATTERN_REF_TEST_FORMAT_ROW_APE = path + settingsMap[language_pair]['pattern_ref_test_format_row_ape']
        self.SRC_REF_TEST_FORMAT_ROW = path + settingsMap[language_pair]['src_ref_test_format_row']
        self.TARGET_REF_TEST_FORMAT_ROW = path + settingsMap[language_pair]['target_ref_test_format_row']
        self.SRC_TARGET_REF_TEST_FORMAT_ROW = path + settingsMap[language_pair]['src_target_ref_test_format_row']
        self.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_FORMAT_ROW = path + settingsMap[language_pair]['post_edition_of_machine_translation_sentences_format_row']
        """
        self.LIST_OF_ID_SENTENCES_ASR = path + settingsMap[language_pair]['list_of_id_sentences_asr']
        self.HYPOTHESIS_ASR_PATH = path + settingsMap[language_pair]['hypothesis_asr_path']
        self.REFERENCE_ASR_PATH = path + settingsMap[language_pair]['reference_asr_path']
        """

        #for testing moses 2009
        self.INPUT_RAW_CORPUS_SOURCE_LANGUAGE_TESTING_MOSES2009 = path + settingsMap[language_pair]['input_raw_corpus_source_language_testing_moses2009']
        self.SRC_REF_TEST_FORMAT_ROW_TESTING_MOSES2009 = path + settingsMap[language_pair]['src_ref_test_format_row_testing_moses2009']
        self.TGT_MT_ALL_FORMAT_ROW_TESTING_MOSES2009 = path + settingsMap[language_pair]['tgt_mt_all_format_row_testing_moses2009']
        self.TGT_MT_ALL_AFTER_LC_TOK_FORMAT_ROW_TESTING_MOSES2009 = path + settingsMap[language_pair]['tgt_mt_all_after_lc_tok_format_row_testing_moses2009']
        self.TRANSLATED_MODEL_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['translated_model_included_alignment']
        self.TRANSLATED_OUTPUT10881_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['translated_output10881_included_alignment']
        self.TRANSLATED_MODEL_NO_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['translated_model_no_included_alignment']
        self.TRANSLATED_OUTPUT10881_NO_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['translated_output10881_no_included_alignment']
        self.LOG_COMPARING_MT_AND_TRANSLATED_MODEL = path + settingsMap[language_pair]['log_comparing_tgt_mt_all_after_lc_tok_and_translated_model_no_included_alignment']
        self.LOG_COMPARING_MT_AND_TRANSLATED_OUTPUT10881 = path + settingsMap[language_pair]['log_comparing_tgt_mt_all_after_lc_tok_and_translated_output10881_no_included_alignment']
        self.POST_EDITION_FOR_CHECKING_MOSES_2009 = path + settingsMap[language_pair]['post_edition_for_checking_moses_2009']
        self.POST_EDITION_AFTER_TOKENIZING_LOWERCASING_CHECKING_MOSES_2009 = path + settingsMap[language_pair]['post_edition_after_tokenizing_lowercasing_checking_moses_2009']


        #for verifying the result
        self.EXTENSION_SOURCE = "src"
        self.EXTENSION_TARGET = "tgt"
        self.TARGET_MT_ALL_FORMAT_ROW = path + settingsMap[language_pair]['target_mt_all_format_row']
        self.SRC_REF_TEST_FORMAT_COL = path + settingsMap[language_pair]['src_ref_test_format_col']
        self.TARGET_REF_TEST_FORMAT_COL = path + settingsMap[language_pair]['target_ref_test_format_col']
        #self.RAW_CORPUS = path + settingsMap[language_pair]['raw_corpus']

        #doi ten --> TARGET_REF_TEST
        #self.HYPOTHESIS_ROW_CORPUS = path + settingsMap[language_pair]['hypothesis_row_corpus']

        self.PROBABILITY_HYPOTHESIS_ROW_CORPUS = path + settingsMap[language_pair]['probability_hypothesis_row_corpus']

        #doi ten --> REF_TEST_OUTPUT_TREETAGGER_SOURCE_LANGUAGE_FORMAT_ROW
        #self.REF_TEST_OUTPUT_TREETAGGER_SOURCE_LANGUAGE = path + settingsMap[language_pair]['ref_test_output_treetagger_source_language']

        #doi ten --> REF_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE_FORMAT_ROW
        #self.REF_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE = path + settingsMap[language_pair]['ref_test_output_treetagger_target_language']

        #doi ten--> MT_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE_FORMAT_ROW
        #self.MT_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE = path + settingsMap[language_pair]['mt_test_output_treetagger_target_language']

        ##TreeTagger output with format ROW
        self.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW = path + settingsMap[language_pair]['src_ref_test_output_treetagger_format_row']
        self.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW = path + settingsMap[language_pair]['target_ref_test_output_treetagger_format_row']
        #doi ten --> TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW
        #self.MT_TEST_OUTPUT_TREETAGGER_TARGET_LANGUAGE_FORMAT_ROW = path + settingsMap[language_pair]['mt_test_output_treetagger_target_language_format_row']

        ##TreeTagger output with format COLUMN
        #doi ten
        #self.TARGET_REF_TEST_FORMAT_COL_POS_STEM = path + settingsMap[language_pair]['target_ref_test_format_col_pos_stem']
        self.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL = path + settingsMap[language_pair]['src_ref_test_output_treetagger_format_col']
        #self.POS_STEM_CORPUS = path + settingsMap[language_pair]['pos_stem_corpus']

        #self.SRC_REF_TEST_FORMAT_COL_POS_STEM = path + settingsMap[language_pair]['src_ref_test_format_col_pos_stem']
        self.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL = path + settingsMap[language_pair]['target_ref_test_output_treetagger_format_col']

        #for source language (fr)
        #--> SRC_REF_TEST
        ##self.ROW_CORPUS_SOURCE_LANGUAGE = path + settingsMap[language_pair]['row_corpus_source_language']

        self.PROBABILITY_ROW_CORPUS_SOURCE_LANGUAGE = path + settingsMap[language_pair]['probability_row_corpus_source_language']

        #for target language (en)
        #doi ten: TARGET_REF_TEST
        #self.ROW_CORPUS_TARGET_LANGUAGE = path + settingsMap[language_pair]['row_corpus_target_language']

        ##alignment files
        ##khong dung nua
        ##self.ALIGNED_1_BEST_FROM_MOSES = path + settingsMap[language_pair]['aligned_1_best_from_moses']
        #self.ALIGNMENT_TARGET_TO_SOURCE_FROM_MOSES = path + settingsMap[language_pair]['alignment_target_to_source_from_moses']

        self.WORD_ALIGNMENT_USING_GIZA = path + settingsMap[language_pair]['word_alignment_using_giza']
        self.WORD_ALIGNMENT_USING_GIZA_AFTER_OPTIMISING = path + settingsMap[language_pair]['word_alignment_using_giza_after_optimising']

        #tam thoi dung duong dan tuyet doi
        #self.LANGUAGE_MODEL_FR = path + settingsMap[language_pair]['moses_ini']
        #self.MOSES_INI = settingsMap[language_pair]['moses_ini']

        self.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['mt_hypothesis_output_1_bestlist_included_alignment']
        self.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT_APE = path + settingsMap[language_pair]['mt_hypothesis_output_1_bestlist_included_alignment_ape']
        self.MT_HYPOTHESIS_OUTPUT_1_BESTLIST = path + settingsMap[language_pair]['mt_hypothesis_output_1_bestlist']

        self.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT = path + settingsMap[language_pair]['mt_hypothesis_output_nbestlist_included_alignment']
        self.MT_HYPOTHESIS_OUTPUT_NBESTLIST = path + settingsMap[language_pair]['mt_hypothesis_output_nbestlist']

        #******************************************************#
        #lib
        self.LIST_PUNCTUATIONS = path + settingsMap[language_pair]['list_punctuations']
        self.LIST_STOP_WORDS_EN = path + settingsMap[language_pair]['list_stop_words_en']
        self.LIST_STOP_WORDS_FR = path + settingsMap[language_pair]['list_stop_words_fr']
        self.LIST_STOP_WORDS_ES = path + settingsMap[language_pair]['list_stop_words_es']

        #******************************************************#
        #extracted_features
        self.RESULT_MESSAGE_OUTPUT = path + settingsMap[language_pair]['result_message_output']
        self.RESULT_MESSAGE_OUTPUT_APE = path + settingsMap[language_pair]['result_message_output_ape']
        self.NUMBER_OF_OCCURRENCES_STEM = path + settingsMap[language_pair]['number_of_occurrences_stem']
        self.NUMBER_OF_OCCURRENCES_WORD = path + settingsMap[language_pair]['number_of_occurrences_word']
        self.NUMERIC = path + settingsMap[language_pair]["numeric"]
        self.OCCUR_IN_GOOGLE_TRANSLATE = path + settingsMap[language_pair]["occur_in_google_translate"]
        self.OCCUR_IN_BING_TRANSLATE = path + settingsMap[language_pair]["occur_in_bing_translate"]
        self.POLYSEMY_COUNT_TARGET = path + settingsMap[language_pair]["polysemy_count_target"]
        self.POLYSEMY_COUNT_SOURCE = path + settingsMap[language_pair]["polysemy_count_source"]
        self.PROPER_NAME = path + settingsMap[language_pair]["proper_name"]
        self.UNKNOWN_LEMMA = path + settingsMap[language_pair]["unknown_lemma"]
        self.PUNCTUATION = path + settingsMap[language_pair]["punctuation"]
        self.STOP_WORD = path + settingsMap[language_pair]["stop_word"]
        self.LONGEST_TARGET_GRAM_LENGTH = path + settingsMap[language_pair]["longest_target_gram_length"]
        self.BACKOFF_BEHAVIOUR = path + settingsMap[language_pair]["backoff_behaviour"]
        self.VERIFY_RESULT_OLD_AND_NEW = path + settingsMap[language_pair]["verify_result_old_and_new"]
        self.WPP_NODES_MIN_MAX_TEMP = path + settingsMap[language_pair]["wpp_nodes_min_max_temp"]
        self.WPP_NODES_MIN_MAX = path + settingsMap[language_pair]["wpp_nodes_min_max"]
        self.WPP_EXACT = path + settingsMap[language_pair]["wpp_exact"]
        self.BACKOFF_BEHAVIOUR_AFTER_CONVERTING_TO_INT = path + settingsMap[language_pair]["backoff_behaviour_after_converting_to_int"]

        self.DIRECTORY_WITH_EXTRACTED_FEATURES_PATH = path + settingsMap[language_pair]["directory_with_extracted_features_path"]

        self.FEATURES_ASR_NOT_ALIGNMENT = path + settingsMap[language_pair]["features_asr_not_alignment"]
        self.FEATURES_ASR_ALIGNED = path + settingsMap[language_pair]["features_asr_aligned"]
        self.FEATURES_ASR_ALIGNED_LAST = path + settingsMap[language_pair]["features_asr_aligned_last"]


        self.ALIGNMENT_SRC_TGT_FORMAT_ROW = path + settingsMap[language_pair]["alignment_src_tgt_format_row"]
        self.ALIGNMENT_TGT_SRC_FORMAT_ROW = path + settingsMap[language_pair]["alignment_tgt_src_format_row"]

        #for test corpus
        self.FEATURES_TEST_WMT14 = path + settingsMap[language_pair]["features_test_wmt14"]
        self.FEATURES_TEST_WMT13 = path + settingsMap[language_pair]["features_test_wmt13"]

        #for train corpus
        self.FEATURES_TRAIN_WMT14 = path + settingsMap[language_pair]["features_train_wmt14"]
        self.FEATURES_TRAIN_WMT13 = path + settingsMap[language_pair]["features_train_wmt13"]

        self.FEATURES_TRAIN_WMT14_WMT13 = path + settingsMap[language_pair]["features_train_wmt14_wmt13"]
        self.FEATURES_TEST_WMT14_WMT13 = path + settingsMap[language_pair]["features_test_wmt14_wmt13"]
        self.LABEL_OUTPUT_FROM_EXTRACTED_FEATURES = path + settingsMap[language_pair]["label_output_from_extracted_features"]
        self.FEATURES_TRAIN_WMT14_WMT13_TEST_WMT14 = path + settingsMap[language_pair]["features_train_wmt14_wmt13_test_wmt14"]
        self.FEATURES_TRAIN_WMT14_WMT13_TEST_WMT13 = path + settingsMap[language_pair]["features_train_wmt14_wmt13_test_wmt13"]
        self.FEATURES_TRAIN_WMT14_TEST_WMT14 = path + settingsMap[language_pair]["features_train_wmt14_test_wmt14"]
        self.FEATURES_TRAIN_WMT13_TEST_WMT13 = path + settingsMap[language_pair]["features_train_wmt13_test_wmt13"]
        self.FEATURES_TRAIN_WMT15_14_13_TEST_WMT = path + settingsMap[language_pair]["features_train_wmt15_14_13_test_wmt"]



        ## Lingua-LinkParser-1.17 + link-grammar-4.8.6 --> Constituent Label & Distance to Root, NULL link (EN)
        ## self.CONSTITUENT_FIRST_EN_TEMP = path + settingsMap[language_pair]["constituent_first_en_temp"]
        ## self.CONSTITUENT_LAST_EN_TEMP = path + settingsMap[language_pair]["constituent_last_en_temp"]
        ## self.CONSTITUENT_FIRST_EN = path + settingsMap[language_pair]["constituent_first_en"]
        ## self.CONSTITUENT_LAST_EN = path + settingsMap[language_pair]["constituent_last_en"]
        self.CONSTITUENT_TREE_TEMP = path + settingsMap[language_pair]["constituent_tree_temp"]
        #self.CONSTITUENT_TREE = path + settingsMap[language_pair]["constituent_tree"]
        self.DISTANCE_TO_ROOT = path + settingsMap[language_pair]["distance_to_root"]
        self.CONSTITUENT_LABEL = path + settingsMap[language_pair]["constituent_label"]
        self.CONSTITUENT_LABEL_AFTER_CONVERTING_TO_INT = path + settingsMap[language_pair]["constituent_label_after_converting_to_int"]

        #for source language (fr)
        self.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET = path + settingsMap[language_pair]["temp_longest_source_gram_length_not_aligned_target"]
        self.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW = path + settingsMap[language_pair]["temp_longest_source_gram_length_not_aligned_target_row"]
        self.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET = path + settingsMap[language_pair]["longest_source_gram_length_aligned_target"]
        self.ALIGNMENT_FEATURES = path + settingsMap[language_pair]["alignment_features"]
        self.ALIGNMENT_FEATURES_AFTER_CONVERTING_TO_INT = path + settingsMap[language_pair]["alignment_features_after_converting_to_int"]

        #type_longest_gram_source_length = MIN, MAX, AVG, FIRST
        self.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL = 0
        self.TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX = 1
        self.TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN = 2
        self.TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG = 3
        self.TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST = 4

        #Path of the tools
        ##for pre_processing
        self.TOOL_PRE_PROCESSING = path + settingsMap[TOOL_ROOT]['tool_pre_processing']
        self.TOOL_PRE_PROCESSING_LOWERCASING = path + settingsMap[TOOL_ROOT]['tool_pre_processing_lowercasing']

        ##TreeTagger
        self.TOOL_TREE_TAGGER = path + settingsMap[TOOL_ROOT]['tool_tree_tagger']
        ###self.TREE_TAGGER_PATH = path + settingsMap[TOOL_ROOT]['tree_tagger_path']
        self.CUSTOMIZE_OUTPUT_TREETAGGER = path + settingsMap[TOOL_ROOT]['customize_output_treetagger']

        #For common name
        #self.BABEL_NET_OUTPUT_CORPUS_TGT_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_tgt_last']
        self.BABEL_NET_OUTPUT_CORPUS_TGT_PATTERN = path + settingsMap[language_pair]['babel_net_output_corpus_tgt_last_pattern']

        #For common name DBnary
        #self.DBNARY_OUTPUT_CORPUS_TGT_LAST = path + settingsMap[language_pair]['dbnary_output_corpus_tgt_last']
        self.DBNARY_OUTPUT_CORPUS_TGT_PATTERN = path + settingsMap[language_pair]['dbnary_output_corpus_tgt_last_pattern']

        ##for independent target language
        ##babel_net_corpus is the temp-file that uses for shell script - BalbelNet
        self.BABEL_NET_CORPUS = path + settingsMap[language_pair]['babel_net_corpus']
        self.BABEL_NET_OUTPUT_CORPUS = path + settingsMap[language_pair]['babel_net_output_corpus']
        self.BABEL_NET_OUTPUT_CORPUS_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_last']
        self.BABEL_NET_OUTPUT_CORPUS_TGT_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_target_last']

        ##babel_net_corpus is the temp-file that uses for shell script - DBnary
        self.DBNARY_CORPUS = path + settingsMap[language_pair]['dbnary_corpus']
        self.DBNARY_OUTPUT_CORPUS = path + settingsMap[language_pair]['dbnary_output_corpus']
        self.DBNARY_OUTPUT_CORPUS_LAST = path + settingsMap[language_pair]['dbnary_output_corpus_last']
        self.DBNARY_OUTPUT_CORPUS_TGT_LAST = path + settingsMap[language_pair]['dbnary_output_corpus_target_last']

        #For OAR
        ##babel_net_corpus is the temp-file that uses for shell script - BalbelNet
        self.BABEL_NET_CORPUS_OAR = path + settingsMap[language_pair]['babel_net_corpus_oar']
        self.BABEL_NET_OUTPUT_CORPUS_OAR = path + settingsMap[language_pair]['babel_net_output_corpus_oar']
        self.BABEL_NET_OUTPUT_CORPUS_OAR_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_oar_last']
        self.BABEL_NET_OUTPUT_CORPUS_TGT_OAR_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_tgt_oar_last']

        #For spanish
        ##babel_net_corpus is the temp-file that uses for shell script - BalbelNet
        self.BABEL_NET_CORPUS_ES = path + settingsMap[language_pair]['babel_net_corpus_es']
        self.BABEL_NET_OUTPUT_CORPUS_ES = path + settingsMap[language_pair]['babel_net_output_corpus_es']
        self.BABEL_NET_OUTPUT_CORPUS_ES_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_es_last']

        #For english
        #doi ten
        #self.BABEL_NET_INPUT_CORPUS_EN = path + settingsMap[TOOL_ROOT]['babel_net_input_corpus_en']

        #self.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_IT_DU_LIEU = path + settingsMap[language_pair]['target_ref_test_output_treetagger_format_col_it_du_lieu']
        ##babel_net_corpus is the temp-file that uses for shell script - BalbelNet
        self.BABEL_NET_CORPUS_EN = path + settingsMap[language_pair]['babel_net_corpus_en']
        self.BABEL_NET_OUTPUT_CORPUS_EN = path + settingsMap[language_pair]['babel_net_output_corpus_en']
        self.BABEL_NET_OUTPUT_CORPUS_EN_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_en_last']

        #For french
        #doi ten
        #self.BABEL_NET_INPUT_CORPUS_FR = path + settingsMap[TOOL_ROOT]['babel_net_input_corpus_fr']
        #self.BABEL_NET_INPUT_CORPUS_FR_IT_DU_LIEU = path + settingsMap[TOOL_ROOT]['babel_net_input_corpus_fr_it_du_lieu']
        #self.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_IT_DU_LIEU = path + settingsMap[TOOL_ROOT]['src_ref_test_output_treetagger_format_col_it_du_lieu']

        ##babel_net_corpus is the temp-file that uses for shell script - BalbelNet
        self.BABEL_NET_CORPUS_FR = path + settingsMap[language_pair]['babel_net_corpus_fr']
        self.BABEL_NET_OUTPUT_CORPUS_FR = path + settingsMap[language_pair]['babel_net_output_corpus_fr']
        self.BABEL_NET_OUTPUT_CORPUS_FR_LAST = path + settingsMap[language_pair]['babel_net_output_corpus_fr_last']

        #shell script tools - BabelNet
        ###self.TOOL_BABEL_NET_EN = path + settingsMap[TOOL_ROOT]["tool_babel_net_en"]
        ###self.TOOL_BABEL_NET_FR = path + settingsMap[TOOL_ROOT]["tool_babel_net_fr"]
        ###self.TOOL_BABEL_NET_ES = path + settingsMap[TOOL_ROOT]["tool_babel_net_es"]
        ###self.TOOL_BABEL_NET_DIR = path + settingsMap[TOOL_ROOT]["tool_babel_net_dir"]

        #Tool ngram in SRILM
        #Phai dung duong dan tuyet doi den thu muc cai dat SRILM
        #KHONG NEN COPY
        #self.TOOL_NGRAM = path + settingsMap[TOOL_ROOT]["tool_ngram"]
        ###self.TOOL_NGRAM = settingsMap[TOOL_ROOT]["tool_ngram"]

        #Shell script in directory "lib"
        self.TOOL_CREATE_PROBABILITY_EACH_WORD_FROM_LANGUAGE_MODEL = path + settingsMap[TOOL_ROOT]['tool_create_probability_each_word_from_language_model']
        self.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH = path + settingsMap[TOOL_ROOT]['tool_create_longest_target_gram_length']
        self.TOOL_N_BEST_TO_LATTICE = path + settingsMap[TOOL_ROOT]['tool_n_best_to_lattice']
        self.TOOL_N_BEST_TO_LATTICE_THREADS = path + settingsMap[TOOL_ROOT]['tool_n_best_to_lattice_threads']

        ##Tool MOSES
        ###self.TOOL_MOSES = path + settingsMap[TOOL_ROOT]['tool_moses']
        self.SCRIPT_TEMP = path + settingsMap[TOOL_ROOT]['script_temp']

        ##Tool fastnc
        ###self.TOOL_FASTNC = path + settingsMap[TOOL_ROOT]['tool_fastnc']
        ###self.TOOL_REFTOCTM = path + settingsMap[TOOL_ROOT]['tool_RefToCtm']

        ##tool lingua nay khong huu dung
        ##tool Lingua-LinkParser-1.17 + link-grammar-4.8.6 --> Constituent Label & Distance to Root, NULL link (EN)
        #self.TOOL_GET_CONSTITUENT_FIRST = path + settingsMap[TOOL_ROOT]['tool_get_constituent_first']
        #self.TOOL_GET_CONSTITUENT_LAST = path + settingsMap[TOOL_ROOT]['tool_get_constituent_last']

        ## Berkeley Parser
        self.REPLACE_PARENTHESIS = path + settingsMap[TOOL_ROOT]['replace_parenthesis']
        self.BERKELEY_PARSER_INPUT = path + settingsMap[language_pair]['berkeley_parser_input']

        #result_berkeley_parser_unknown: (())
        #out_of_knowdlege_string: OOK
        #out_of_knowdlege_int: -1

        self.RESULT_BERKELEY_PARSER_UNKNOWN = "(())"
        self.OUT_OF_KNOWDLEGE_STRING = "OOK"
        self.OUT_OF_KNOWDLEGE_INT = -1

        """
        self.TOOL_GET_CONSTITUENT_FR = path + settingsMap[TOOL_ROOT]['tool_get_constituent_fr']
        self.VISITE_PRECEDENT = ".."
        self.TOOL_BERKELEY_PARSER_PATH = path + settingsMap[TOOL_ROOT]['tool_berkeley_parser_path']
        self.GRAMMAR_FR_FOR_BERKELEY_PARSER_PATH = path + settingsMap[TOOL_ROOT]['grammar_fr_for_berkeley_parser_path']
        self.GRAMMAR_EN_FOR_BERKELEY_PARSER_PATH = path + settingsMap[TOOL_ROOT]['grammar_en_for_berkeley_parser_path']
        self.GRAMMAR_AR_FOR_BERKELEY_PARSER_PATH = path + settingsMap[TOOL_ROOT]['grammar_ar_for_berkeley_parser_path']
        self.GRAMMAR_ES_FOR_BERKELEY_PARSER_PATH = path + settingsMap[TOOL_ROOT]['grammar_es_for_berkeley_parser_path']
        """

        ## Terp_a
        self.CUSTOMIZE_INPUT_BEFORE_USING_TERPA = path + settingsMap[TOOL_ROOT]['customize_input_before_using_terpa']
        ###self.TOOL_TERPA = path + settingsMap[TOOL_ROOT]['tool_terpa']
        ###self.TOOL_TERPA_NO_SHIFT_COST = path + settingsMap[TOOL_ROOT]['tool_terpa_no_shift_cost']
        ###self.TOOL_TERPA_WITHIN_TOKENIZING = path + settingsMap[TOOL_ROOT]['tool_terpa_within_tokenizing']
        ###self.TOOL_TERP = path + settingsMap[TOOL_ROOT]['tool_terp']
        ###self.TOOL_TERCOM = path + settingsMap[TOOL_ROOT]['tool_tercom']
        self.HYPOTHESIS_SET = "tstset"
        self.POST_EDITION_SET = "refset"
        self.TOOL_WRAP_TEXT_TO_SGM = path + settingsMap[TOOL_ROOT]['wrap_text_to_sgm']
        self.HYPOTHESIS_SET_SGM = path + settingsMap[language_pair]['hypothesis_set_sgm']
        self.POST_EDITION_SGM = path + settingsMap[language_pair]['post_edition_sgm']
        self.TERP_PRA = path + settingsMap[TOOL_ROOT]['terp_pra']
        self.LABEL_OUTPUT = path + settingsMap[language_pair]['label_output']
        self.TERP_PRA_FROM_WCE_SLT_LIG = path + settingsMap[language_pair]['terp_pra_from_wce_slt_lig']

        #for Tercom - wmt
        self.TOOL_TERCOM = path + settingsMap[TOOL_ROOT]['tool_tercom']
        self.TERCOM_RESULT = path + settingsMap[language_pair]['tercom_result']
        self.TERCOM_SHIFTED_SENTENCES = path + settingsMap[language_pair]['tercom_shifted_sentences']
        self.LABEL_OUTPUT_TERCOM_ORIGINAL = path + settingsMap[language_pair]['label_output_tercom_original']
        self.LABEL_OUTPUT_TERCOM_WCE = path + settingsMap[language_pair]['label_output_tercom_wce']
        self.LABEL_OUTPUT_TERCOM_APE = path + settingsMap[language_pair]['label_output_tercom_ape']
        self.LABEL_OUTPUT_TERCOM_WCE_VERIFY = path + settingsMap[language_pair]['label_output_tercom_wce_verify']
        self.TERCPP_RESULT = path + settingsMap[language_pair]['tercpp_result']
        self.LABEL_OUTPUT_TERCPP_ORIGINAL = path + settingsMap[language_pair]['label_output_tercpp_original']

        ## CRF model
        ###self.TOOL_WAPITI = path + settingsMap[TOOL_ROOT]['tool_wapiti']
        self.OUTPUT_MERGED_FEATURES = path + settingsMap[language_pair]['output_merged_features']
        self.OUTPUT_MERGED_FEATURES_WMT15 = path + settingsMap[language_pair]['output_merged_features_wmt15']
        self.OUTPUT_MERGED_FEATURES_FOR_TESTING_MODEL = path + settingsMap[language_pair]['output_merged_features_for_testing_model']
        self.OUTPUT_MERGED_FEATURES_WMT15_AFTER_CONVERTING_TO_INT = path + settingsMap[language_pair]['output_merged_features_wmt15_after_converting_to_int']
        self.OUTPUT_MERGED_FEATURES_WMT15_AFTER_CONVERTING_TO_INT_WITHIN_LABEL = path + settingsMap[language_pair]['output_merged_features_wmt15_after_converting_to_int_within_label']
        self.OUTPUT_MERGED_FEATURES_WMT15_AFTER_CONVERTING_TO_INT_AND_REMOVE_EMPTY_LINE = path + settingsMap[language_pair]['output_merged_features_wmt15_after_converting_to_int_and_remove_empty_line']
        self.OUTPUT_MERGED_FEATURES_WMT15_FOR_PCA = path + settingsMap[language_pair]['output_merged_features_wmt15_for_pca']
        self.OUTPUT_MERGED_FEATURES_WMT15_FOR_PCA_AFTER_PCA = path + settingsMap[language_pair]['output_merged_features_wmt15_for_pca_after_pca']
        self.OUTPUT_MERGED_FEATURES_WMT15_AFTER_PCA_LAST = path + settingsMap[language_pair]['output_merged_features_wmt15_after_pca_last']
        self.OUTPUT_MERGED_FEATURES_WMT15_AFTER_PCA_LAST_AND_LABEL = path + settingsMap[language_pair]['output_merged_features_wmt15_after_pca_last_and_label']
        self.OUTPUT_MERGED_FEATURES_WMT15_AFTER_PCA_LAST_AND_LABEL_AND_REMOVE_EMPTY_LINE = path + settingsMap[language_pair]['output_merged_features_wmt15_after_pca_last_and_label_and_remove_empty_line']

        self.OUTPUT_MERGED_FEATURES_WMT14_WMT13 = path + settingsMap[language_pair]['output_merged_features_wmt14_wmt13']
        self.OUTPUT_MERGED_FEATURES_WMT14_WMT13_AFTER_CONVERTING_TO_INT = path + settingsMap[language_pair]['output_merged_features_wmt14_wmt13_after_converting_to_int']

        self.TEMPLATE_PATH = path + settingsMap[language_pair]['template_path']
        self.MODEL_PATH = path + settingsMap[language_pair]['model_path']
        self.TRAIN_FILE_PATH = path + settingsMap[language_pair]['train_file_path']
        self.DEV_FILE_PATH = path + settingsMap[language_pair]['dev_file_path']
        self.TEST_FILE_PATH = path + settingsMap[language_pair]['test_file_path']
        self.RESULT_TESTING_WAPITI = path + settingsMap[language_pair]['result_testing_wapiti']
        self.LOG_FILE_TRAINING_WAPITI = path + settingsMap[language_pair]['log_file_training_wapiti']
        self.LOG_FILE_TESTING_WAPITI = path + settingsMap[language_pair]['log_file_testing_wapiti']
        self.SEQUENTIAL_CORPUS = 1 #for Sequential Corpus in order to generate
        self.RANDOM_CORPUS = 2 #for Random corpus in order to generate
        self.RESULT_LABELING_WAPITI = path + settingsMap[language_pair]['result_labeling_wapiti']
        self.RESULT_LABELING_THRESHOLD = path + settingsMap[language_pair]['result_labeling_threshold']
        self.RESULT_THRESHOLD_BEST = path + settingsMap[language_pair]['result_threshold_best']

        ## For module "metrics"
        self.F_MEASURE_RESULT_BASELINE = path + settingsMap[language_pair]["f_measure_result_baseline"]
        self.BASELINE_WMT15 = path + settingsMap[language_pair]["baseline_wmt15"]
        self.BASELINE_WMT14_WMT13 = path + settingsMap[language_pair]["baseline_wmt14_wmt13"]
        self.CRF_MESSAGE_OUTPUT = path + settingsMap[language_pair]['crf_message_output']
        self.BASELINE_TEST_MODEL_CRF = path + settingsMap[language_pair]["baseline_test_model_crf"]

        ## for module "Feature Selection"
        #self.ALIGNMENT_FEATURES_NAME = "alignment features"
        self.ALIGNMENT_CONTEXT_POS_NAME = 'alignment context pos'
        self.ALIGNMENT_CONTEXT_STEM_NAME = 'alignment context stem'
        self.ALIGNMENT_CONTEXT_WORD_NAME = 'alignment context word'
        self.SOURCE_POS_NAME = 'source pos'
        self.SOURCE_STEM_NAME = 'source stem'
        self.SOURCE_WORD_NAME = 'source word'
        self.TARGET_POS_NAME = 'target pos'
        self.TARGET_STEM_NAME = 'target stem'
        self.TARGET_WORD_NAME = 'target word'
        self.BACKOFF_BEHAVIOUR_NAME = "backoff behaviour"
        self.CONSTITUENT_LABEL_NAME = "constituent label"
        self.DISTANCE_TO_ROOT_NAME = "distance to root"
        self.LONGEST_SOURCE_GRAM_LENGTH_NAME = "longest source gram length"
        self.LONGEST_TARGET_GRAM_LENGTH_NAME = "longest target gram length"
        self.MAX_EN_NAME = "max"
        self.MIN_EN_NAME = "min"
        self.NODES_NAME = "nodes"
        self.NUMBER_OF_OCCURRENCES_STEM_NAME = "number of occurrences stem"
        self.NUMBER_OF_OCCURRENCES_WORD_NAME = "number of occurrences word"
        self.NUMERIC_NAME = "numeric"
        self.OCCUR_IN_BING_TRANSLATOR_NAME = "occur in bing translator"
        self.OCCUR_IN_GOOGLE_TRANSLATOR_NAME = "occur in google translator"
        self.POLYSEMYCOUNT_TARGET_NAME = "polysemycount target"
        self.PROPER_NAME_NAME = "proper name"
        self.PUNCTUATION_NAME = "punctuation"
        self.STOP_WORD_NAME = "stop word"
        self.UNKNOWN_LEMMA_NAME = "unknown lemma"
        self.WPP_ANY_NAME = "wpp any"
        self.WPP_EXACT_NAME = "wpp exact"

        #self.ALIGNMENT_FEATURES_PATH = path + settingsMap[TOOL_ROOT]['alignment_features']
        self.ALIGNMENT_CONTEXT_POS_PATH = path + settingsMap[TOOL_ROOT]['alignment_context_pos']
        self.ALIGNMENT_CONTEXT_STEM_PATH = path + settingsMap[TOOL_ROOT]['alignment_context_stem']
        self.ALIGNMENT_CONTEXT_WORD_PATH = path + settingsMap[TOOL_ROOT]['alignment_context_word']
        self.SOURCE_POS_PATH = path + settingsMap[TOOL_ROOT]['source_pos']
        self.SOURCE_STEM_PATH = path + settingsMap[TOOL_ROOT]['source_stem']
        self.SOURCE_WORD_PATH = path + settingsMap[TOOL_ROOT]['source_word']
        self.TARGET_POS_PATH = path + settingsMap[TOOL_ROOT]['target_pos']
        self.TARGET_STEM_PATH = path + settingsMap[TOOL_ROOT]['target_stem']
        self.TARGET_WORD_PATH = path + settingsMap[TOOL_ROOT]['target_word']

        self.BACKOFF_BEHAVIOUR_PATH = path + settingsMap[TOOL_ROOT]['backoff_behaviour']
        self.CONSTITUENT_LABEL_PATH = path + settingsMap[TOOL_ROOT]['constituent_label']
        self.DISTANCE_TO_ROOT_PATH = path + settingsMap[TOOL_ROOT]['distance_to_root']
        self.LONGEST_SOURCE_GRAM_LENGTH_PATH = path + settingsMap[TOOL_ROOT]['longest_source_gram_length']
        self.LONGEST_TARGET_GRAM_LENGTH_PATH = path + settingsMap[TOOL_ROOT]['longest_target_gram_length']
        self.MAX_EN_PATH = path + settingsMap[TOOL_ROOT]['max_en']
        self.MIN_EN_PATH = path + settingsMap[TOOL_ROOT]['min_en']
        self.NODES_PATH = path + settingsMap[TOOL_ROOT]['nodes']
        self.NUMBER_OF_OCCURRENCES_STEM_PATH = path + settingsMap[TOOL_ROOT]['number_of_occurrences_stem']
        self.NUMBER_OF_OCCURRENCES_WORD_PATH = path + settingsMap[TOOL_ROOT]['number_of_occurrences_word']
        self.NUMERIC_PATH = path + settingsMap[TOOL_ROOT]['numeric']
        self.OCCUR_IN_BING_TRANSLATOR_PATH = path + settingsMap[TOOL_ROOT]['occur_in_bing_translator']
        self.OCCUR_IN_GOOGLE_TRANSLATOR_PATH = path + settingsMap[TOOL_ROOT]['occur_in_google_translator']
        self.POLYSEMYCOUNT_TARGET_PATH = path + settingsMap[TOOL_ROOT]['polysemycount_target']
        self.PROPER_NAME_PATH = path + settingsMap[TOOL_ROOT]['proper_name']
        self.PUNCTUATION_PATH = path + settingsMap[TOOL_ROOT]['punctuation']
        self.STOP_WORD_PATH = path + settingsMap[TOOL_ROOT]['stop_word']
        self.UNKNOWN_LEMMA_PATH = path + settingsMap[TOOL_ROOT]['unknown_lemma']
        self.WPP_ANY_PATH = path + settingsMap[TOOL_ROOT]['wpp_any']
        self.WPP_EXACT_PATH = path + settingsMap[TOOL_ROOT]['wpp_exact']

        self.FEATURE_LIST['SrcPos'] = path + settingsMap[TOOL_ROOT]['source_pos']
        self.FEATURE_LIST['TgtPos'] = path + settingsMap[TOOL_ROOT]['target_pos']
        self.FEATURE_LIST['TgtWrd'] = path + settingsMap[TOOL_ROOT]['target_word']
        self.FEATURE_LIST['BACKOFF'] = path + settingsMap[TOOL_ROOT]['backoff_behaviour']
        self.FEATURE_LIST['LngSrcNg'] = path + settingsMap[TOOL_ROOT]['longest_source_gram_length']
        self.FEATURE_LIST['LngTgtNg'] = path + settingsMap[TOOL_ROOT]['longest_target_gram_length']
        self.FEATURE_LIST['WPPMax'] = path + settingsMap[TOOL_ROOT]['max_en']
        self.FEATURE_LIST['WPPMIN'] = path + settingsMap[TOOL_ROOT]['min_en']
        self.FEATURE_LIST['Nd'] = path + settingsMap[TOOL_ROOT]['nodes']
        self.FEATURE_LIST['NbrOcStem'] = path + settingsMap[TOOL_ROOT]['number_of_occurrences_stem']
        self.FEATURE_LIST['NbrOcWrd'] = path + settingsMap[TOOL_ROOT]['number_of_occurrences_word']
        self.FEATURE_LIST['Num'] = path + settingsMap[TOOL_ROOT]['numeric']
        self.FEATURE_LIST['Punct'] = path + settingsMap[TOOL_ROOT]['punctuation']
        self.FEATURE_LIST['StpWrd'] = path + settingsMap[TOOL_ROOT]['stop_word']
        self.FEATURE_LIST['WPPAny'] = path + settingsMap[TOOL_ROOT]['wpp_any']
        self.FEATURE_LIST['WPPEx'] = path + settingsMap[TOOL_ROOT]['wpp_exact']
        self.FEATURE_LIST['OcGG'] = path + settingsMap[TOOL_ROOT]['occur_in_google_translator']

        self.FEATURE_LIST['AWrd'] = path + settingsMap[TOOL_ROOT]['alignment_context_word']
        self.FEATURE_LIST['APos'] = path + settingsMap[TOOL_ROOT]['alignment_context_pos']
        self.FEATURE_LIST['PNam'] = path + settingsMap[TOOL_ROOT]['proper_name']
        self.FEATURE_LIST['SrcWrd'] = path + settingsMap[TOOL_ROOT]['source_word']
        self.FEATURE_LIST['ConsLab'] = path + settingsMap[TOOL_ROOT]['constituent_label']
        self.FEATURE_LIST['DistRoot'] = path + settingsMap[TOOL_ROOT]['distance_to_root']
        self.FEATURE_LIST['PolTtgt'] = path + settingsMap[TOOL_ROOT]['polysemycount_target']

        self.FEATURE_LIST['AStm'] = path + settingsMap[TOOL_ROOT]['alignment_context_stem']
        self.FEATURE_LIST['UNKLem'] = path + settingsMap[TOOL_ROOT]['unknown_lemma']
        self.FEATURE_LIST['SrcStm'] = path + settingsMap[TOOL_ROOT]['source_stem']
        self.FEATURE_LIST['TgtStm'] = path + settingsMap[TOOL_ROOT]['target_stem']
        self.FEATURE_LIST['OcBing'] = path + settingsMap[TOOL_ROOT]['occur_in_bing_translator']

        self.ALPHA = 0.7 #bad - weight score
        self.BETA = 0.3 #good - weight score
        self.LOWEST_THRESHOLD = 0.1 #lowest threshold
        self.HIGHEST_THRESHOLD = 0.975 #highest threshold
        self.STEP_THRESHOLD = 0.025 #step of threshold
        self.TEMPLATE_PATH_PATTERN = path + settingsMap[language_pair]['template_path_pattern']
        self.LABEL_GOOD = "G"
        self.LABEL_BAD = "B"
        self.RESULT_WORD_LABEL_THRESHOLD = path + settingsMap[language_pair]['result_word_label_using_threshold_pattern']
        self.RESULT_FEATURE_SELECTION = path + settingsMap[language_pair]['result_feature_selection']

        ##Boosting
        self.TOOL_BOOSTING_PATH = path + settingsMap[TOOL_ROOT]['tool_boosting_path']
        self.NUMBER_OF_FEATURES_BOOSTING = 12
        self.TRAINING_CROSS_VALIDATION_PATH_PATTERN = path + settingsMap[language_pair]['training_cross_validation_path_pattern']
        self.DEVELOPING_CROSS_VALIDATION_PATH_PATTERN = path + settingsMap[language_pair]['developing_cross_validation_path_pattern']
        self.TESTING_CROSS_VALIDATION_PATH_PATTERN = path + settingsMap[language_pair]['testing_cross_validation_path_pattern']
        self.BOOST_TEMPLATE_PATH_PATTERN = path + settingsMap[language_pair]['boost_template_path_pattern']
        self.BOOSTING_CORPUS = 3 #for Boosting corpus in order to generate cross validation, default = 3
        self.NUMBER_OF_CLASSIFIERS = 98
        self.NUMBER_OF_FOLDS = 10 #folds for cross validation, default = 10
        self.NUMBER_OF_SENTENCES_TRAINING_WAPITI = 1088 #default = 1088
        self.NUMBER_OF_SENTENCES_DEVELOPING_WAPITI = 0
        self.DELTA = 20 #vi khi chia 10881 cho 10 folds thi du 1 cau --> can phai lay cau nay dua vao test --> Dung delta de: Neu tong so cau - (num_for_testing*order_n_fold - 1) >= delta thi gan index_end = number_of_sentences_merged_file, default = 10
        self.TRAINING_CORPUS_NAME = path + settingsMap[language_pair]['training_corpus_name']
        self.TRAINING_CORPUS_FOR_BOOSTING_PATH = path + settingsMap[language_pair]['training_corpus_for_boosting_path']
        self.TRAINING_NAMES_FOR_BOOSTING_PATH = path + settingsMap[language_pair]['training_names_for_boosting_path']
        self.BOOSTING_TRAINING_LOG_PATH = path + settingsMap[language_pair]['boosting_training_log_path']
        self.BOOSTING_TESTING_LOG_PATH = path + settingsMap[language_pair]['boosting_testing_log_path']
        self.RESULT_TESTING_PATH = path + settingsMap[language_pair]['result_testing_path']

        ##ASR tasks
        self.TOOL_DIFF = path + settingsMap[TOOL_ROOT]['tool_diff']
        self.FEATURES_VALUES_ASR_PATH = path + settingsMap[language_pair]['features_values_asr_path']
        self.AFTER_SORTING_FEATURES_VALUES_ASR_PATH = path + settingsMap[language_pair]['after_sorting_features_values_asr_path']
        self.OUTPUT_SENTENCES_NOT_ENCODING = path + settingsMap[language_pair]['output_sentences_not_encoding']
        self.OUTPUT_SENTENCES_WITHIN_ENCODING = path + settingsMap[language_pair]['output_sentences_within_encoding']
        self.OUTPUT_FORMAT_ROW_WITHIN_ENCODING = path + settingsMap[language_pair]['output_format_row_within_encoding']
        self.OUTPUT_FORMAT_COLUMN_WITHIN_ENCODING = path + settingsMap[language_pair]['output_format_column_within_encoding']
        self.OUTPUT_FORMAT_COLUMN_RESULT_DIFF = path + settingsMap[language_pair]['output_format_column_result_diff']
        #self.DEFAULT_FEATURES_VALUES_ASR = "id_sent,0,punct,1,0,1,0,0,1,PUN,K."
        #self.DEFAULT_FEATURES_VALUES_ASR_NOT_HAVE_ALIGNMENT = "id_sent,0,not_have_alignment,0,0,0,0,0,0,PUN,C."
        self.DEFAULT_FEATURES_VALUES_ASR = "id_sent,0,pun,0,0,0,0,0,0,PUN"
        self.DEFAULT_FEATURES_VALUES_ASR_NOT_HAVE_ALIGNMENT = "id_sent,0,not_have_alignment,0,0,0,0,0,0,<unknown>"

        #self.TOOL_COMPUTE_SCLITE = path + settingsMap[TOOL_ROOT]['tool_compute_sclite']
        #Dung duong dan tuyet doi
        ###self.TOOL_COMPUTE_SCLITE = settingsMap[TOOL_ROOT]['tool_compute_sclite']
        self.SCLITE_FILES_DIRECTORY_PATH = path + settingsMap[language_pair]['sclite_files_directory_path']
        #self.LATTICE_DIRECTORY_PATH = path + settingsMap[TOOL_ROOT]['lattice_directory_path']
        ###self.LATTICE_DIRECTORY_PATH = settingsMap[TOOL_ROOT]['lattice_directory_path'] #tam thoi dung duong dan tuyet doi

        #for ASR

        # tools configuration
        #-------------------
        #self.TOOL_LATTICE = settingsMap[TOOL_ROOT]['tool_lattice'] #duong dan tuyet doi
        #self.TOOL_GETPRO = settingsMap[TOOL_ROOT]['tool_getpro'] #duong dan tuyet doi
        #self.TREETAGGER_FRENCH = path + settingsMap[TOOL_ROOT]['treetagger_french']

        # models configuration
        #---------------------
        #lm="/home/lecouteu/KALDI.V2/exp/nnet5c/decode_dev_ant_2g/out_myconvert/"
        #base_name="BigLM4"
        #"/home/lecouteu/KALDI.FR/exp_full_big/sgmm2_5b2_mixedubm_big/decode_bref/"
        #self.LM_ASR = settingsMap[TOOL_ROOT]['lm_asr'] #duong dan tuyet doi
        self.BASE_NAME = "nouveaumodele" #base_name
        self.LMSCALE = 10 #lmscale
        self.ACSCALE = 0 #acscale

        # label name
        #--------------------
        #GOODLABEL="C"
        #BADLABEL="E"
        #self.LABEL_GOOD = "G"
        #self.LABEL_BAD = "B"

        self.ERROR_WORDS_OUTPUT = path + settingsMap[language_pair]['error_words_output']

        # table formate configuration
        #---------------------
        self.PRINT_TEMPLATE = "{0:20}{1:12}{2:15}{3:12}{4:12}{5:15}{6:12}{7:12}{8:15}{9:12}{10:12}{11:12}" #print_template
        self.TOOL_ANALYSE_ERREURS = path + settingsMap[TOOL_ROOT]['tool_analyse_erreurs']


        ##For Giza++ alignment
        self.TARGET_SOURCE_A3_FINAL = path + settingsMap[language_pair]['target_source_A3_final']
        self.TOOL_GIZA = path + settingsMap[TOOL_ROOT]['tool_giza']
        ###self.PATH_TO_TOOL_GIZA = path + settingsMap[TOOL_ROOT]['path_to_tool_giza']
        ###self.PATH_TO_TOOL_MKCLS = path + settingsMap[TOOL_ROOT]['path_to_tool_mkcls']
        self.PATH_TO_CORPUS = path + settingsMap[language_pair]['path_to_corpus']
        self.SOURCE_CORPUS_NAME = settingsMap[language_pair]['source_corpus_name']
        self.TARGET_CORPUS_NAME = settingsMap[language_pair]['target_corpus_name']

        ##MOSES
        self.MODEL_DIR_PATH = path + settingsMap[language_pair]['model_dir_path']

        ### For WMT14 & WMT13
        self.WMT14_TRAIN_SOURCE = path + settingsMap[language_pair]['wmt14_train_source']
        self.WMT14_TRAIN_SOURCE_TEMP = path + settingsMap[language_pair]['wmt14_train_source_temp']
        self.WMT14_TRAIN_TARGET = path + settingsMap[language_pair]['wmt14_train_target']
        self.WMT14_TRAIN_TAG = path + settingsMap[language_pair]['wmt14_train_tag']
        self.WMT14_TEST_SOURCE = path + settingsMap[language_pair]['wmt14_test_source']
        self.WMT14_TEST_SOURCE_TEMP = path + settingsMap[language_pair]['wmt14_test_source_temp']
        self.WMT14_TEST_TARGET = path + settingsMap[language_pair]['wmt14_test_target']
        self.WMT14_TEST_TAG = path + settingsMap[language_pair]['wmt14_test_tag']

        self.WMT13_TRAIN_SOURCE = path + settingsMap[language_pair]['wmt13_train_source']
        self.WMT13_TRAIN_TARGET = path + settingsMap[language_pair]['wmt13_train_target']
        self.WMT13_TRAIN_TAG = path + settingsMap[language_pair]['wmt13_train_tag']
        self.WMT13_TEST_SOURCE = path + settingsMap[language_pair]['wmt13_test_source']
        self.WMT13_TEST_TARGET = path + settingsMap[language_pair]['wmt13_test_target']
        self.WMT13_TEST_TAG = path + settingsMap[language_pair]['wmt13_test_tag']

        #combination of wmt14_wmt13_train_test
        self.WMT14_WMT13_TRAIN_SOURCE = path + settingsMap[language_pair]['wmt14_wmt13_train_source']
        self.WMT14_WMT13_TRAIN_TARGET = path + settingsMap[language_pair]['wmt14_wmt13_train_target']
        self.WMT14_WMT13_TRAIN_TAG = path + settingsMap[language_pair]['wmt14_wmt13_train_tag']
        self.WMT14_WMT13_TEST_SOURCE = path + settingsMap[language_pair]['wmt14_wmt13_test_source']
        self.WMT14_WMT13_TEST_TARGET = path + settingsMap[language_pair]['wmt14_wmt13_test_target']
        self.WMT14_WMT13_TEST_TAG = path + settingsMap[language_pair]['wmt14_wmt13_test_tag']
        self.WMT14_WMT13_TRAIN_TEST_SOURCE = path + settingsMap[language_pair]['wmt14_wmt13_train_test_source']
        self.WMT14_WMT13_TRAIN_TEST_TARGET = path + settingsMap[language_pair]['wmt14_wmt13_train_test_target']
        self.WMT14_WMT13_TRAIN_TEST_TAG = path + settingsMap[language_pair]['wmt14_wmt13_train_test_tag']

        #For OAR
        self.LIST_OF_SERVER_NAME = ["bach0","bach1","bach2","bach3","bach4","bach5"]
        self.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_PATTERN = path + settingsMap[language_pair]['target_ref_test_output_treetagger_format_col_pattern']
        self.MERGED_FILES = path + settingsMap[language_pair]['merged_files']

        #For converting text to int
        self.FEATURE_BACKOFF_BEHAVIOUR = 1
        self.FEATURE_CONSTITUENT_LABEL = 2
        self.FEATURE_ALIGNMENT = 3

        ## For APE 2015
        self.FILE_OUTPUT_PATTERN = path + settingsMap[language_pair]['file_output_pattern']

#**************************************************************************#
if __name__ == "__main__":
    #Test case:

    path_file_configuration = "configuration.yml"

    obj = config(path_file_configuration)

    #print(path_file_configuration)

    print('OK')
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

    print ('OK')
    """
#**************************************************************************#
