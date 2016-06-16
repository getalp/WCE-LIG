# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 10:46:58 2015
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

"""
from config.configuration import *
from feature.common_functions import *
from metrics.common_function_metrics import *
"""
from common_module.cm_config import load_configuration
from common_module.cm_file import generating_merged_features

#**************************************************************************#
"""
B1: Ket hop cac feature theo thu tu bang lenh "paste". Sau do chi du lieu thanh cac phan khac nhau: train, dev, test
B2: Tao template phu hop voi "en". Chu y: Nen tao nhieu template de co the kiem tra duoc muc do chinh xac cua template
B3: Dung wapiti voi cac template cho truoc de tao CRF model. Sau do, wapiti dung model de kiem tra lai du lieu dung ?%
"""
#**************************************************************************#
#B2: Tao cac file dung cho qua trinh train; dev; test
def creating_sequential_corpus_train_dev_test_file_from_merged_file_version1(file_input_path):
    """
    Generating the corpus for training, developing and testing from merge file.

    :type file_input_path: string
    :param file_input_path: path to merged file that contains all features

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed merged file that contains all features')
    config_end_user = load_config_end_user()
    current_config = load_configuration()

    #number of sentences for training, developing and testing
    number_of_sentences_all = int(config_end_user.RAW_CORPUS_TRAINING_SIZE) + int(config_end_user.RAW_CORPUS_TEST_SIZE)
    number_of_sentences_in_file_for_training = int(config_end_user.RAW_CORPUS_TRAINING_SIZE)
    number_of_sentences_in_file_for_developing = 0
    #number_of_sentences_in_file_for_testing = number_of_sentences_all - number_of_sentences_in_file_for_training - number_of_sentences_in_file_for_developing
    number_of_sentences_in_file_for_testing = config_end_user.RAW_CORPUS_TEST_SIZE


    #10 000
    number_of_sentences_in_file_for_developing_to = number_of_sentences_in_file_for_training + number_of_sentences_in_file_for_developing


    number_of_current_sentence = 1

    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    #for writing:
    file_writer_train = open(current_config.TRAIN_FILE_PATH, mode = 'w', encoding = 'utf-8')
    file_writer_dev = open(current_config.DEV_FILE_PATH, mode = 'w', encoding = 'utf-8')
    file_writer_test = open(current_config.TEST_FILE_PATH, mode = 'w', encoding = 'utf-8')

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line) == 0: #cau moi xuat hien
            number_of_current_sentence += 1
        else:
            if number_of_current_sentence <= number_of_sentences_in_file_for_training:
                file_writer_train.write(line)
            elif number_of_current_sentence <= number_of_sentences_in_file_for_developing_to:
                file_writer_dev.write(line)
            else:
                file_writer_test.write(line)
            #end if

        if number_of_current_sentence <= number_of_sentences_in_file_for_training:
            file_writer_train.write('\n')
        elif number_of_current_sentence <= number_of_sentences_in_file_for_developing_to:
            file_writer_dev.write('\n')
        else:
            file_writer_test.write('\n')
        #end if

    #end for

    #close file
    file_reader.close()
    file_writer_train.close()
    file_writer_dev.close()
    file_writer_test.close()

#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:

    config_end_user = load_config_end_user()
    current_config = load_configuration()

    #number of sentences for training, developing and testing
    number_of_sentences_all = int(config_end_user.RAW_CORPUS_TRAINING_SIZE) + int(config_end_user.RAW_CORPUS_TEST_SIZE)
    number_of_sentences_in_file_for_training = int(config_end_user.RAW_CORPUS_TRAINING_SIZE)
    number_of_sentences_in_file_for_developing = 0
    number_of_sentences_in_file_for_testing = config_end_user.RAW_CORPUS_TEST_SIZE

    #B1: "paste" all of output from extracting phase --> one file
    generating_merged_features()

    #################################
    #Demo with Sequential Corpus:
    corpus_type = current_config.SEQUENTIAL_CORPUS

    demo_name = "System_1"
    number_of_template = 4
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)
