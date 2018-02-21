# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 2018
"""

# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues
# et de la Parole
# Homepage: http://getalp.imag.fr
#
# Authors: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com

"""
Task:
+ Get Model CRF after training with given input data.
+ Arguments: path-of-out-model

# --------------------------------------------------------------------------
Demo: System_WCE - Training with template 1
Template path: /home/lent/Develops/Solution/WCE-LIG///wce_system/lib/templates/template.en1

For example - Shell-script for Training Phase:

/home/lent/Develops/Solution/WCE-LIG///tools/wapiti-1.5.0/./wapiti train -a sgd-l1 -i 200 -e 0.00005 -w 6 -p /home/lent/Develops/Solution/WCE-LIG///wce_system/lib/templates/template.en1 /home/lent/Develops/Solution/WCE-LIG///wce_system/var/data/CRF_tgt.column.train_file_System_WCE.txt /home/lent/Develops/Solution/WCE-LIG///wce_system/var/data/CRF_model_with_template1_System_WCE.txt --nthread 3 2>&1 | tee /home/lent/Develops/Solution/WCE-LIG///wce_system/var/data/CRF_model_training_log_file1_System_WCE.txt

# --------------------------------------------------------------------------
# General Shell-script for Training Phase:

/home/lent/Develops/Solution/WCE-LIG///tools/wapiti-1.5.0/./wapiti train -a sgd-l1 -i 200 -e 0.00005 -w 6 -p path_to_template_CRF_file path_to_train_file_System_WCE_using_format_column path_to_CRF_model_with_template_System_WCE --nthread 3 2>&1 | tee path_to_training_log_file_System_WCE.txt

# See more detail of the parameters (-a, -e, -w, -p, etc): https://wapiti.limsi.fr/manual.html
# --------------------------------------------------------------------------

"""

import os
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from common_module.cm_config import load_configuration, load_config_end_user, get_absolute_path_current_module
from common_module.cm_util import  is_numeric, is_in_list, is_in_string, print_time, print_result, split_string_to_list_delimeter_tab, get_str_value_given_key, is_match, split_string_to_list_delimeter_comma, print_introduction
from preprocessing.pre_processing import preprocessing_corpus,preprocessing_corpus_threads
from feature.extract_all_features import extracting_all_features,extracting_all_features_threads
from metrics.demo_metrics import generate_model_CRF_threads

#*****************************************************************************#
def get_model_CRF_threads(result_output_path, config_end_user, current_config):
    """
    Extracting all features

    :type result_output_path: string
    :param result_output_path: path of log-file that contains results of DEMO
    """

    #introduction of this solution
    print_introduction(result_output_path)

    feature_name = "BEGIN - GET TRAINING MODEL"
    print_time(feature_name, result_output_path)

    ##########################################################################

    #pre-processing
    # preprocessing_corpus_threads(result_output_path)

    #extracting all features
    # extracting_all_features_threads(result_output_path)

    #generating CRF model
    model_path = generate_model_CRF_threads(result_output_path, config_end_user, current_config)

    ##########################################################################

    feature_name = "END - GET TRAINING MODEL"
    print_time(feature_name, result_output_path)

    return model_path
#*****************************************************************************#
if __name__ == "__main__":
    #Test case:
    config_end_user = load_config_end_user()
    current_config = load_configuration()

    model_path = "Empty_path"

    if current_config.THREADS > 1:
        model_path = get_model_CRF_threads(current_config.SOLUTION_MESSAGE_OUTPUT, config_end_user, current_config)
    else:
        pass

    # end if

    print("Path of CRF model after training: " + model_path)

    # /home/lent/Develops/Solution/WCE-LIG/wce_system/var/data/CRF_model_with_template1_System_WCE.txt

    print ('OK')

