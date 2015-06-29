# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 14:48:42 2015
"""

# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole Toolkit (eval_agent Toolkit)
# Homepage: http://getalp.imag.fr
#
# Authors: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com

import os
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from common_module.cm_config import load_configuration, load_config_end_user, get_absolute_path_current_module
from common_module.cm_util import  is_numeric, is_in_list, is_in_string, print_time, print_result, split_string_to_list_delimeter_tab, get_str_value_given_key, is_match, split_string_to_list_delimeter_comma, print_introduction
from preprocessing.pre_processing import preprocessing_corpus,preprocessing_corpus_threads
from feature.extract_all_features import extracting_all_features,extracting_all_features_threads
from metrics.demo_metrics import demo_baselines_and_systems

#*****************************************************************************#
def demo_solution(result_output_path):
    """
    Extracting all features

    :type result_output_path: string
    :param result_output_path: path of log-file that contains results of DEMO
    """

    #introduction of this solution
    print_introduction(result_output_path)

    feature_name = "BEGIN - DEMO OUR SOLUTION"
    print_time(feature_name, result_output_path)

    ##########################################################################

    #pre-processing
#    preprocessing_corpus(result_output_path)

    #extracting all features
#    extracting_all_features(result_output_path)

    #demo metrics
    demo_baselines_and_systems(result_output_path)

    ##########################################################################

    feature_name = "END - DEMO OUR SOLUTION"
    print_time(feature_name, result_output_path)
#*****************************************************************************#
def demo_solution_threads(result_output_path):
    """
    Extracting all features

    :type result_output_path: string
    :param result_output_path: path of log-file that contains results of DEMO
    """

    #introduction of this solution
    print_introduction(result_output_path)

    feature_name = "BEGIN - DEMO OUR SOLUTION"
    print_time(feature_name, result_output_path)

    ##########################################################################

    #pre-processing
    preprocessing_corpus_threads(result_output_path)

    #extracting all features
    extracting_all_features_threads(result_output_path)

    #demo metrics
    demo_baselines_and_systems(result_output_path)

    ##########################################################################

    feature_name = "END - DEMO OUR SOLUTION"
    print_time(feature_name, result_output_path)
#*****************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()

    if current_config.THREADS > 1:
      demo_solution_threads(current_config.SOLUTION_MESSAGE_OUTPUT)
    else:
      demo_solution(current_config.SOLUTION_MESSAGE_OUTPUT)
    

    print ('OK')
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#

