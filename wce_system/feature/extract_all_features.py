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
import threading
import time

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_util import print_time, print_result
from common_module.cm_file import convert_format_column_to_format_row, delete_all_files_temporary_threads, delete_already_existed_file

from feature.punctuation import feature_punctuation
from feature.stop_word import get_feature_stop_word
from feature.numeric import feature_numeric
from feature.proper_name import feature_proper_name, feature_proper_name_threads
from feature.unknown_lemma import feature_unknown_lemma
from feature.number_of_occurrences_word import feature_number_of_occurrences_word
from feature.number_of_occurrences_stem import feature_number_of_occurrences_stem
from feature.occur_in_bing_translate import feature_occur_in_bing_translate
from feature.occur_in_google_translate import feature_occur_in_google_translate
from feature.occur_in_translator import feature_occur_in_translators

from feature.longest_target_gram_length import get_probability_from_language_model, create_longest_target_gram_length, get_probability_from_language_model_threads, create_longest_target_gram_length_threads
from feature.longest_source_gram_length import get_temp_longest_source_gram_length_not_aligned_target, feature_longest_gram_source_length, get_temp_longest_source_gram_length_not_aligned_target_threads, feature_longest_gram_source_length_threads
from feature.backoff_behaviour import feature_backoff_behaviour
from feature.alignment_features import get_alignment_features, get_alignment_features_threads
from feature.constituent_label_distance_to_root import feature_constituent_label_get_list_distance_to_root_null_link, feature_constituent_label_get_list_distance_to_root_null_link_threads
from feature.polysemy_count_common import convert_format_treetagger_to_format_babelnet, feature_polysemy_count_language, filter_number_of_polysemy
from feature.polysemy_count_english import dict_tagset_english
from feature.polysemy_count_french import dict_tagset_french
from feature.polysemy_count_spanish import dict_tagset_spanish
from feature.wpp_nodes_min_max import feature_wpp_nodes_min_max, feature_wpp_nodes_min_max_threads
from feature.wpp_exact import feature_wpp_exact, feature_wpp_exact_threads
from feature.label_word import extracting_label_for_word_format_column, extracting_given_label, extracting_label_for_word_format_column_threads
from feature.polysemy_count_within_given_target_language import get_polysemy_count_within_given_target_language, get_polysemy_count_within_given_target_language_threads, get_polysemy_count_within_given_target_language_with_dbnary, get_polysemy_count_within_given_target_language_with_dbnary_threads

