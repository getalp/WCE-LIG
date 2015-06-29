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

    #chu y: chuong trinh se sinh ra theo tuan tu 9000 cau dau cho train + 1000 dev + 881 test
    number_of_sentences_in_file_for_training = 10000
    number_of_sentences_in_file_for_developing = 0
    #number_of_sentences_in_file_for_testing = 881 # co nghia la con lai bao nhieu thi dua qua file testing

    #10 000
    number_of_sentences_in_file_for_developing_to = number_of_sentences_in_file_for_training + number_of_sentences_in_file_for_developing

    #10 881
    #number_of_sentences_in_file_for_testing_to = number_of_sentences_in_file_for_developing_to + number_of_sentences_in_file_for_testing

    number_of_current_sentence = 1

    current_config = load_configuration()

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

    current_config = load_configuration()

    #B1: "paste" all of output from extracting phase --> one file
    generating_merged_features()

    #################################
    #Demo with Sequential Corpus:
    corpus_type = current_config.SEQUENTIAL_CORPUS

    #demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)
    demo_name = "System_1"
    number_of_sentences_in_file_for_training = 11500
    number_of_sentences_in_file_for_developing = 0
    number_of_template = 4
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)
    """old version --> ref in notebook :)
    template.en1 : All features + bigram + trigram
    template.en2 : Remove some bigram
    template.en3 : template.en1, replace 'U' by '*'
    template.en4 : template.en2, replace 'U' by '*'
    template.en5 : template.en1 within 'same' list of features with Quang
    template.en6 : template.en2 within 'same' list of features with Quang
    template.en7 : Enable bigram & Disable trigram
    template.en8 : Disable bigram & trigram
    template.en9 : Disable bigram & trigram, but re-enable bigram alignment
    """


    """
Chosing:

+ Template 2 - for System 1
+ Template 5 - for System 1 with the 'same' features
---------------------------------------------------------------
*** Template_1_System_1 classifier Good/Bad:
X-Bad = 4538     Y-Bad = 21701   Z-Bad = 4538
X-Good = 0       Y-Good = 0      Z-Good = 17163
B        Pr=0.2091       Rc=1.0000       F1=0.3459
G        Pr=-1.0000      Rc=0.0000       F1=-1.0000
---------------------------------------------------------------
*** Template_2_System_1 classifier Good/Bad:
X-Bad = 1526     Y-Bad = 3262    Z-Bad = 4538
X-Good = 15427   Y-Good = 18439          Z-Good = 17163
B        Pr=0.4678       Rc=0.3363       F1=0.3913
G        Pr=0.8367       Rc=0.8989       F1=0.8666
---------------------------------------------------------------
*** Template_3_System_1 classifier Good/Bad:
X-Bad = 4538     Y-Bad = 21701   Z-Bad = 4538
X-Good = 0       Y-Good = 0      Z-Good = 17163
B        Pr=0.2091       Rc=1.0000       F1=0.3459
G        Pr=-1.0000      Rc=0.0000       F1=-1.0000
---------------------------------------------------------------
*** Template_4_System_1 classifier Good/Bad:
X-Bad = 4538     Y-Bad = 21701   Z-Bad = 4538
X-Good = 0       Y-Good = 0      Z-Good = 17163
B        Pr=0.2091       Rc=1.0000       F1=0.3459
G        Pr=-1.0000      Rc=0.0000       F1=-1.0000
---------------------------------------------------------------
*** Template_5_System_1 classifier Good/Bad:
X-Bad = 1439     Y-Bad = 3042    Z-Bad = 4538
X-Good = 15560   Y-Good = 18659          Z-Good = 17163
B        Pr=0.4730       Rc=0.3171       F1=0.3797
G        Pr=0.8339       Rc=0.9066       F1=0.8687
---------------------------------------------------------------
*** Template_6_System_1 classifier Good/Bad:
X-Bad = 1460     Y-Bad = 3145    Z-Bad = 4538
X-Good = 15478   Y-Good = 18556          Z-Good = 17163
B        Pr=0.4642       Rc=0.3217       F1=0.3801
G        Pr=0.8341       Rc=0.9018       F1=0.8667
---------------------------------------------------------------
*** Template_7_System_1 classifier Good/Bad:
X-Bad = 1495     Y-Bad = 3170    Z-Bad = 4538
X-Good = 15488   Y-Good = 18531          Z-Good = 17163
B        Pr=0.4716       Rc=0.3294       F1=0.3879
G        Pr=0.8358       Rc=0.9024       F1=0.8678
---------------------------------------------------------------
*** Template_8_System_1 classifier Good/Bad:
X-Bad = 4538     Y-Bad = 21701   Z-Bad = 4538
X-Good = 0       Y-Good = 0      Z-Good = 17163
B        Pr=0.2091       Rc=1.0000       F1=0.3459
G        Pr=-1.0000      Rc=0.0000       F1=-1.0000
---------------------------------------------------------------
*** Template_9_System_1 classifier Good/Bad:
X-Bad = 1402     Y-Bad = 2903    Z-Bad = 4538
X-Good = 15662   Y-Good = 18798          Z-Good = 17163
B        Pr=0.4829       Rc=0.3089       F1=0.3768
G        Pr=0.8332       Rc=0.9125       F1=0.8711
---------------------------------------------------------------
    """

    """
---------------------------------------------------------------
*** Template_1_System_1 classifier Good/Bad:
X-Bad = 1301     Y-Bad = 3029    Z-Bad = 4538
X-Good = 15435   Y-Good = 18672          Z-Good = 17163
B        Pr=0.4295       Rc=0.2867       F1=0.3439
G        Pr=0.8266       Rc=0.8993       F1=0.8614
---------------------------------------------------------------
*** Template_2_System_1 classifier Good/Bad:
X-Bad = 1333     Y-Bad = 3110    Z-Bad = 4538
X-Good = 15386   Y-Good = 18591          Z-Good = 17163
B        Pr=0.4286       Rc=0.2937       F1=0.3486
G        Pr=0.8276       Rc=0.8965       F1=0.8607
---------------------------------------------------------------
*** Template_3_System_1 classifier Good/Bad:
X-Bad = 4538     Y-Bad = 21701   Z-Bad = 4538
X-Good = 0       Y-Good = 0      Z-Good = 17163
B        Pr=0.2091       Rc=1.0000       F1=0.3459
G        Pr=-1.0000      Rc=0.0000       F1=-1.0000
---------------------------------------------------------------
*** Template_4_System_1 classifier Good/Bad:
X-Bad = 4538     Y-Bad = 21701   Z-Bad = 4538
X-Good = 0       Y-Good = 0      Z-Good = 17163
B        Pr=0.2091       Rc=1.0000       F1=0.3459
G        Pr=-1.0000      Rc=0.0000       F1=-1.0000
---------------------------------------------------------------
*** Template_5_System_1 classifier Good/Bad:
X-Bad = 1264     Y-Bad = 2964    Z-Bad = 4538
X-Good = 15463   Y-Good = 18737          Z-Good = 17163
B        Pr=0.4265       Rc=0.2785       F1=0.3370
G        Pr=0.8253       Rc=0.9009       F1=0.8614
---------------------------------------------------------------
*** Template_6_System_1 classifier Good/Bad:
X-Bad = 1271     Y-Bad = 2935    Z-Bad = 4538
X-Good = 15499   Y-Good = 18766          Z-Good = 17163
B        Pr=0.4330       Rc=0.2801       F1=0.3402
G        Pr=0.8259       Rc=0.9030       F1=0.8628
---------------------------------------------------------------

    """

    """
    demo_name = "System_2"
    number_of_sentences_in_file_for_training = 9000
    number_of_sentences_in_file_for_developing = 1000
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)

    demo_name = "System_3"
    number_of_sentences_in_file_for_training = 9500
    number_of_sentences_in_file_for_developing = 500
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)

    demo_name = "System_4"
    number_of_sentences_in_file_for_training = 8705
    number_of_sentences_in_file_for_developing = 1088
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)

    demo_name = "System_5"
    number_of_sentences_in_file_for_training = 9793
    number_of_sentences_in_file_for_developing = 544
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)
    """
    #################################
    """
    #Demo with Random Corpus:
    corpus_type = current_config.RANDOM_CORPUS

    demo_name = "System_6"
    number_of_sentences_in_file_for_training = 10000
    number_of_sentences_in_file_for_developing = 0
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)

    demo_name = "System_7"
    number_of_sentences_in_file_for_training = 9000
    number_of_sentences_in_file_for_developing = 1000
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)

    demo_name = "System_8"
    number_of_sentences_in_file_for_training = 9500
    number_of_sentences_in_file_for_developing = 500
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)

    demo_name = "System_9"
    number_of_sentences_in_file_for_training = 8705
    number_of_sentences_in_file_for_developing = 1088
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)

    demo_name = "System_10"
    number_of_sentences_in_file_for_training = 9793
    number_of_sentences_in_file_for_developing = 544
    number_of_template = 2
    demo_system(demo_name, corpus_type, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing, number_of_template)
    """

    """
    #get_random_index_of_sentences_for_train_dev_test(number_of_sentences_merged_file, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)
    number_of_sentences_merged_file = 10881
    number_of_sentences_in_file_for_training = 9000
    number_of_sentences_in_file_for_developing = 1000

    #get random index list for training, developing and testing
    list_index_training, list_index_developing, list_index_testing = get_random_index_of_sentences_for_train_dev_test(number_of_sentences_merged_file, number_of_sentences_in_file_for_training, number_of_sentences_in_file_for_developing)

    #is_disjoint(list_reference, list_test) in common_function
    #training & developing
    if is_disjoint(list_index_training, list_index_developing):
        print("There is NOT any item in both list_index_training and list_index_developing.")
    else:
        print("There is some items in both list_index_training and list_index_developing.")

        #get_list_intersection(list_reference, list_test) in common_function
        list_intersection = get_list_intersection(list_index_training, list_index_developing)
        length = len(list_intersection)
        print("Length of list intersection is: %d" %length)
        print(list_intersection)

    #training & testing
    if is_disjoint(list_index_training, list_index_testing):
        print("There is NOT any item in both list_index_training and list_index_testing.")
    else:
        print("There is some items in both list_index_training and list_index_testing.")

    #developing & testing
    if is_disjoint(list_index_developing, list_index_testing):
        print("There is NOT any item in both list_index_developing and list_index_testing.")
    else:
        print("There is some items in both list_index_developing and list_index_testing.")

    print ('OK')

    #get_list_index_of_empty_line(file_input_path)
    list_index_empty_line = get_list_index_of_empty_line(current_config.OUTPUT_MERGED_FEATURES)
    print(list_index_empty_line)
    print("The number of sentences in merged file is: %d" %len(list_index_empty_line))
    """

