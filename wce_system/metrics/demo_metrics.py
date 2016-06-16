# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 12:49:54 2015
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
from common_module.cm_file import is_existed_file, divide_merged_features_file_within_given_input_file, wce_system_after_dividing_corpus, get_file_oracle_label_given_all_features_file, get_list_of_file_paths_not_included_nbestlist_and_asr_within_our_labels, generating_merged_features_within_given_list_of_file_paths, get_list_of_file_paths_not_included_nbestlist_and_asr, get_list_of_file_paths_for_ape_2015, get_list_of_file_paths_included_nbestlist_not_asr, merge_files_threads
from common_module.cm_util import  print_time, print_result
from metrics.baseline import get_baseline
#**************************************************************************#
#Baselines
#**************************************************************************#
#System 1
#template 1: all features (38 features)

#template 2: The 'same' list of features with Quang's
#(24 features, diff template, not included NULL Link).
#Note: Template 2 does not contain feature "Occur in Bing Translator"

#template 3: same template 1, remove 2 features: Occur in Google Translator ; Occur in Bing Translator

#template 4: same template 2, remove features: Occur in Google Translator -> remaining 23 features
#**************************************************************************#
def demo_baselines_and_systems(log_output_path):
    #log_output_path = current_config.CRF_MESSAGE_OUTPUT
    #log_output_path = file_log_path
    current_config = load_configuration()
    config_end_user = load_config_end_user()
    

    #introduction of this solution
    #print_introduction(log_output_path)

    feature_name = "BEGIN Task - Demo Baselines & System CRF"
    print_time(feature_name, log_output_path)

    #B1: "paste" all of output from extracting phase --> one file
    #generating_merged_features()
    #ref trong module cm_file
    #list_of_file_paths = get_list_of_file_paths_not_included_nbestlist_and_asr_within_our_labels() #within our labels
    """For WCE 2015"""
    """
    list_of_file_paths = get_list_of_file_paths_not_included_nbestlist_and_asr() #within given labels
    file_output_path = current_config.OUTPUT_MERGED_FEATURES_WMT15
    generating_merged_features_within_given_list_of_file_paths(list_of_file_paths, file_output_path)
    """

    """For APE 2015"""
    #list_of_file_paths = get_list_of_file_paths_for_ape_2015() #within given labels

    #for WCE
    list_of_file_paths = get_list_of_file_paths_included_nbestlist_not_asr()

    print("list_of_file_paths-BEGIN")
    print(list_of_file_paths)
    print("list_of_file_paths-END")

    file_output_path = current_config.OUTPUT_MERGED_FEATURES
    generating_merged_features_within_given_list_of_file_paths(list_of_file_paths, file_output_path)

    #raise Exception("Just for testing...")

    #number of sentences for training, developing and testing
    number_of_sentences_all = int(config_end_user.RAW_CORPUS_TRAINING_SIZE) + int(config_end_user.RAW_CORPUS_TEST_SIZE)
    number_of_sentences_in_file_for_training = int(config_end_user.RAW_CORPUS_TRAINING_SIZE)
    number_of_sentences_in_file_for_developing = 0
    #number_of_sentences_in_file_for_testing = number_of_sentences_all - number_of_sentences_in_file_for_training - number_of_sentences_in_file_for_developing
    number_of_sentences_in_file_for_testing = config_end_user.RAW_CORPUS_TEST_SIZE


    file_input_path = current_config.OUTPUT_MERGED_FEATURES

    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    corpus_type = current_config.SEQUENTIAL_CORPUS
    demo_name = "System_WCE"
    divide_merged_features_file_within_given_input_file(demo_name, file_input_path, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    """
    training_corpus_path = current_config.TRAIN_FILE_PATH + "_" + demo_name + ".txt"
    developing_corpus_path = current_config.DEV_FILE_PATH + "_" + demo_name + ".txt"
    testing_corpus_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"
    """

    #B3: Tinh baseline doi voi phan test
    ##########################################################################
    ## Demo: Baseline 1, 2 and 3
    ##########################################################################
    feature_name = "Baseline-Systems 1, 2 and 3"
    print_time(feature_name, log_output_path)

    #demo_baseline(current_config.LABEL_OUTPUT, current_config.F_MEASURE_RESULT_BASELINE)
    #demo_baseline(current_config.LABEL_OUTPUT, log_output_path)
    file_input_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"
    file_output_path = current_config.LABEL_OUTPUT_FROM_EXTRACTED_FEATURES

    get_file_oracle_label_given_all_features_file(file_input_path, file_output_path)

    file_result_path = current_config.BASELINE_WMT15
    get_baseline(file_output_path, file_result_path)

    print_result(feature_name, log_output_path)

    #B4: System1 doi voi phan test, co nghia la: Train va Dev; Roi Testing voi Splitted_Test_Corpus
    number_of_template = 6
    num_of_template_start = 0
    num_of_template_end = 6
    feature_name = "System WCE - Sequential Corpus - all="+ str(number_of_sentences_all) +" train="+  str(number_of_sentences_in_file_for_training) +"; dev=" + str(number_of_sentences_in_file_for_developing) + "; test=" + str(number_of_sentences_in_file_for_testing)
    print_time(feature_name, log_output_path)

    wce_system_after_dividing_corpus(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template, num_of_template_start, num_of_template_end)

    print_result(feature_name, log_output_path)

    ##########################################################################
    feature_name = "END Task - Demo Baselines & System CRF"
    print_time(feature_name, log_output_path)
#**************************************************************************#
      
      
  
def demo_baselines_and_systems_threads(log_output_path):
    """
    :type log_output_path: string
    :param log_output_path: path of log-file that contains results of DEMO
    """
    #log_output_path = current_config.CRF_MESSAGE_OUTPUT
    #log_output_path = file_log_path
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #introduction of this solution
    #print_introduction(log_output_path)

    feature_name = "BEGIN Task - Demo Baselines & System CRF"
    print_time(feature_name, log_output_path)

    #for WCE
    list_of_file_paths = get_list_of_file_paths_included_nbestlist_not_asr()

    print("list_of_file_paths-BEGIN")
    merge_files_threads(list_of_file_paths,current_config)
    print(list_of_file_paths)
    print("list_of_file_paths-END")
    

    file_output_path = current_config.OUTPUT_MERGED_FEATURES
    generating_merged_features_within_given_list_of_file_paths(list_of_file_paths, file_output_path)

    #raise Exception("Just for testing...")

    #B2: chuan bi du lieu de testing
    #number of sentences for training, developing and testing
    number_of_sentences_all = int(config_end_user.RAW_CORPUS_TRAINING_SIZE) + int(config_end_user.RAW_CORPUS_TEST_SIZE)
    number_of_sentences_in_file_for_training = int(config_end_user.RAW_CORPUS_TRAINING_SIZE)
    number_of_sentences_in_file_for_developing = 0
    #number_of_sentences_in_file_for_testing = number_of_sentences_all - number_of_sentences_in_file_for_training - number_of_sentences_in_file_for_developing
    number_of_sentences_in_file_for_testing = config_end_user.RAW_CORPUS_TEST_SIZE 

    file_input_path = current_config.OUTPUT_MERGED_FEATURES

    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    corpus_type = current_config.SEQUENTIAL_CORPUS
    demo_name = "System_WCE"
    divide_merged_features_file_within_given_input_file(demo_name, file_input_path, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    """
    training_corpus_path = current_config.TRAIN_FILE_PATH + "_" + demo_name + ".txt"
    developing_corpus_path = current_config.DEV_FILE_PATH + "_" + demo_name + ".txt"
    testing_corpus_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"
    """
    #return

    #B3: Tinh baseline doi voi phan test
    ##########################################################################
    ## Demo: Baseline 1, 2 and 3
    ##########################################################################
    feature_name = "Baseline-Systems 1, 2 and 3"
    print_time(feature_name, log_output_path)

    #demo_baseline(current_config.LABEL_OUTPUT, current_config.F_MEASURE_RESULT_BASELINE)
    #demo_baseline(current_config.LABEL_OUTPUT, log_output_path)
    file_input_path = current_config.TEST_FILE_PATH + "_" + demo_name + ".txt"
    file_output_path = current_config.LABEL_OUTPUT_FROM_EXTRACTED_FEATURES
    print("TEST "+file_input_path)
    print("TEST "+file_output_path)

    get_file_oracle_label_given_all_features_file(file_input_path, file_output_path)

    file_result_path = current_config.BASELINE_WMT15
    get_baseline(file_output_path, file_result_path)

    print_result(feature_name, log_output_path)

    #B4: System1 doi voi phan test, co nghia la: Train va Dev; Roi Testing voi Splitted_Test_Corpus
    number_of_template = 6
    num_of_template_start = 0
    num_of_template_end = 6
    feature_name = "System WCE - Sequential Corpus - all="+ str(number_of_sentences_all) +" train="+  str(number_of_sentences_in_file_for_training) +"; dev=" + str(number_of_sentences_in_file_for_developing) + "; test=" + str(number_of_sentences_in_file_for_testing)
    print_time(feature_name, log_output_path)

    wce_system_after_dividing_corpus(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template, num_of_template_start, num_of_template_end)

    print_result(feature_name, log_output_path)

    ##########################################################################
    feature_name = "END Task - Demo Baselines & System CRF"
    print_time(feature_name, log_output_path)
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()

    if current_config.THREADS > 1:
      demo_baselines_and_systems_threads(current_config.CRF_MESSAGE_OUTPUT)
    else:
      demo_baselines_and_systems(current_config.CRF_MESSAGE_OUTPUT)
    
    

    print ('OK')