#*****************************************************************************#
def extracting_all_features(log_path):
    """
    Extracting all features

    :type log_path: string
    :param log_path: path of log-file that contains results of DEMO
    """
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #You should update target language
    target_language = config_end_user.TARGET_LANGUAGE

    #target_language = current_config.LANGUAGE_SPANISH # Spanish
    #target_language = current_config.LANGUAGE_ENGLISH # English
    #target_language = current_config.LANGUAGE_FRENCH # French

    #introduction of this solution
    #print_introduction(log_path)

    feature_name = "BEGIN Task - Extracting Features"
    print_time(feature_name, log_path)

    ##########################################################################
    ## Feature: Punctuation
    ##########################################################################
    if current_config.punctuation:
      feature_name = "Punctuation"
      print_time(feature_name, log_path)
      feature_punctuation(current_config.TARGET_REF_TEST_FORMAT_COL, current_config.LIST_PUNCTUATIONS, current_config.PUNCTUATION)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Stop Word
    ##########################################################################
    if current_config.stop_words:
      feature_name = "Stop Word" #List of stop word phu thuoc vao ngon ngu dich
      print_time(feature_name, log_path)
      get_feature_stop_word( current_config.TARGET_REF_TEST_FORMAT_COL, target_language, current_config.STOP_WORD)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Numeric
    ##########################################################################
    if current_config.numeric:
      feature_name = "Numeric"
      print_time(feature_name, log_path)
      feature_numeric( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.NUMERIC)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Proper Name
    ##########################################################################
    if current_config.proper_name:
      feature_name = "Proper Name" #List of POS-Proper name phu thuoc vao ngon ngu dich
      print_time(feature_name, log_path)
      feature_proper_name( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, target_language, current_config.PROPER_NAME)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Unknown Lemma
    ##########################################################################
    if current_config.unknown_lemma:
      feature_name = "Unknown Lemma"
      print_time(feature_name, log_path)
      feature_unknown_lemma( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL, current_config.UNKNOWN_LEMMA)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Number Of Occurrences word
    ##########################################################################
    if current_config.occurence_words:
      feature_name = "Number Of Occurrences word"
      print_time(feature_name, log_path)
      feature_number_of_occurrences_word( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL,  current_config.NUMBER_OF_OCCURRENCES_WORD)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Number Of Occurrences stem (frequency of stemmed word)
    ##########################################################################
    if current_config.occurence_stems:
      feature_name = "Number Of Occurrences stemmed word"
      print_time(feature_name, log_path)
      feature_number_of_occurrences_stem( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL,  current_config.NUMBER_OF_OCCURRENCES_STEM)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Occur in Google Translatator
    ##########################################################################
    if current_config.google_translator:
      feature_name = "Occur in Google Translatator"
      print_time(feature_name, log_path)
      #feature_occur_in_google_translate( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.GOOGLE_TRANSLATE_CORPUS, current_config.OCCUR_IN_GOOGLE_TRANSLATE)
      feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.GOOGLE_TRANSLATE_CORPUS, current_config.OCCUR_IN_GOOGLE_TRANSLATE)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Occur in Bing Translatator
    ##########################################################################
    if current_config.bing_translator:
      feature_name = "Occur in Bing Translatator"
      print_time(feature_name, log_path)
      #feature_occur_in_bing_translate( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.BING_TRANSLATE_CORPUS, current_config.OCCUR_IN_BING_TRANSLATE)
      feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL, current_config.BING_TRANSLATE_CORPUS, current_config.OCCUR_IN_BING_TRANSLATE)
      print_result(feature_name, log_path)

    #143-270
    ##########################################################################
    ## Feature: Longest Target gram length
    ##########################################################################
    if current_config.longest_ngram_length_tgt:
      feature_name = "Longest Target gram length"
      print_time(feature_name, log_path)

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

      print_result(feature_name, log_path)


    ##########################################################################
    ## Feature: Longest Source gram length
    ## Phan nay chay kha lau
    ##########################################################################
    if current_config.longest_ngram_length_src:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "Longest Source gram length"
          print_time(feature_name, log_path)

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

          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Backoff Behaviour
    ##########################################################################
    if current_config.backoff:
      feature_name = "Backoff Behaviour"
      print_time(feature_name, log_path)
      feature_backoff_behaviour( current_config.LONGEST_TARGET_GRAM_LENGTH, current_config.BACKOFF_BEHAVIOUR)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Alignment Features = 6 * 3 = 18 features
    ## Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
    ## Word; POS; Stemming
    ##########################################################################
    if current_config.alignments:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "Alignment Features"
          print_time(feature_name, log_path)

          get_alignment_features( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.ALIGNMENT_FEATURES)

          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature:  WPP Exact
    ##########################################################################
    if current_config.wpp:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "WPP Exact"
          print_time(feature_name, log_path)
          feature_wpp_exact( current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT,  current_config.WPP_EXACT)
          print_result(feature_name, log_path)
    ##########################################################################
    ## Feature: Constituent Label & Distance to Root
    ##########################################################################
    if current_config.distance_to_root:
      feature_name = "Constituent Label & Distance to Root using NLTK 3.0 within supporting python3"
      print_time(feature_name, log_path)

      #Doc lap ngon ngu
      feature_constituent_label_get_list_distance_to_root_null_link( current_config.TARGET_REF_TEST_FORMAT_ROW, target_language, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL)

      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Polysemy Count - Target (Support English, French and Spanish)
    ##########################################################################
    if current_config.polysemy_count_target:
      feature_name = "Polysemy Count - Target"
      print_time(feature_name, log_path)

      file_input_path = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL
      file_output_path = current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST

      get_polysemy_count_within_given_target_language(target_language, file_input_path, file_output_path)

      print_result(feature_name, log_path)
    ##########################################################################
    ## Feature:  WPP any, Max, Min, Nodes
    ##########################################################################
    if current_config.wpp_any:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "WPP any, Max, Min, Nodes"
          print_time(feature_name, log_path)

          feature_wpp_nodes_min_max(current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT,  current_config.TOOL_N_BEST_TO_LATTICE, current_config.WPP_NODES_MIN_MAX_TEMP, current_config.WPP_NODES_MIN_MAX)
          print_result(feature_name, log_path)


    ##########################################################################
    ## Feature: Label - Word (Using Terpa)
    ##########################################################################
    if current_config.label:
      feature_name = "Label - Word (Given Label)"
      print_time(feature_name, log_path)

      extracting_label_for_word_format_column(current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT)

      print_result(feature_name, log_path)

    ##########################################################################
    feature_name = "END Task - Extracting Features"
    print_time(feature_name, log_path)

