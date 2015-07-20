# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 17:17:00 2014
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

# **************************************************************************#
import os
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  #in order to test with line by line on the server

from preprocessing.alignment_giza import *
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import copy_file_from_path1_to_path2, lowercase_raw_corpus_not_tokenizer, get_output_treetagger_format_row, \
    get_file_alignments_target_to_source_word_alignment_using_moses, convert_format_row_to_format_column, tokenizer_raw_corpus
from common_module.cm_util import print_time, print_result, check_value_boolean

#**************************************************************************#

def copy_raw_files():
    """
    Copy files in config that is defined by user to corresponding paths
    """
    current_config = load_configuration()

    config_end_user = load_config_end_user()

    ###########################################################################
    #corpus: 3 files
    #print("from: %s" %config_end_user.RAW_CORPUS_SOURCE_LANGUAGE)
    #print("to: %s" %current_config.INPUT_RAW_CORPUS_SOURCE_LANGUAGE)

    #raw_corpus.src
    from_path = config_end_user.RAW_CORPUS_SOURCE_LANGUAGE
    to_path = current_config.INPUT_RAW_CORPUS_SOURCE_LANGUAGE
    copy_file_from_path1_to_path2(from_path, to_path)

    #raw_corpus.tgt
    from_path = config_end_user.RAW_CORPUS_TARGET_LANGUAGE
    to_path = current_config.INPUT_RAW_CORPUS_TARGET_LANGUAGE
    copy_file_from_path1_to_path2(from_path, to_path)

    #post_edition.tgt (neu co xu ly post-edition, vi du: wmt15)
    if str(config_end_user.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE) != "None":
        from_path = config_end_user.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE
        to_path = current_config.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE
        copy_file_from_path1_to_path2(from_path, to_path)
    #end if

    """
    #LIST_OF_ID_SENTENCES_ASR
    from_path = config_end_user.LIST_OF_ID_SENTENCES_ASR
    to_path = current_config.LIST_OF_ID_SENTENCES_ASR
    copy_file_from_path1_to_path2(from_path, to_path)

    #hypothesis_asr_path
    from_path = config_end_user.HYPOTHESIS_ASR_PATH
    to_path = current_config.HYPOTHESIS_ASR_PATH
    copy_file_from_path1_to_path2(from_path, to_path)

    #reference_asr_path
    from_path = config_end_user.REFERENCE_ASR_PATH
    to_path = current_config.REFERENCE_ASR_PATH
    copy_file_from_path1_to_path2(from_path, to_path)

    #lowercasing & tokenizing post-edition
    tokenizer_raw_corpus(current_config.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE, current_config.LANGUAGE_ENGLISH, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING)
    """

    """tokenizer_raw_corpus(current_config.INPUT_RAW_CORPUS_SOURCE_LANGUAGE, current_config.LANGUAGE_FRENCH, current_config.SRC_REF_TEST_FORMAT_ROW)"""

    """
    from_path = current_config.INPUT_RAW_CORPUS_SOURCE_LANGUAGE
    to_path = current_config.SRC_REF_TEST_FORMAT_ROW
    copy_file_from_path1_to_path2(from_path, to_path)
    """

    #if "is_has_a_file_included_alignment" in "config_end_user" = 1
    #it should get the Target Source from file MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT with index = 1
    from_path = current_config.INPUT_RAW_CORPUS_TARGET_LANGUAGE
    to_path = current_config.TARGET_REF_TEST_FORMAT_ROW
    copy_file_from_path1_to_path2(from_path, to_path)

    """
    if config_end_user.IS_HAS_A_FILE_INCLUDED_ALIGNMENT == 1:
        get_file_hypothethis_from_output_moses(config_end_user.ONE_BEST_LIST_INCLUDED_ALIGNMENT, current_config.TARGET_REF_TEST_FORMAT_ROW)
    else:
        #version - bo sung
        tokenizer_raw_corpus(current_config.INPUT_RAW_CORPUS_SOURCE_LANGUAGE, current_config.LANGUAGE_FRENCH, current_config.SRC_REF_TEST_FORMAT_ROW)
        tokenizer_raw_corpus(current_config.INPUT_RAW_CORPUS_TARGET_LANGUAGE, current_config.LANGUAGE_ENGLISH, current_config.TARGET_REF_TEST_FORMAT_ROW)
    """

    #lowercase_raw_corpus_not_tokenizer
    #LOWERCASE
    #TOKENIZER
    is_lowercase = check_value_boolean(config_end_user.LOWERCASE)
    is_tokenizer = check_value_boolean(config_end_user.TOKENIZER)

    if is_lowercase and not is_tokenizer:
        print("lowercase_raw_corpus_not_tokenizer")
        if str(config_end_user.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE) != "None":
            lowercase_raw_corpus_not_tokenizer(current_config.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE, current_config.LANGUAGE_SPANISH,                                        current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING)
        #end if

        lowercase_raw_corpus_not_tokenizer(current_config.INPUT_RAW_CORPUS_SOURCE_LANGUAGE, current_config.LANGUAGE_ENGLISH, current_config.SRC_REF_TEST_FORMAT_ROW)

        #lowercase_raw_corpus_not_tokenizer(current_config.INPUT_RAW_CORPUS_TARGET_LANGUAGE, current_config.LANGUAGE_SPANISH, current_config.TARGET_REF_TEST_FORMAT_ROW)
    elif is_lowercase is True and is_tokenizer is True:
        tokenizer_raw_corpus(current_config.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE, current_config.LANGUAGE_ENGLISH, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING)

        tokenizer_raw_corpus(current_config.INPUT_RAW_CORPUS_SOURCE_LANGUAGE, current_config.LANGUAGE_FRENCH, current_config.SRC_REF_TEST_FORMAT_ROW)
        #tokenizer_raw_corpus(current_config.INPUT_RAW_CORPUS_TARGET_LANGUAGE, current_config.LANGUAGE_ENGLISH, current_config.TARGET_REF_TEST_FORMAT_ROW)
    #end if

    ###########################################################################

    #language model: 2 files
    from_path = config_end_user.LANGUAGE_MODEL_SOURCE_LANGUAGE
    to_path = current_config.LANGUAGE_MODEL_SRC
    copy_file_from_path1_to_path2(from_path, to_path)

    from_path = config_end_user.LANGUAGE_MODEL_TARGET_LANGUAGE
    to_path = current_config.LANGUAGE_MODEL_TGT
    copy_file_from_path1_to_path2(from_path, to_path)

    ###########################################################################
    #Output from Google & Bing Translator: 2 files

    from_path = config_end_user.GOOGLE_TRANSLATOR
    to_path = current_config.GOOGLE_TRANSLATE_CORPUS
    copy_file_from_path1_to_path2(from_path, to_path)

    from_path = config_end_user.BING_TRANSLATOR
    to_path = current_config.BING_TRANSLATE_CORPUS
    copy_file_from_path1_to_path2(from_path, to_path)

    ###########################################################################
    #n best list using MOSES: 2 files
    from_path = config_end_user.ONE_BEST_LIST_INCLUDED_ALIGNMENT
    to_path = current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT
    copy_file_from_path1_to_path2(from_path, to_path)

    from_path = config_end_user.N_BEST_LIST_INCLUDED_ALIGNMENT
    to_path = current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT
    copy_file_from_path1_to_path2(from_path, to_path)
    ###########################################################################
    #version moses
    version_moses = config_end_user.VERSION_MOSES
    print("\n Version of moses for this solution: %s" % version_moses)
    ###########################################################################
    ###########################################################################

    print("Done-copy_raw_files")


