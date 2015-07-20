# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 13:44:43 2015
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
import random

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server


from common_module.cm_config import load_configuration
from common_module.cm_file import is_existed_file, get_file_oracle_label_given_all_features_file, get_result_testing_CRF_models_within_given_list_of_models
from common_module.cm_util import get_number_of_words_with_label_good_and_bad_in_list_label, get_precision_recall_fscore_within_list
#**************************************************************************#


#**************************************************************************#
def get_list_of_oracle_label(file_input_path):
    """
    Getting list of words' labels after extracting label.

    :type file_input_path: string
    :param file_input_path: contains corpus with format each "word" in each line; there is a empty line among the sentences.

    :rtype: list of oracle label

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus that is result of extracting word-label.')

    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    result = []

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            continue
        #end if

        result.append(line)
    #end for

    #close file
    file_reader.close()

    return result
#**************************************************************************#
#Demo baseline: always predicts "Good" & "Bad"
#muc dich: de biet duoc length cua danh sach Oracle Label
## zip('ABCD', 'xy') --> Ax By
"""Note: python 2 --> ham izip
>>> x = [1, 2, 3]
>>> y = [4, 5, 6]
>>> zipped = zip(x, y)
>>> list(zipped)
[(1, 4), (2, 5), (3, 6)]
"""
def get_list_of_word_label_ALL(list_of_oracle_label, label_all_word):
    """
    Getting list of words' labels that has the same length and ALL labels are Good/Bad

    :type list_of_oracle_label: string
    :param list_of_oracle_label: contains list of word label (oracle label)

    :type label_all_word: string
    :param label_all_word: "G"/"B"

    :rtype: list of all label is Good or Bad

    :raise ValueError: if len(list_of_oracle_label) = 0
    """
    n = len(list_of_oracle_label)
    result = []
    range_length = range(n)

    for item in range_length:
        result.append(label_all_word)
    #end for

    return result
#**************************************************************************#
#tao mang gom cac nhan ngau nhien
def get_list_of_word_label_random(list_of_oracle_label):
    """
    Getting list of words' labels that is the result after randomizing from classifier.

    :type list_of_oracle_label: string
    :param list_of_oracle_label: contains list of word label (oracle label)

    :type label_all_word: string
    :param label_all_word: random "G"/"B"

    :rtype: list of all label is Good or Bad

    :raise ValueError: if len(list_of_oracle_label) = 0
    """
    n = len(list_of_oracle_label)
    result = []
    range_length = range(n)

    #ref: https://docs.python.org/3.4/library/random.html
    for item in range_length:
        label_random = random.choice('GB')

        result.append(label_random)
    #end for

    return result
#**************************************************************************#
#Baseline 3: random classifier Good/Bad
#**************************************************************************#
#Baseline 1: All of word-label is GOOD
#Baseline 2: all of word-label is BAD
#Baseline 3: random classifier Good/Bad
def get_baseline(file_oracle_label_path, file_output_path):
    """
    * Baseline 1: All of word-label is GOOD.

    * Baseline 2: All of word-label is BAD.

    * Baseline 3: Random classifier Good/Bad.

    :type file_oracle_label_path: string
    :param file_oracle_label_path: contains corpus oracle label with format each "label" in each line; there is a empty line among the sentences.

    :type file_output_path: string
    :param file_output_path: result of 3 baselines.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_oracle_label_path):
        raise TypeError('Not Existed file that contains corpus oracle label with format each "label" in each line; there is a empty line among the sentences.')
    """
    str_message_if_not_existed = "Not Existed file that contains corpus oracle label with format each label in each line; there is a empty line among the sentences"
    is_existed_file(file_oracle_label_path, str_message_if_not_existed)

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'a', encoding = 'utf-8')#old version: type=w

    #get_list_of_oracle_label(file_input_path)
    #LABEL_OUTPUT
    #list_of_oracle_label = get_list_of_oracle_label(current_config.LABEL_OUTPUT)
    list_of_oracle_label = get_list_of_oracle_label(file_oracle_label_path)

    # Get list that contains the same word label.
    current_config = load_configuration()
    #label_good = "G"
    #label_bad = "B"
    label_good = current_config.LABEL_GOOD
    label_bad = current_config.LABEL_BAD

    list_of_all_label_good = get_list_of_word_label_ALL(list_of_oracle_label, label_good)
    list_of_all_label_bad = get_list_of_word_label_ALL(list_of_oracle_label, label_bad)
    list_of_random_label = get_list_of_word_label_random(list_of_oracle_label)

    #oracle label
    Z_good, Z_bad = get_number_of_words_with_label_good_and_bad_in_list_label(list_of_oracle_label)

    line_separate = "-"*63

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################
    #Thong ke phan tram cua oracle label
    str_statistics = "*** Statistics of Oracle label:"
    print(str_statistics)
    file_writer.write(str_statistics)
    file_writer.write("\n")

    str_B_G_oracle = "Bad Oracle = %d \t Good Oracle = %d " %(Z_bad, Z_good)
    print(str_B_G_oracle)
    file_writer.write(str_B_G_oracle)
    file_writer.write("\n")

    Z_sum = Z_bad + Z_good
    per_b_oracle = Z_bad / Z_sum
    per_g_oracle = Z_good / Z_sum

    str_per_oracle = "Bad = %.4f \nGood = %.4f" %(per_b_oracle, per_g_oracle)
    print(str_per_oracle)
    file_writer.write(str_per_oracle)
    file_writer.write("\n")

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    #* Baseline 1: All of word-label is GOOD.
    X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good = get_precision_recall_fscore_within_list(list_of_oracle_label, list_of_all_label_good)

    str_baseline = "*** Baseline 1 - all of words predict \"Good\":"
    print(str_baseline)
    file_writer.write(str_baseline)
    file_writer.write("\n")

    #B - in Baseline 1
    str_B_baseline = "X-Bad = %d \t Y-Bad = %d \t Z-Bad = %d" %(X_bad, Y_bad, Z_bad)
    print(str_B_baseline)
    file_writer.write(str_B_baseline)
    file_writer.write("\n")

    #G - in Baseline 1
    str_G_baseline = "X-Good = %d \t Y-Good = %d \t Z-Good = %d" %(X_good, Y_good, Z_good)
    print(str_G_baseline)
    file_writer.write(str_G_baseline)
    file_writer.write("\n")

    ##########################
    #B - in Baseline 1
    str_result = "B \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_bad, Rc_bad, F_bad)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #G - in Baseline 1
    str_result = "G \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_good, Rc_good, F_good)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    #* Baseline 2: All of word-label is BAD.
    X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good = get_precision_recall_fscore_within_list(list_of_oracle_label, list_of_all_label_bad)

    str_baseline = "*** Baseline 2 - all of words predict \"Bad\":"
    print(str_baseline)
    file_writer.write(str_baseline)
    file_writer.write("\n")

    #B - in Baseline 2
    str_B_baseline = "X-Bad = %d \t Y-Bad = %d \t Z-Bad = %d" %(X_bad, Y_bad, Z_bad)
    print(str_B_baseline)
    file_writer.write(str_B_baseline)
    file_writer.write("\n")

    #G - in Baseline 2
    str_G_baseline = "X-Good = %d \t Y-Good = %d \t Z-Good = %d" %(X_good, Y_good, Z_good)
    print(str_G_baseline)
    file_writer.write(str_G_baseline)
    file_writer.write("\n")

    ##########################
    #B - in Baseline 2
    str_result = "B \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_bad, Rc_bad, F_bad)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #G - in Baseline 2
    str_result = "G \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_good, Rc_good, F_good)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    #* Baseline 3: Random classifier Good/Bad.
    X_bad, Y_bad, Z_bad, Pr_bad, Rc_bad, F_bad, X_good, Y_good, Z_good, Pr_good, Rc_good, F_good = get_precision_recall_fscore_within_list(list_of_oracle_label, list_of_random_label)

    str_baseline = "*** Baseline 3 - Random classifier Good/Bad:"
    print(str_baseline)
    file_writer.write(str_baseline)
    file_writer.write("\n")

    #B - in Baseline 3
    str_B_baseline = "X-Bad = %d \t Y-Bad = %d \t Z-Bad = %d" %(X_bad, Y_bad, Z_bad)
    print(str_B_baseline)
    file_writer.write(str_B_baseline)
    file_writer.write("\n")

    #G - in Baseline 3
    str_G_baseline = "X-Good = %d \t Y-Good = %d \t Z-Good = %d" %(X_good, Y_good, Z_good)
    print(str_G_baseline)
    file_writer.write(str_G_baseline)
    file_writer.write("\n")

    ##########################
    #B - in Baseline 3
    str_result = "B \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_bad, Rc_bad, F_bad)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #G - in Baseline 3
    str_result = "G \t Pr=%.4f \t Rc=%.4f \t F1=%.4f \t" %(Pr_good, Rc_good, F_good)
    print(str_result)
    file_writer.write(str_result)
    file_writer.write("\n")

    #######################################################################
    print(line_separate)
    print(line_separate)
    file_writer.write(line_separate)
    file_writer.write("\n")
    file_writer.write(line_separate)
    file_writer.write("\n")
    #######################################################################

    #close file
    file_writer.close()
#**************************************************************************#
#wmt14_test #test_file_path = current_config.FEATURES_TEST_WMT14
#wmt13_test #test_file_path = current_config.FEATURES_TEST_WMT13
#list_of_best_models = [41,42,43]
def demo_baselines_and_systems_within_given_model_wmt15( demo_name, test_file_path, list_of_best_models, extension = ""):
    """
    Demo all baselines and System 1

    :type result_output_path: string
    :param result_output_path: path of log-file that contains results of DEMO
    """
    current_config = load_configuration()


    #wmt14_test
    #test_file_path = current_config.FEATURES_TEST_WMT14

    #wmt13_test
    #test_file_path = current_config.FEATURES_TEST_WMT13
    file_input_path = test_file_path
    file_output_path = current_config.LABEL_OUTPUT_FROM_EXTRACTED_FEATURES

    get_file_oracle_label_given_all_features_file(file_input_path, file_output_path)

    #file_result_path = current_config.BASELINE_WMT14_WMT13
    file_result_path = current_config.BASELINE_TEST_MODEL_CRF
    get_baseline(file_output_path, file_result_path)

    #Tich hop wapiti va lay output
    #list_of_best_models = [41,42,43]#[8,12,18,20]
    #demo_name = "System_1"
    for order_of_template in list_of_best_models:
        get_result_testing_CRF_models_within_given_list_of_models(demo_name, order_of_template, test_file_path, extension)
    #end for
#**************************************************************************#
if __name__ == "__main__":
    #Test case:

    current_config = load_configuration()



    get_baseline(current_config.LABEL_OUTPUT, current_config.F_MEASURE_RESULT_BASELINE)

    print ('OK')

