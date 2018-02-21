# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 2018
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
+ Arguments: path-of-input-data-have-no-post-edited-corpus, path-of-trained-model, decision-threshold, path-of-labelled-output-data-format-column

Ex:
path-of-input-data-have-no-post-edited-corpus =
path-of-trained-model=WCE-LIG/wce_system/var/data/CRF_model_with_template1_System_WCE.txt
decision-threshold=0.5 (If confidence score >= decision-threshold then labelling GOOD, otherwise BAD)
path-of-labelled-output-data-format-column

# --------------------------------------------------------------------------
For example - Shell-script for Labelling Phase:

Demo: System_WCE - Labelling Phase

WCE-LIG///tools/wapiti-1.5.0/./wapiti label -c -s -p WCE-LIG/wce_system/var/data/CRF_tgt.column.test_file_System_WCE.txt -m WCE-LIG/wce_system/var/data/CRF_model_with_template1_System_WCE.txt WCE-LIG/wce_system/var/data/CRF_model_result_testing1_System_WCE.txt 2>&1 | tee WCE-LIG/wce_system/var/data/CRF_model_testing_log_file1_System_WCE.txt


# --------------------------------------------------------------------------
# General Shell-script for Labelling Phase:

WCE-LIG///tools/wapiti-1.5.0/./wapiti label -c -s -p path_to_test_file_System_WCE_using_format_column -m path_to_CRF_model_with_template_System_WCE path_to_CRF_model_result_testing_System_WCE.txt 2>&1 | tee path_to_testing_log_file_System_WCE

# See more detail of the parameters (-c, -s, -p, -m, etc): https://wapiti.limsi.fr/manual.html
# --------------------------------------------------------------------------
"""

import argparse
import os
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

from common_module.cm_config import load_configuration, load_config_end_user, get_absolute_path_current_module
from common_module.cm_util import  is_numeric, is_in_list, is_in_string, print_time, print_result, split_string_to_list_delimeter_tab, get_str_value_given_key, is_match, split_string_to_list_delimeter_comma, print_introduction
from preprocessing.pre_processing import preprocessing_new_corpus_threads
from feature.extract_all_features import extracting_all_features_new_corpus_threads
from metrics.demo_metrics import label_new_corpus_using_trained_model

#*****************************************************************************#
def get_labels_with_given_CRF_model(raw_corpus_source_language_new_corpus_path, raw_corpus_target_language_new_corpus_path, file_output_google_translator, file_output_bing_translator, file_output_1_bestlist_included_alignment, file_output_N_bestlist_included_alignment, model_path, file_wce_output,
    log_path):
    """
    Note that: In this case, we have no post-edited input-data. However, we have CRF model that is trained.

    Expected Result:

0   0   0   0   0   1   1   1   1   NNS 8   2   1   F   2   2   2   2   surgeons    NNS surgeon in  IN  in  _X-1    _X-1    _X-1    chirurgiens NOM chirurgien  de  PRP de  les DET le          G   G/0.999998
0   1   0   0   0   1   1   0   0   IN  8   -1  1   E   2   2   2   2   in  IN  in  los NP  los surgeons    NNS surgeon de  PRP de  los NOM los chirurgiens NOM chirurgien          B   B/0.949764
...
0   1   0   0   0   1   1   1   1   JJ  4   -1  1   D   1   1   1   1   mr  NN  Mr  camus   NN  <unknown>   said    VVD say m.  VER <unknown>   camus   ADJ camus   déclaré VER déclarer            G   G/1.000000
0   0   0   1   1   1   1   1   1   NN  4   -1  1   D   1   1   1   1   camus   NN  <unknown>   .   SENT    .   mr  NN  Mr  camus   ADJ camus   .   SENT    .   m.  VER <unknown>           G   G/1.000000
1   0   0   0   0   1   1   1   1   .   2   -1  1   D   2   2   2   2   .   SENT    .   _X+1    _X+1    _X+1    camus   NN  <unknown>   .   SENT    .   _X+1    _X+1    _X+1    camus   ADJ camus           G   G/1.000000


    --> It means that:
    1st target word "surgeons" is labelled by "G" and having confidence-score = 0.999998 ==> ~99.99% become G-label

    2nd target word "in" is labelled by "B" and having confidence-score = 1-0.949764 = 0.050236 ==> ~5.02% become G-label

    Note that, there is an empty line among two sentences in this format "column"

    """

    #introduction of this solution
    print_introduction(log_path)

    feature_name = "BEGIN - Task Labelling for New Corpus"
    print_time(feature_name, log_path)

    ##########################################################################

    # pre-processing
    preprocessing_new_corpus_threads(raw_corpus_source_language_new_corpus_path, raw_corpus_target_language_new_corpus_path, file_output_google_translator, file_output_bing_translator, file_output_1_bestlist_included_alignment, file_output_N_bestlist_included_alignment, log_path, config_end_user, current_config)

    # extracting all features
    extension = "_new_corpus"
    extracting_all_features_new_corpus_threads(log_path, config_end_user, current_config, extension)

    # Labelling
    extension = "_new_corpus"
    label_new_corpus_using_trained_model(model_path, log_path, file_wce_output, config_end_user, current_config,  extension)

    ##########################################################################

    feature_name = "END - Task Labelling for New Corpus"
    print_time(feature_name, log_path)
#*****************************************************************************#
if __name__ == "__main__":
    #Test case:
    config_end_user = load_config_end_user()
    current_config = load_configuration()

    parser = argparse.ArgumentParser()

    # files
    parser.add_argument('--raw-src', '-rs', required=True,
                        help='Raw Corpus - Source Language')

    parser.add_argument('--raw-tgt', '-rt', required=True,
                        help='Raw Corpus - Target Language')

    parser.add_argument('--google-output', '-go', required=True,
                        help='Google Translator output')

    parser.add_argument('--bing-output', '-bo', required=True,
                        help='Bing Translator output')

    parser.add_argument('--one-best-list', '-ob', required=True,
                        help='MT output 1-best-list')

    parser.add_argument('--n-best-list', '-nb', required=True,
                        help='MT output N-best-list')

    parser.add_argument('--model', '-m', required=True,
                        help='given CRF model')

    parser.add_argument('--wce-output', '-out', required=True,
                        help='WCE Output after labelling')


    args = parser.parse_args()

    raw_corpus_source_language_new_corpus_path = args.raw_src # src-ref-all.fr
    raw_corpus_target_language_new_corpus_path = args.raw_tgt # tgt-mt-all.en
    file_output_google_translator = args.google_output # output_Google_Translator.en
    file_output_bing_translator = args.bing_output # output_Bing_Translator.en
    file_output_1_bestlist_included_alignment = args.one_best_list # src-ref-all.fr.translated_output
    file_output_N_bestlist_included_alignment = args.n_best_list # src-ref-all.fr.translated_1000_output
    model_path = args.model
    file_wce_output = args.wce_output
    log_path = current_config.SOLUTION_MESSAGE_OUTPUT

    get_labels_with_given_CRF_model(raw_corpus_source_language_new_corpus_path, raw_corpus_target_language_new_corpus_path, file_output_google_translator, file_output_bing_translator, file_output_1_bestlist_included_alignment, file_output_N_bestlist_included_alignment, model_path, file_wce_output, log_path)

    print ('OK')
