# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:25:15 2014
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

from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_util import print_time, print_result
from common_module.cm_file import convert_format_column_to_format_row

from feature.punctuation import feature_punctuation
from feature.stop_word import get_feature_stop_word
from feature.numeric import feature_numeric
from feature.proper_name import feature_proper_name
from feature.unknown_lemma import feature_unknown_lemma
from feature.number_of_occurrences_word import feature_number_of_occurrences_word
from feature.number_of_occurrences_stem import feature_number_of_occurrences_stem
from feature.occur_in_bing_translate import feature_occur_in_bing_translate
from feature.occur_in_google_translate import feature_occur_in_google_translate
from feature.occur_in_translator import feature_occur_in_translators

from feature.longest_target_gram_length import get_probability_from_language_model, create_longest_target_gram_length
from feature.longest_source_gram_length import get_temp_longest_source_gram_length_not_aligned_target, feature_longest_gram_source_length
from feature.backoff_behaviour import feature_backoff_behaviour
from feature.alignment_features import get_alignment_features
from feature.constituent_label_distance_to_root import feature_constituent_label_get_list_distance_to_root_null_link
from feature.polysemy_count_common import convert_format_treetagger_to_format_babelnet, feature_polysemy_count_language, filter_number_of_polysemy
from feature.polysemy_count_english import dict_tagset_english
from feature.polysemy_count_french import dict_tagset_french
from feature.polysemy_count_spanish import dict_tagset_spanish
from feature.wpp_nodes_min_max import feature_wpp_nodes_min_max
from feature.wpp_exact import feature_wpp_exact
from feature.label_word import extracting_label_for_word_format_column, extracting_given_label
from feature.polysemy_count_within_given_target_language import get_polysemy_count_within_given_target_language