#*****************************************************************************#
def extracting_all_features_threads(log_path):
    """
    Extracting all features

    :type log_path: string
    :param log_path: path of log-file that contains results of DEMO
    """
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #You should update target language
    target_language = config_end_user.TARGET_LANGUAGE

    #target_language = current_config.LANGUAGE_SPANISH # Spanish
    #target_language = current_config.LANGUAGE_ENGLISH # English
    #target_language = current_config.LANGUAGE_FRENCH # French

    #introduction of this solution
    #print_introduction(log_path)

    feature_name = "BEGIN Task - Extracting Features"
    print_time(feature_name, log_path)

    ##########################################################################
    ## Feature: Punctuation
    ##########################################################################
    if current_config.punctuation:
      feature_name = "Punctuation"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_punctuation(current_config.TARGET_REF_TEST_FORMAT_COL+"."+str(l_inc), current_config.LIST_PUNCTUATIONS, current_config.PUNCTUATION+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Stop Word
    ##########################################################################
    if current_config.stop_words:
      feature_name = "Stop Word" #List of stop word phu thuoc vao ngon ngu dich
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        get_feature_stop_word( current_config.TARGET_REF_TEST_FORMAT_COL+"."+str(l_inc), target_language, current_config.STOP_WORD+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Numeric
    ##########################################################################
    if current_config.numeric:
      feature_name = "Numeric"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_numeric( current_config.TARGET_REF_TEST_FORMAT_COL+"."+str(l_inc), current_config.NUMERIC+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Proper Name
    ##########################################################################
    if current_config.proper_name:
      feature_name = "Proper Name" #List of POS-Proper name phu thuoc vao ngon ngu dich
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_proper_name_threads( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL+"."+str(l_inc), target_language, current_config.PROPER_NAME+"."+str(l_inc), current_config)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Unknown Lemma
    ##########################################################################
    if current_config.unknown_lemma:
      feature_name = "Unknown Lemma"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_unknown_lemma( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL+"."+str(l_inc), current_config.UNKNOWN_LEMMA+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Number Of Occurrences word
    ##########################################################################
    if current_config.occurence_words:
      feature_name = "Number Of Occurrences word"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_number_of_occurrences_word( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL+"."+str(l_inc),  current_config.NUMBER_OF_OCCURRENCES_WORD+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Number Of Occurrences stem (frequency of stemmed word)
    ##########################################################################
    if current_config.occurence_stems:
      feature_name = "Number Of Occurrences stemmed word"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_number_of_occurrences_stem( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL+"."+str(l_inc),  current_config.NUMBER_OF_OCCURRENCES_STEM+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Occur in Google Translatator
    ##########################################################################
    if current_config.google_translator:
      feature_name = "Occur in Google Translatator"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL+"."+str(l_inc), current_config.GOOGLE_TRANSLATE_CORPUS+"."+str(l_inc), current_config.OCCUR_IN_GOOGLE_TRANSLATE+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Occur in Bing Translatator
    ##########################################################################
    if current_config.bing_translator:
      feature_name = "Occur in Bing Translatator"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL+"."+str(l_inc), current_config.BING_TRANSLATE_CORPUS+"."+str(l_inc), current_config.OCCUR_IN_BING_TRANSLATE+"."+str(l_inc))
      print_result(feature_name, log_path)

    #143-270
    ##########################################################################
    ## Feature: Longest Target gram length
    ##########################################################################
    if current_config.longest_ngram_length_tgt:
      feature_name = "Longest Target gram length"
      print_time(feature_name, log_path)

      get_probability_from_language_model_threads( current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_MODEL_TGT, 5, current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS, current_config, config_end_user)

      create_longest_target_gram_length_threads( current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS, current_config.LONGEST_TARGET_GRAM_LENGTH, current_config)

      print_result(feature_name, log_path)


    ##########################################################################
    ## Feature: Longest Source gram length
    ##########################################################################
    if current_config.longest_ngram_length_src:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "Longest Source gram length"
          print_time(feature_name, log_path)

          #Buoc 1: File Source-ngram giong nhu cach lam Target-ngram
          get_temp_longest_source_gram_length_not_aligned_target_threads( current_config.SRC_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_MODEL_SRC, current_config.N_GRAM, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET, current_config, config_end_user)

          #convert format column to format row
          #trong du lieu cot thi nen them 1 dong trong nua, neu khong se bi mat sentence du lieu cuoi cung
          for l_inc in range(1,current_config.THREADS+1):
            #print (current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET+"."+str(l_inc))
            #print (current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW+"."+str(l_inc))
            convert_format_column_to_format_row( current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET+"."+str(l_inc), current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW+"."+str(l_inc))
  #        convert_format_column_to_format_row( current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW)

          #feature_longest_gram_source_length(file_output_from_moses_included_alignment_word_to_word_path,  file_temp_longest_source_gram_length_not_aligned_target_row_path, type_longest_gram_source_length, file_output_path)
          #type_longest_gram_source_length
          #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MAX = 1
          #TYPE_LONGEST_SOURCE_GRAM_LENGTH_MIN = 2
          #TYPE_LONGEST_SOURCE_GRAM_LENGTH_AVG = 3
          #TYPE_LONGEST_SOURCE_GRAM_LENGTH_FIRST = 4
          l_threads = []
          for l_inc in range(1,current_config.THREADS+1):
            #print(command_line)
            #command_line_thread = path_script + " " + file_input_path+"."+str(l_inc) + " " + file_output_path+"."+str(l_inc)
            ts = threading.Thread(target=feature_longest_gram_source_length_threads , args=(current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT+"."+str(l_inc), current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW+"."+str(l_inc), current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL, current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET+"."+str(l_inc), current_config, config_end_user))
            #ts = threading.Thread(target=call_script, args=(command_line_thread, script_path))
            l_threads.append(ts)
            ts.start()
          for myT in l_threads:
            myT.join()

          #for l_inc in range(1,current_config.THREADS+1):
          #feature_longest_gram_source_length_threads (current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW, current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL, current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET, current_config, config_end_user)
  #        feature_longest_gram_source_length( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW, current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL, current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET)

          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Backoff Behaviour
    ##########################################################################
    if current_config.backoff:
      feature_name = "Backoff Behaviour"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_backoff_behaviour( current_config.LONGEST_TARGET_GRAM_LENGTH+"."+str(l_inc), current_config.BACKOFF_BEHAVIOUR+"."+str(l_inc))
  #    feature_backoff_behaviour( current_config.LONGEST_TARGET_GRAM_LENGTH, current_config.BACKOFF_BEHAVIOUR)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Alignment Features = 6 * 3 = 18 features
    ## Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
    ## Word; POS; Stemming
    ##########################################################################
    if current_config.alignments:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "Alignment Features"
          print_time(feature_name, log_path)
          for l_inc in range(1,current_config.THREADS+1):
            get_alignment_features_threads( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT+"."+str(l_inc), current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW+"."+str(l_inc), current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW+"."+str(l_inc), current_config.ALIGNMENT_FEATURES+"."+str(l_inc), config_end_user)
  #        get_alignment_features( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.ALIGNMENT_FEATURES)
          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature:  WPP Exact
    ##########################################################################
    if current_config.wpp:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "WPP Exact"
          print_time(feature_name, log_path)

          for l_inc in range(1,current_config.THREADS+1):
            file_output_path_temp = current_config.WPP_EXACT+"."+str(l_inc)
            # Delete extracted files (because they used mode "append")
            message="WARNING: " + file_output_path_temp + " already exists and will be deleted!\n"
            delete_already_existed_file(file_output_path_temp, message)
          #end for

          #for l_inc in range(1,current_config.THREADS+1):
          #for l_inc in range(2,4):
            #feature_wpp_exact_threads( current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT+"."+str(l_inc), current_config.WPP_EXACT+"."+str(l_inc), l_inc , current_config)
          l_threads = []
          for l_inc in range(1,current_config.THREADS+1):
            ts = threading.Thread(target=feature_wpp_exact_threads , args=(current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT+"."+str(l_inc), current_config.WPP_EXACT+"."+str(l_inc), l_inc , current_config))
            l_threads.append(ts)
            ts.start()
          for myT in l_threads:
            myT.join()

          #delete_all_files_temporary_threads(current_config)
          #delete_all_files_temporary_threads(current_config)
          print_result(feature_name, log_path)
    ##########################################################################
    ## Feature: Constituent Label & Distance to Root
    ##########################################################################
    if current_config.distance_to_root:
      feature_name = "Constituent Label & Distance to Root using NLTK 3.0 within supporting python3"
      print_time(feature_name, log_path)

      #Doc lap ngon ngu
      #l_threads = []
      feature_constituent_label_get_list_distance_to_root_null_link_threads( current_config.TARGET_REF_TEST_FORMAT_ROW, target_language, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL, current_config, config_end_user)
      print_result(feature_name, log_path)


    ##########################################################################
    ## Feature: Polysemy Count - Target (Support English, French and Spanish)
    ##########################################################################
    if current_config.polysemy_count_target:
      feature_name = "Polysemy Count - Target"
      print_time(feature_name, log_path)

      file_input_path = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL
      file_output_path = current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST

      l_threads = []
      for l_inc in range(1,current_config.THREADS+1):
      #for l_inc in range(5,7):
        ts = threading.Thread(target=get_polysemy_count_within_given_target_language_threads , args=(current_config, config_end_user, target_language, file_input_path+"."+str(l_inc), file_output_path+"."+str(l_inc), l_inc))
        #current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT+"."+str(l_inc), current_config.WPP_EXACT+"."+str(l_inc), l_inc , current_config))
        l_threads.append(ts)
        ts.start()
        time.sleep(1)
      for myT in l_threads:
        myT.join()

      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Polysemy Count - Target using DBnary (Support English, French and Spanish)
    ##########################################################################
    if current_config.polysemy_count_target_dbnary:
      feature_name = "Polysemy Count - Target using DBnary"
      print_time(feature_name, log_path)

      file_input_path = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL
      file_output_path = current_config.DBNARY_OUTPUT_CORPUS_TGT_LAST

      l_threads = []
      for l_inc in range(1,current_config.THREADS+1):
      #for l_inc in range(5,7):
        ts = threading.Thread(target=get_polysemy_count_within_given_target_language_with_dbnary_threads , args=(current_config, config_end_user, target_language, file_input_path+"."+str(l_inc), file_output_path+"."+str(l_inc), l_inc))
        #current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT+"."+str(l_inc), current_config.WPP_EXACT+"."+str(l_inc), l_inc , current_config))
        l_threads.append(ts)
        ts.start()
        time.sleep(1)
      for myT in l_threads:
        myT.join()

      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature:  WPP any, Max, Min, Nodes
    ##########################################################################
    if current_config.wpp_any:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "WPP any, Max, Min, Nodes"
          print_time(feature_name, log_path)

          feature_wpp_nodes_min_max_threads(current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT,  current_config.TOOL_N_BEST_TO_LATTICE_THREADS, current_config.WPP_NODES_MIN_MAX_TEMP, current_config.WPP_NODES_MIN_MAX, current_config, config_end_user)
          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Label - Word (Using Terpa)
    ##########################################################################
    if current_config.label:
      feature_name = "Label - Word (Given Label)"
      print_time(feature_name, log_path)
      #extracting_label_for_word_format_column_threads(current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT, current_config, config_end_user)

      l_threads = []
      for l_inc in range(1,current_config.THREADS+1):
        ts = threading.Thread(target=extracting_label_for_word_format_column_threads , args=(current_config.TARGET_REF_TEST_FORMAT_ROW+"."+str(l_inc), current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING+"."+str(l_inc), current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT+"."+str(l_inc), l_inc, current_config, config_end_user))
                              #(file_hypothesis_path+"."+str(l_inc), file_reference_path+"."+str(l_inc), input_extension, output_extension))
        #ts = threading.Thread(target=get_polysemy_count_within_given_target_language_threads , args=(current_config, config_end_user, target_language, file_input_path+"."+str(l_inc), file_output_path+"."+str(l_inc)))
        l_threads.append(ts)
        time.sleep(1)
        ts.start()
      for myT in l_threads:
        myT.join()


    ##########################################################################
    feature_name = "END Task - Extracting Features"
    print_time(feature_name, log_path)
#*****************************************************************************#
def extracting_all_features_new_corpus_threads(log_path, config_end_user, current_config, extension="_new_corpus"):
    """
    Extracting all features

    :type log_path: string
    :param log_path: path of log-file that contains results of DEMO
    """
    #current_config = load_configuration()
    #config_end_user = load_config_end_user()

    #You should update target language
    target_language = config_end_user.TARGET_LANGUAGE

    feature_name = "BEGIN Task - Extracting Features"
    print_time(feature_name, log_path)

    ##########################################################################
    ## Feature: Punctuation
    ##########################################################################
    if current_config.punctuation:
      feature_name = "Punctuation"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_punctuation(current_config.TARGET_REF_TEST_FORMAT_COL_NEW_CORPUS+"."+str(l_inc), current_config.LIST_PUNCTUATIONS, current_config.PUNCTUATION+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Stop Word
    ##########################################################################
    if current_config.stop_words:
      feature_name = "Stop Word"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        get_feature_stop_word( current_config.TARGET_REF_TEST_FORMAT_COL_NEW_CORPUS+"."+str(l_inc), target_language, current_config.STOP_WORD+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Numeric
    ##########################################################################
    if current_config.numeric:
      feature_name = "Numeric"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_numeric( current_config.TARGET_REF_TEST_FORMAT_COL_NEW_CORPUS+"."+str(l_inc), current_config.NUMERIC+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Proper Name
    ##########################################################################
    if current_config.proper_name:
      feature_name = "Proper Name"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_proper_name_threads( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_NEW_CORPUS+"."+str(l_inc), target_language, current_config.PROPER_NAME+extension+"."+str(l_inc), current_config)
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Unknown Lemma
    ##########################################################################
    if current_config.unknown_lemma:
      feature_name = "Unknown Lemma"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_unknown_lemma( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_NEW_CORPUS+"."+str(l_inc), current_config.UNKNOWN_LEMMA+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Number Of Occurrences word
    ##########################################################################
    if current_config.occurence_words:
      feature_name = "Number Of Occurrences word"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_number_of_occurrences_word( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_NEW_CORPUS+"."+str(l_inc),  current_config.NUMBER_OF_OCCURRENCES_WORD+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Number Of Occurrences stem (frequency of stemmed word)
    ##########################################################################
    if current_config.occurence_stems:
      feature_name = "Number Of Occurrences stemmed word"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_number_of_occurrences_stem( current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_NEW_CORPUS+"."+str(l_inc),  current_config.NUMBER_OF_OCCURRENCES_STEM+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Occur in Google Translatator
    ##########################################################################
    if current_config.google_translator:
      feature_name = "Occur in Google Translatator"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL_NEW_CORPUS+"."+str(l_inc), current_config.GOOGLE_TRANSLATE_CORPUS_NEW_CORPUS+"."+str(l_inc), current_config.OCCUR_IN_GOOGLE_TRANSLATE+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Occur in Bing Translatator
    ##########################################################################
    if current_config.bing_translator:
      feature_name = "Occur in Bing Translatator"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_occur_in_translators( current_config.TARGET_REF_TEST_FORMAT_COL_NEW_CORPUS+"."+str(l_inc), current_config.BING_TRANSLATE_CORPUS_NEW_CORPUS+"."+str(l_inc), current_config.OCCUR_IN_BING_TRANSLATE+extension+"."+str(l_inc))
      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Longest Target gram length
    ##########################################################################
    if current_config.longest_ngram_length_tgt:
      feature_name = "Longest Target gram length"
      print_time(feature_name, log_path)

      get_probability_from_language_model_threads( current_config.TARGET_REF_TEST_FORMAT_ROW_NEW_CORPUS, current_config.LANGUAGE_MODEL_TGT, 5, current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS_NEW_CORPUS, current_config, config_end_user)

      create_longest_target_gram_length_threads( current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS_NEW_CORPUS, current_config.LONGEST_TARGET_GRAM_LENGTH+extension, current_config)

      print_result(feature_name, log_path)


    ##########################################################################
    ## Feature: Longest Source gram length
    ##########################################################################
    if current_config.longest_ngram_length_src:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "Longest Source gram length"
          print_time(feature_name, log_path)

          #Buoc 1: File Source-ngram giong nhu cach lam Target-ngram
          get_temp_longest_source_gram_length_not_aligned_target_threads( current_config.SRC_REF_TEST_FORMAT_ROW_NEW_CORPUS, current_config.LANGUAGE_MODEL_SRC, current_config.N_GRAM, current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET, current_config, config_end_user)

          #convert format column to format row
          for l_inc in range(1,current_config.THREADS+1):
            convert_format_column_to_format_row( current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET+"."+str(l_inc), current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW+"."+str(l_inc))

          l_threads = []
          for l_inc in range(1,current_config.THREADS+1):
            ts = threading.Thread(target=feature_longest_gram_source_length_threads , args=(current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT_NEW_CORPUS+"."+str(l_inc), current_config.TEMP_LONGEST_SOURCE_GRAM_LENGTH_NOT_ALIGNED_TARGET_ROW+"."+str(l_inc), current_config.TYPE_LONGEST_SOURCE_GRAM_LENGTH_ALL, current_config.LONGEST_SOURCE_GRAM_LENGTH_ALIGNED_TARGET+extension+"."+str(l_inc), current_config, config_end_user))

            l_threads.append(ts)
            ts.start()

          for myT in l_threads:
            myT.join()

          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Backoff Behaviour
    ##########################################################################
    if current_config.backoff:
      feature_name = "Backoff Behaviour"
      print_time(feature_name, log_path)
      for l_inc in range(1,current_config.THREADS+1):
        feature_backoff_behaviour( current_config.LONGEST_TARGET_GRAM_LENGTH+extension+"."+str(l_inc), current_config.BACKOFF_BEHAVIOUR+extension+"."+str(l_inc))

      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Alignment Features = 6 * 3 = 18 features
    ## Target; Right_Target; Left_Target; Source; Right_Source; Left_Source
    ## Word; POS; Stemming
    ##########################################################################
    if current_config.alignments:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "Alignment Features"
          print_time(feature_name, log_path)
          for l_inc in range(1,current_config.THREADS+1):
            get_alignment_features_threads( current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT_NEW_CORPUS+"."+str(l_inc), current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW_NEW_CORPUS+"."+str(l_inc), current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW_NEW_CORPUS+"."+str(l_inc), current_config.ALIGNMENT_FEATURES+extension+"."+str(l_inc), config_end_user)

          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature:  WPP Exact
    ##########################################################################
    if current_config.wpp:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "WPP Exact"
          print_time(feature_name, log_path)

          for l_inc in range(1,current_config.THREADS+1):
            file_output_path_temp = current_config.WPP_EXACT+extension+"."+str(l_inc)
            # Delete extracted files (because they used mode "append")
            message="WARNING: " + file_output_path_temp + " already exists and will be deleted!\n"
            delete_already_existed_file(file_output_path_temp, message)
          #end for

          l_threads = []
          for l_inc in range(1,current_config.THREADS+1):
            ts = threading.Thread(target=feature_wpp_exact_threads , args=(current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT_NEW_CORPUS+"."+str(l_inc), current_config.WPP_EXACT+extension+"."+str(l_inc), l_inc , current_config))
            l_threads.append(ts)
            ts.start()

          for myT in l_threads:
            myT.join()

          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Constituent Label & Distance to Root
    ##########################################################################
    if current_config.distance_to_root:
      feature_name = "Constituent Label & Distance to Root using NLTK 3.0 within supporting python3"
      print_time(feature_name, log_path)

      feature_constituent_label_get_list_distance_to_root_null_link_threads(
        current_config.TARGET_REF_TEST_FORMAT_ROW_NEW_CORPUS,
        target_language,
        current_config.CONSTITUENT_TREE_TEMP,
        current_config.DISTANCE_TO_ROOT+extension,
        current_config.CONSTITUENT_LABEL+extension,
        current_config,
        config_end_user)

      print_result(feature_name, log_path)


    ##########################################################################
    ## Feature: Polysemy Count - Target (Support English, French and Spanish)
    ##########################################################################
    if current_config.polysemy_count_target:
      feature_name = "Polysemy Count - Target"
      print_time(feature_name, log_path)

      file_input_path = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_NEW_CORPUS
      file_output_path = current_config.BABEL_NET_OUTPUT_CORPUS_TGT_LAST + extension

      l_threads = []
      for l_inc in range(1,current_config.THREADS+1):
        ts = threading.Thread(target=get_polysemy_count_within_given_target_language_threads , args=(current_config, config_end_user, target_language, file_input_path+"."+str(l_inc), file_output_path+"."+str(l_inc), l_inc))

        l_threads.append(ts)
        ts.start()
        time.sleep(1)

      for myT in l_threads:
        myT.join()

      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Polysemy Count - Target using DBnary (Support English, French and Spanish)
    ##########################################################################
    if current_config.polysemy_count_target_dbnary:
      feature_name = "Polysemy Count - Target using DBnary"
      print_time(feature_name, log_path)

      file_input_path = current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL_NEW_CORPUS
      file_output_path = current_config.DBNARY_OUTPUT_CORPUS_TGT_LAST + extension

      l_threads = []
      for l_inc in range(1,current_config.THREADS+1):
        ts = threading.Thread(target=get_polysemy_count_within_given_target_language_with_dbnary_threads , args=(current_config, config_end_user, target_language, file_input_path+"."+str(l_inc), file_output_path+"."+str(l_inc), l_inc))

        l_threads.append(ts)
        ts.start()
        time.sleep(1)


      for myT in l_threads:
        myT.join()

      print_result(feature_name, log_path)

    ##########################################################################
    ## Feature:  WPP any, Max, Min, Nodes
    ##########################################################################
    if current_config.wpp_any:
      if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == config_end_user.NUM_IS_HAS_A_FILE_INCLUDED_ALIGNMENT:
          feature_name = "WPP any, Max, Min, Nodes"
          print_time(feature_name, log_path)

          feature_wpp_nodes_min_max_threads(
            current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT_NEW_CORPUS,
            current_config.TOOL_N_BEST_TO_LATTICE_THREADS,
            current_config.WPP_NODES_MIN_MAX_TEMP,
            current_config.WPP_NODES_MIN_MAX + extension,
            current_config,
            config_end_user)

          print_result(feature_name, log_path)

    ##########################################################################
    ## Feature: Label - Word (Using Terpa)
    ##########################################################################
    # if current_config.label:
    #   feature_name = "Label - Word (Given Label)"
    #   print_time(feature_name, log_path)

    #   l_threads = []
    #   for l_inc in range(1,current_config.THREADS+1):
    #     ts = threading.Thread(target=extracting_label_for_word_format_column_threads , args=(current_config.TARGET_REF_TEST_FORMAT_ROW+"."+str(l_inc), current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING+"."+str(l_inc), current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT+"."+str(l_inc), l_inc, current_config, config_end_user))

    #     l_threads.append(ts)
    #     time.sleep(1)
    #     ts.start()
    #   for myT in l_threads:
    #     myT.join()


    ##########################################################################
    feature_name = "END Task - Extracting Features"
    print_time(feature_name, log_path)



#*****************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()

    config_end_user = load_config_end_user()

    log_path = current_config.RESULT_MESSAGE_OUTPUT

    if current_config.THREADS > 1:
      extracting_all_features_threads(log_path)
    else:
      extracting_all_features(log_path)

    #extracting_all_features_threads(log_path)
    #extracting_all_features_test(log_path)

    print ('OK')