#**************************************************************************#

#**************************************************************************#
#B1: Preprocessing
#File output of Google & Bing Translator
#Language Model: (included)
#    config_end_user.LANGUAGE_MODEL_SOURCE_LANGUAGE-> current_config.LANGUAGE_MODEL_SRC
#    config_end_user.LANGUAGE_MODEL_TARGET_LANGUAGE -> current_config.LANGUAGE_MODEL_TGT
#file_pattern_format_row_ape = current_config.PATTERN_REF_TEST_FORMAT_ROW_APE
#extension_src, extension_tgt = current_config.EXTENSION_SOURCE, current_config.EXTENSION_TARGET
#config_end_user.PATH_TO_TOOL_GIZA, current_config.MODEL_DIR_PATH, current_config.MT_HYPOTHESIS_OUTPUT_1_BESTLIST_INCLUDED_ALIGNMENT_APE
#Note: if file_lang_model_src_lang_path == "": thi khong copy language model :)
def get_preprocessing_ape( file_input_format_row_src_lang_path, file_input_format_row_tgt_lang_path, src_lang, tgt_lang, need_tokenizing, need_lowercasing, file_google_translator_path, file_bing_translator_path, file_output_path_src_lang, file_output_path_tgt_lang, file_output_path_src_lang_format_col, file_output_path_tgt_lang_format_col, file_output_path_src_lang_treetagger_format_row, file_output_path_tgt_lang_treetagger_format_row, file_output_path_src_lang_treetagger_format_col, file_output_path_tgt_lang_treetagger_format_col, file_output_google_path, file_output_bing_path, file_pattern_format_row_ape, extension_src, extension_tgt, dir_tool_giza_path, model_dir_path, file_alignment_output_path, file_lang_model_src_lang_path = "", file_lang_model_tgt_lang_path = "", file_output_lang_model_src_lang_path = "", file_output_lang_model_tgt_lang_path = ""):

    ###########################################################################
    # Preprocessing raw input corpus
    ###########################################################################
    feature_name = "Preprocessing raw input corpus"
    print(feature_name)

    #language model: 2 files
    if file_lang_model_src_lang_path != "":
        from_path = file_lang_model_src_lang_path
        to_path = file_output_lang_model_src_lang_path
        copy_file_from_path1_to_path2(from_path, to_path)

        from_path = file_lang_model_tgt_lang_path
        to_path = file_output_lang_model_tgt_lang_path
        copy_file_from_path1_to_path2(from_path, to_path)
    #end if
    ###########################################################################

    is_lowercase = need_lowercasing
    is_tokenizer = need_tokenizing

    #output filename
    #file_output_path_src_lang = file_output_pattern + "after_preprocessing." + src_lang
    #file_output_path_tgt_lang = file_output_pattern + "after_preprocessing." + tgt_lang

    if is_lowercase and not is_tokenizer:
        print("lowercasing but NOT tokenizing")
        lowercase_raw_corpus_not_tokenizer(file_input_format_row_src_lang_path, src_lang, file_output_path_src_lang)
        lowercase_raw_corpus_not_tokenizer(file_input_format_row_tgt_lang_path, tgt_lang, file_output_path_tgt_lang)
    elif is_lowercase and is_tokenizer:
        print("lowercasing and tokenizing")
        tokenizer_raw_corpus(file_input_format_row_src_lang_path, src_lang, file_output_path_src_lang)
        tokenizer_raw_corpus(file_input_format_row_tgt_lang_path, tgt_lang, file_output_path_tgt_lang)
    else:  #No need both lowercasing and tokenizing
        #source language
        from_path = file_input_format_row_src_lang_path
        to_path = file_output_path_src_lang
        copy_file_from_path1_to_path2(from_path, to_path)

        #target language
        from_path = file_input_format_row_tgt_lang_path
        to_path = file_output_path_tgt_lang
        copy_file_from_path1_to_path2(from_path, to_path)
    #end if

    ###########################################################################
    #Output from Google & Bing Translator: 2 files

    #output filename
    #file_output_google_path = file_output_pattern + "after_preprocessing_google_translator"
    #file_output_bing_path = file_output_pattern + "after_preprocessing_bing_translator"

    from_path = file_google_translator_path
    to_path = file_output_google_path
    copy_file_from_path1_to_path2(from_path, to_path)

    from_path = file_bing_translator_path
    to_path = file_output_bing_path
    copy_file_from_path1_to_path2(from_path, to_path)

    ##########################################################################
    ## Using TreeTagger for Source & Target Corpus
    ##########################################################################
    feature_name = "Using TreeTagger for Source & Target Corpus"
    print(feature_name)
    get_output_treetagger_format_row(file_output_path_src_lang, src_lang, file_output_path_src_lang_treetagger_format_row)
    get_output_treetagger_format_row(file_output_path_tgt_lang, tgt_lang, file_output_path_tgt_lang_treetagger_format_row)

    ##########################################################################
    ## Converting raw text & POS text from format ROW to format COLUMN
    ##########################################################################
    feature_name = "Converting raw text & POS text from format ROW to format COLUMN"
    print(feature_name)
    #Corpus###########
    #Source Language
    convert_format_row_to_format_column(file_output_path_src_lang, file_output_path_src_lang_format_col)

    #Target Language
    convert_format_row_to_format_column(file_output_path_tgt_lang, file_output_path_tgt_lang_format_col)

    #TreeTagger########
    #Source Language
    convert_format_row_to_format_column(file_output_path_src_lang_treetagger_format_row, file_output_path_src_lang_treetagger_format_col)

    #Target Language
    convert_format_row_to_format_column(file_output_path_tgt_lang_treetagger_format_row, file_output_path_tgt_lang_treetagger_format_col)

    ##########################################################################
    ## Get alignment by MOSES (step1-3) using Giza++
    ##########################################################################
    feature_name = "Get alignment by MOSES (step1-3) using Giza++"
    print(feature_name)

    #Dung tool moses de lay alignment va lay theo dang 1-best-list
    #get_file_alignments_target_to_source_word_alignment_using_moses(pattern_file_path, extension_source, extension_target, path_to_tool_giza,
    # output_directory_path, file_output_path)
    #command_line = command_line + script_path + " -corpus "+ current_config.PATTERN_REF_TEST_FORMAT_ROW + " -f "+ current_config.EXTENSION_SOURCE +" -e "+
    # current_config.EXTENSION_TARGET + " -alignment grow-diag-final-and --first-step 1 --last-step 3 --external-bin-dir="+
    # config_end_user.PATH_TO_TOOL_GIZA +" --model-dir=" + current_config.MODEL_DIR_PATH
    get_file_alignments_target_to_source_word_alignment_using_moses(file_pattern_format_row_ape, extension_src, extension_tgt, dir_tool_giza_path,
                                                                    model_dir_path, file_alignment_output_path)


