# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 11:25:12 2014
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

"""
*** Muc dich: #Tim Backoff Behavior
Xem ly thuyet trang 45 - These

Chu y:
7 6 5 4 3 2 1
A B C D E F G

Buoc 0: Cho truoc file target-4gram co dang. Chu y: O co nghia la tu nay la OOV
1
3
2
3
0
1

2
4
3
2
Chu y: Cac cau cach nhau bang khoang trang.
Buoc 1:
~GeTools/Target_ngram-BackOffBehavior$ java CreateBackoffBehaviour target-4gram.txt result_backoff_behavior.txt
"""
import sys
import os

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
from common_module.cm_file import is_existed_file
from common_module.cm_config import load_configuration
#**************************************************************************#
def feature_backoff_behaviour(file_input_path, file_output_path):
    """
    Checking each number of each line (in file_input_path) that is the longest target gram length. To see algorithm: contact to Tien Ngoc LE :) Email: ngoc-tien.le@imag.fr

    :type file_input_path: string
    :param file_input_path: contains each number of each line that is the longest target gram length; there is a empty line among the sentences.

    :type file_output_path: string
    :param file_output_path: contains corpus with format each "word" in each line; there is a empty line among the sentences. ABCDEFG ~ 7654321

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #Them 1 dong trong trong file input
    file_append = open(file_input_path, mode = 'a', encoding = 'utf-8')#, 'a')
    file_append.write("\n")
    file_append.close()

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    sentence = [] # empty sentence

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        if len(line) > 0:
            #Dua tat ca so nguyen trong cau vao trong list de xu ly
            sentence.append(int(line)) #chuyen thanh so nguyen de dze xu ly

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        else: #len(line) == 0
            #bat dau xu ly thuat toan voi tung tu trong cau
            #duyet cau hien tai trong list sentence
            #theo index
            for i in range(len(sentence)): # from 0 to n-1
                x = sentence[i] #gia tri cua tu hien tai

                if x == 0:
                    file_writer.write('G\n') #Khong co tu nay trong LM
                    continue

                if i == 0: # Xet tu thu 1 trong cau, voi x > 0
                    file_writer.write('F\n') # chi ton tai [x] trong LM
                elif i == 1: # Xet tu thu 2 trong cau
                    x_1 = sentence[i-1] #gia tri cua tu truoc no (i-1)
                    if x >= 2:
                        file_writer.write('C\n') #Ton tai [x_1,x] trong LM
                    else:
                        if x_1 >= 1:
                            file_writer.write('E\n') #Ton tai "x_1" va "x" doc lap trong LM
                        else:
                            file_writer.write('F\n')
                else: # i >= 2
                    x_1 = sentence[i-1] #gia tri cua tu truoc no (i-1)
                    x_2 = sentence[i-2] #gia tri cua tu truoc no (i-2)

                    if x >= 3:
                        file_writer.write('A\n') #Ton tai [x_2,x_1,x] trong LM
                    elif x == 2:
                        if x_1 >= 2:
                            file_writer.write('B\n') #Ton tai [...,x_2,x_1] va [x_1,x] ton tai doc lap trong LM
                        else:
                            file_writer.write('C\n') #Ton tai [x_1,x] ton tai trong LM
                    else: #x == 1
                        if x_1 >= 1 and x_2 >= 1:
                            file_writer.write('D\n') #Ton tai [x_2,x_1] va [x] ton tai doc lap trong LM
                        elif x_1 >= 1:
                            file_writer.write('E\n') #Ton tai [x_2,x_1] va [x] ton tai doc lap trong LM
                        else:
                            file_writer.write('F\n') #Ton tai [x_2] va [x_1] va [x] ton tai doc lap trong LM

            file_writer.write('\n') # empty line in output file
            sentence = [] # empty sentence

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
if __name__ == "__main__":
    #Test case:
    #feature_backoff_behaviour(file_input_path, file_output_path)

    current_config = load_configuration()

    print('longest target gram length corpus')
    print (current_config.LONGEST_TARGET_GRAM_LENGTH)

    print('output')
    print(current_config.BACKOFF_BEHAVIOUR)

    feature_backoff_behaviour( current_config.LONGEST_TARGET_GRAM_LENGTH, current_config.BACKOFF_BEHAVIOUR)

    print ('OK')