#*****************************************************************************#
def extracting_all_features(result_output_path):
    """
    Extracting all features

    :type result_output_path: string
    :param result_output_path: path of log-file that contains results of DEMO
    """
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #You should update target language
    target_language = config_end_user.TARGET_LANGUAGE

    #target_language = current_config.LANGUAGE_SPANISH # Spanish
    #target_language = current_config.LANGUAGE_ENGLISH # English
    #target_language = current_config.LANGUAGE_FRENCH # French

    #introduction of this solution
    #print_introduction(result_output_path)

    feature_name = "BEGIN Task - Extracting Features"
    print_time(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Punctuation
    ##########################################################################
    feature_name = "Punctuation"
    print_time(feature_name, result_output_path)
    feature_punctuation(current_config.TARGET_REF_TEST_FORMAT_COL, current_config.LIST_PUNCTUATIONS, current_config.PUNCTUATION)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Stop Word
    ##########################################################################
    feature_name = "Stop Word" #List of stop word phu thuoc vao ngon ngu dich
    print_time(feature_name, result_output_path)
    get_feature_stop_word( current_config.TARGET_REF_TEST_FORMAT_COL, target_language, current_config.STOP_WORD)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Numeric
    ##########################################################################
    feature_name = "Numeric"
    print_time(feature_name, result_output_path)
    feature_numeric( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.NUMERIC)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Proper Name
    ##########################################################################
    feature_name = "Proper Name" #List of POS-Proper name phu thuoc vao ngon ngu dich
    print_time(feature_name, result_output_path)
    feature_proper_name( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, target_language, current_config.PROPER_NAME)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Unknown Lemma
    ##########################################################################
    feature_name = "Unknown Lemma"
    print_time(feature_name, result_output_path)
    feature_unknown_lemma( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, current_config.UNKNOWN_LEMMA)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Number Of Occurrences word
    ##########################################################################
    feature_name = "Number Of Occurrences word"
    print_time(feature_name, result_output_path)
    feature_number_of_occurrences_word( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL,  current_config.NUMBER_OF_OCCURRENCES_WORD)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Number Of Occurrences stem (frequency of stemmed word)
    ##########################################################################
    feature_name = "Number Of Occurrences stemmed word"
    print_time(feature_name, result_output_path)
    feature_number_of_occurrences_stem( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL,  current_config.NUMBER_OF_OCCURRENCES_STEM)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Occur in Google Translatator
    ##########################################################################
    feature_name = "Occur in Google Translatator"
    print_time(feature_name, result_output_path)
    #feature_occur_in_google_translate( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.GOOGLE_TRANSLATE_CORPUS, current_config.OCCUR_IN_GOOGLE_TRANSLATE)
    feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.GOOGLE_TRANSLATE_CORPUS, current_config.OCCUR_IN_GOOGLE_TRANSLATE)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Occur in Bing Translatator
    ##########################################################################
    feature_name = "Occur in Bing Translatator"
    print_time(feature_name, result_output_path)
    #feature_occur_in_bing_translate( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.BING_TRANSLATE_CORPUS, current_config.OCCUR_IN_BING_TRANSLATE)
    feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.BING_TRANSLATE_CORPUS, current_config.OCCUR_IN_BING_TRANSLATE)
    print_result(feature_name, result_output_path)

    #143-270
    ##########################################################################
    ## Feature: Longest Target gram length
    ##########################################################################
    feature_name = "Longest Target gram length"
    print_time(feature_name, result_output_path)

    #da fix loi SRILM vi file trong /srilm/bin/i686-m64 -> chmod +x *
    #Buoc 1: Tao file chua xac suat theo tung gram (Language Model)
    #Goi ham ngram tu SRILM
    #Test case: checking the function
    #get_probability_from_language_model(file_input_path, language_model_path,  n_gram, file_output_path)
    #get_probability_from_language_model( current_config.HYPOTHESIS_ROW_CORPUS, current_config.LANGUAGE_MODEL_TGT, 5, current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS)
    get_probability_from_language_model( current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_MODEL_TGT, 5, current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS)

    #Buoc 2:
    #create_longest_target_gram_length(file_input_path, file_output_path)
    create_longest_target_gram_length( current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS, current_config.LONGEST_TARGET_GRAM_LENGTH)

    print_result(feature_name, result_output_path)


    ##########################################################################
    ## Feature: Longest Source gram length
    ## Phan nay chay kha lau
    ##########################################################################
    if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
        feature_name = "Longest Source gram length"
        print_time(feature_name, result_output_path)

        #Buoc 1: File Source-ngram giong nhu cach lam Target-ngram
        get_temp_longest_source_gram_length_not_aligned_target( current_config.SRC_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_MODEL_SRC, current_config.N_GRAM, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET)

        #convert format column to format row
        #trong du lieu cot thi nen them 1 dong trong nua, neu khong se bi mat sentence du lieu cuoi cung
        convert_format_column_to_format_row( current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW)

        #feature_longest_gram_source_length(file_output_from_moses_included_alignment_word_to_word_path,  file_temp_longest_source_gram_length_not_aligned_target_row_path, type_longest_gram_source_length, file_output_path)
        #type_longest_gram_source_length
        #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX = 1
        #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN = 2
        #TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG = 3
        #TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST = 4
        feature_longest_gram_source_length( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW, current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL, current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

        print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Backoff Behaviour
    ##########################################################################
    feature_name = "Backoff Behaviour"
    print_time(feature_name, result_output_path)
    feature_backoff_behaviour( current_config.LONGEST_TARGET_GRAM_LENGTH, current_config.BACKOFF_BEHAVIOUR)
    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Alignment Features = 6 * 3 = 18 features
    ## Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
    ## Word; POS; Stemming
    ##########################################################################
    if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
        feature_name = "Alignment Features"
        print_time(feature_name, result_output_path)

        get_alignment_features( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.ALIGNMENT_FEATURES)

        print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature:  WPP Exact
    ##########################################################################
    if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
        feature_name = "WPP Exact"
        print_time(feature_name, result_output_path)
        feature_wpp_exact( current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT,  current_config.WPP_EXACT)
        print_result(feature_name, result_output_path)
    ##########################################################################
    ## Feature: Constituent Label & Distance to Root
    ##########################################################################
    #can cai dat NLTK 3.0 within supporting python3
    feature_name = "Constituent Label & Distance to Root using NLTK 3.0 within supporting python3"
    print_time(feature_name, result_output_path)

    #Doc lap ngon ngu
    feature_constituent_label_get_list_distance_to_root_null_link( current_config.TARGET_REF_TEST_FORMAT_ROW, target_language, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL)

    print_result(feature_name, result_output_path)

    ##########################################################################
    ## Feature: Polysemy Count - Target (Support English, French and Spanish)
    ##########################################################################
    feature_name = "Polysemy Count - Target"
    print_time(feature_name, result_output_path)

    file_input_path = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL
    file_output_path = current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST

    get_polysemy_count_within_given_target_language(target_language, file_input_path, file_output_path)

    print_result(feature_name, result_output_path)
    ##########################################################################
    ## Feature:  WPP any, Max, Min, Nodes
    ##########################################################################
    if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
        feature_name = "WPP any, Max, Min, Nodes"
        print_time(feature_name, result_output_path)

        feature_wpp_nodes_min_max(current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT,  current_config.TOOL_N_BEST_TO_LATTICE, current_config.WPP_NODES_MIN_MAX_TEMP, current_config.WPP_NODES_MIN_MAX)
        print_result(feature_name, result_output_path)


    ##########################################################################
    ## Feature: Label - Word (Using Terpa)
    ##########################################################################
    feature_name = "Label - Word (Given Label)"
    print_time(feature_name, result_output_path)

    extracting_label_for_word_format_column(current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT)

    print_result(feature_name, result_output_path)

    ##########################################################################
    feature_name = "END Task - Extracting Features"
    print_time(feature_name, result_output_path)

#*****************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()

    config_end_user = load_config_end_user()

    result_output_path = current_config.RESULT_MESSAGE_OUTPUT

    extracting_all_features(result_output_path)

    print ('OK')