#**************************************************************************#
#**************************************************************************#
def preprocessing_corpus(result_output_path):
    """
    Preprocessing corpus for our solution.

    :type result_output_path: string
    :param result_output_path: path of log-file that contains results of DEMO
    """
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #introduction of this solution
    #print_introduction(result_output_path)

    feature_name = "BEGIN Task - Preprocessing"
    print_time(feature_name, result_output_path)

    ##########################################################################
    ## Copy Raw Corpus
    ##########################################################################

    feature_name = "Copy Raw Corpus"
    print_time(feature_name, result_output_path)
    copy_raw_files()
    print_result(feature_name, result_output_path)



    ##########################################################################
    ## Using TreeTagger for Source & Target Corpus
    ##########################################################################
    feature_name = "Using TreeTagger for Source & Target Corpus"
    print_time(feature_name, result_output_path)

    #ce_agent
    get_output_treetagger_format_row(current_config.SRC_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_FRENCH,
                                     current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW)

    get_output_treetagger_format_row(current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_ENGLISH,
                                     current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW)



    print_result(feature_name,result_output_path)  

    ##########################################################################
    ## Converting raw text & POS text from format row to format column
    ##########################################################################
    feature_name = "Converting raw text & POS text from format row to format column"
    print_time(feature_name, result_output_path)

    #Corpus###########
    #Source Language
    convert_format_row_to_format_column(current_config.SRC_REF_TEST_FORMAT_ROW, current_config.SRC_REF_TEST_FORMAT_COL)

    #Target Language
    convert_format_row_to_format_column(current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.TARGET_REF_TEST_FORMAT_COL)

    #TreeTagger########
    #Source Language
    convert_format_row_to_format_column(current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.SRC_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL)

    #Target Language
    convert_format_row_to_format_column(current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_ROW, current_config.TARGET_REF_TEST_OUTPUT_TREETAGGER_FORMAT_COL)

    print_result(feature_name, result_output_path)
    ##########################################################################

    ##########################################################################
    ## Get alignment by using Giza++
    ##########################################################################
    ##########################################################################

    feature_name = "END Task - Preprocessing"
    print_time(feature_name, result_output_path)
#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    current_config = load_configuration()

    preprocessing_corpus(current_config.PREPROCESSING_MESSAGE_OUTPUT)

    print('OK')
