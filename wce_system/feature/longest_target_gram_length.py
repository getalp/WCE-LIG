# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 11:29:58 2014
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
Muc dich: Tim target-source ?gram dai nhat trong Language Model

Chu y: doi voi Target thi khong can file alignment. Nhung doi voi SOURCE thi can phai co alignment de biet word-target nay duoc aligned voi word-SOURCE nao?

Buoc 1: Tao file chua xac suat theo tung gram (Language Model)
Vi du:
surgeons in los angeles , it said they were also told me to camus .
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
--> co nghia la: chuoi "(1) (2) (3) said" co trong LM, nhung khong co 5 gram; 0.0330624 la xac suat cua 4-gram; [ -1.48067 ] : duoc tinh tu ham log xac suat trong Phrase-based Model
Chu y: trong n-gram, n lon --> Do phuc tap lon

cat /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MThypothesis_2643_tokenized.txt | /home/tienle/Documents/Develops/DevTools/srilm/bin/i686-m64/ngram  -order 4 -lm /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MT08.en.lm  -ppl - -debug 2 -no-eos -no-sos > tmpfile-order4

*** Chu y: Tong hop 2 buoc (buoc 2 va 3) tren bang version 2 cua file 'create-ngram-feature.sh'
~GeTools/Target_ngram-BackOffBehavior$ ./create-ngram-feature-version2.sh tmpfile-order4 target-4gram.txt

Khong dung Buoc 2 va Buoc 3 *****************************
#Buoc 2:
#~GeTools/Target_ngram-BackOffBehavior$ chmod +x create-ngram-feature.sh
#~GeTools/Target_ngram-BackOffBehavior$ ./create-ngram-feature.sh tmpfile-order4 target_4gram.txt

#Buoc 3: Ham chuyen tu chuoi thanh so ?!?! --> Da lam duoc
"""

import os
import sys
import threading

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
#from common_module.cm_util import
from common_module.cm_file import is_existed_file
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_script import run_chmod, call_script
#**************************************************************************#
#Buoc 1: Tao file chua xac suat theo tung gram (Language Model)
#Goi ham ngram tu SRILM
def get_probability_from_language_model(file_input_path, language_model_path,  n_gram, file_output_path):
    """
    Using tool "ngram" in SRILM for extracting the probability of the word in the sentence of hypothesis
    =============================================================
    Example:
    file_input_path: surgeons in los angeles , it said they were also told me to camus .
    file_output_path:
    ******BEGIN-Example

    surgeons in los angeles , it said they were also told me to camus .

	p( surgeons |  ) 	= [1gram] 2.63551e-05 [ -4.57914 ]
	p( in | surgeons ...) 	= [2gram] 0.0349445 [ -1.45662 ]
	p( los | in ...) 	= [2gram] 0.00100078 [ -2.99966 ]
	p( angeles | los ...) 	= [3gram] 0.992084 [ -0.00345142 ]
	p( , | angeles ...) 	= [4gram] 0.268746 [ -0.570658 ]
	p( it | , ...) 	= [4gram] 0.00495355 [ -2.30508 ]
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
	p( they | said ...) 	= [4gram] 0.00135257 [ -2.86884 ]
	p( were | they ...) 	= [4gram] 0.37974 [ -0.420514 ]
	p( also | were ...) 	= [4gram] 0.00891918 [ -2.04967 ]
	p( told | also ...) 	= [4gram] 0.0217238 [ -1.66306 ]
	p( me | told ...) 	= [3gram] 0.00838321 [ -2.07659 ]
	p( to | me ...) 	= [4gram] 0.0552748 [ -1.25747 ]
	p( camus | to ...) 	= [2gram] 1.8308e-07 [ -6.73736 ]
	p( . | camus ...) 	= [3gram] 0.55815 [ -0.253249 ]

    0 sentences, 15 words, 0 OOVs
    0 zeroprobs, logprob= -30.722 ppl= 111.721 ppl1= 111.721

    ******END-Example

    * Other example:
    surgeons in los angeles , it said they were also told me to camus .
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
    --> co nghia la: chuoi "(1) (2) (3) said" co trong LM, nhung khong co 5 gram; 0.0330624 la xac suat cua 4-gram; [ -1.48067 ] : duoc tinh tu ham log xac suat trong Phrase-based Model
    Chu y: trong n-gram, n lon --> Do phuc tap lon
    =============================================================

    :type file_input_path: string
    :param file_input_path: file output of Machine Translation that is hypothesis.

    type language_model_path: string
    :param language_model_path: The Language Model of the Target Language.

    type n_gram: integer
    :param n_gram: in order to generate the probability file from tool "ngram" in SRILM

    :type file_output_path: string
    :param file_output_path: contains the probability of each word of each sentence that is given in the file_input_path.

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - row')

    if not os.path.exists(language_model_path):
        raise TypeError('Not Existed file Language Model')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file Language Model"
    is_existed_file(language_model_path, str_message_if_not_existed)

    #cat /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MThypothesis_2643_tokenized.txt | /home/tienle/Documents/Develops/DevTools/srilm/bin/i686-m64/ngram  -order 4 -lm /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MT08.en.lm  -ppl - -debug 2 -no-eos -no-sos > tmpfile-order4
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #using ngram in order to generate probability of each word
    path_script = current_config.TOOL_CREATE_PROBABILITY_EACH_WORD_FROM_LANGUAGE_MODEL #Path to the shell script in SRILM Tool

    #change mode execute script
    run_chmod(path_script)

    #command_line = path_script + " " + file_input_path + " " + current_config.TOOL_NGRAM + " " + str(n_gram) + " " + language_model_path + " " + file_output_path
    command_line = path_script + " " + file_input_path + " " + config_end_user.TOOL_NGRAM + " " + str(n_gram) + " " + language_model_path + " " + file_output_path
    """
    #print("Command line:")
    #print(command_line)

    args = shlex.split(command_line)
    #print("args")
    #print(args)

    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(current_config.TOOL_NGRAM))

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
    Da chuyen vao common_functions
    """

    print(command_line)

    #call_script(command_line, path_to_script)
    #call_script(command_line, current_config.TOOL_NGRAM)
    call_script(command_line, config_end_user.TOOL_NGRAM)

#**************************************************************************#
#Buoc 2 & 3: Tinh longest gram length
"""
Tong hop 2 buoc (buoc 2 va 3) tren bang version 2 cua file 'create-ngram-feature.sh'
~GeTools/Target_ngram-BackOffBehavior$ ./create-ngram-feature-version2.sh tmpfile-order4 target-4gram.txt
"""
def get_probability_from_language_model_threads(file_input_path, language_model_path,  n_gram, file_output_path, current_config, config_end_user):
    """
    Using tool "ngram" in SRILM for extracting the probability of the word in the sentence of hypothesis
    =============================================================
    Example:
    file_input_path: surgeons in los angeles , it said they were also told me to camus .
    file_output_path:
    ******BEGIN-Example

    surgeons in los angeles , it said they were also told me to camus .

	p( surgeons |  ) 	= [1gram] 2.63551e-05 [ -4.57914 ]
	p( in | surgeons ...) 	= [2gram] 0.0349445 [ -1.45662 ]
	p( los | in ...) 	= [2gram] 0.00100078 [ -2.99966 ]
	p( angeles | los ...) 	= [3gram] 0.992084 [ -0.00345142 ]
	p( , | angeles ...) 	= [4gram] 0.268746 [ -0.570658 ]
	p( it | , ...) 	= [4gram] 0.00495355 [ -2.30508 ]
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
	p( they | said ...) 	= [4gram] 0.00135257 [ -2.86884 ]
	p( were | they ...) 	= [4gram] 0.37974 [ -0.420514 ]
	p( also | were ...) 	= [4gram] 0.00891918 [ -2.04967 ]
	p( told | also ...) 	= [4gram] 0.0217238 [ -1.66306 ]
	p( me | told ...) 	= [3gram] 0.00838321 [ -2.07659 ]
	p( to | me ...) 	= [4gram] 0.0552748 [ -1.25747 ]
	p( camus | to ...) 	= [2gram] 1.8308e-07 [ -6.73736 ]
	p( . | camus ...) 	= [3gram] 0.55815 [ -0.253249 ]

    0 sentences, 15 words, 0 OOVs
    0 zeroprobs, logprob= -30.722 ppl= 111.721 ppl1= 111.721

    ******END-Example

    * Other example:
    surgeons in los angeles , it said they were also told me to camus .
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
    --> co nghia la: chuoi "(1) (2) (3) said" co trong LM, nhung khong co 5 gram; 0.0330624 la xac suat cua 4-gram; [ -1.48067 ] : duoc tinh tu ham log xac suat trong Phrase-based Model
    Chu y: trong n-gram, n lon --> Do phuc tap lon
    =============================================================

    :type file_input_path: string
    :param file_input_path: file output of Machine Translation that is hypothesis.

    type language_model_path: string
    :param language_model_path: The Language Model of the Target Language.

    type n_gram: integer
    :param n_gram: in order to generate the probability file from tool "ngram" in SRILM

    :type file_output_path: string
    :param file_output_path: contains the probability of each word of each sentence that is given in the file_input_path.

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - row')

    if not os.path.exists(language_model_path):
        raise TypeError('Not Existed file Language Model')
    """
    #str_message_if_not_existed = "Not Existed file corpus input with format - column"
    #is_existed_file(file_input_path, str_message_if_not_existed)

    str_message_if_not_existed = "Not Existed file Language Model"
    is_existed_file(language_model_path, str_message_if_not_existed)

    #cat /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MThypothesis_2643_tokenized.txt | /home/tienle/Documents/Develops/DevTools/srilm/bin/i686-m64/ngram  -order 4 -lm /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MT08.en.lm  -ppl - -debug 2 -no-eos -no-sos > tmpfile-order4
    #current_config = load_configuration()
    #config_end_user = load_config_end_user()

    #using ngram in order to generate probability of each word
    path_script = current_config.TOOL_CREATE_PROBABILITY_EACH_WORD_FROM_LANGUAGE_MODEL #Path to the shell script in SRILM Tool
    script_path = config_end_user.TOOL_NGRAM
    #change mode execute script
    run_chmod(path_script)

    #command_line = path_script + " " + file_input_path + " " + current_config.TOOL_NGRAM + " " + str(n_gram) + " " + language_model_path + " " + file_output_path
    #command_line = path_script + " " + file_input_path + " " + config_end_user.TOOL_NGRAM + " " + str(n_gram) + " " + language_model_path + " " + file_output_path
    l_threads = []
    for l_inc in range(1,current_config.THREADS+1):
      str_message_if_not_existed = file_input_path + "." + str(l_inc) + " does not exist! Not Existed file corpus input with format - column"
      is_existed_file(file_input_path + "." + str(l_inc), str_message_if_not_existed)
      command_line_thread = path_script + " " + file_input_path+"."+str(l_inc) + " " + config_end_user.TOOL_NGRAM + " " + str(n_gram) + " " + language_model_path + " " + file_output_path+"."+str(l_inc)
      print(command_line_thread)
      ts = threading.Thread(target=call_script, args=(command_line_thread, script_path))
      l_threads.append(ts)
      ts.start()
    for myT in l_threads:
      myT.join()    


    """
    #print("Command line:")
    #print(command_line)

    args = shlex.split(command_line)
    #print("args")
    #print(args)

    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(current_config.TOOL_NGRAM))

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
    Da chuyen vao common_functions
    """


    #call_script(command_line, path_to_script)
    #call_script(command_line, current_config.TOOL_NGRAM)
    #call_script(command_line, config_end_user.TOOL_NGRAM)

#**************************************************************************#
#Buoc 2 & 3: Tinh longest gram length
"""
Tong hop 2 buoc (buoc 2 va 3) tren bang version 2 cua file 'create-ngram-feature.sh'
~GeTools/Target_ngram-BackOffBehavior$ ./create-ngram-feature-version2.sh tmpfile-order4 target-4gram.txt
"""

def create_longest_target_gram_length(file_input_path, file_output_path):
    """
    Using script for extracting the longest target gram length of the word in the sentence of hypothesis
    =============================================================
    Example:
    file_input_path:
    ******BEGIN-Example

    surgeons in los angeles , it said they were also told me to camus .

	p( surgeons |  ) 	= [1gram] 2.63551e-05 [ -4.57914 ]
	p( in | surgeons ...) 	= [2gram] 0.0349445 [ -1.45662 ]
	p( los | in ...) 	= [2gram] 0.00100078 [ -2.99966 ]
	p( angeles | los ...) 	= [3gram] 0.992084 [ -0.00345142 ]
	p( , | angeles ...) 	= [4gram] 0.268746 [ -0.570658 ]
	p( it | , ...) 	= [4gram] 0.00495355 [ -2.30508 ]
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
	p( they | said ...) 	= [4gram] 0.00135257 [ -2.86884 ]
	p( were | they ...) 	= [4gram] 0.37974 [ -0.420514 ]
	p( also | were ...) 	= [4gram] 0.00891918 [ -2.04967 ]
	p( told | also ...) 	= [4gram] 0.0217238 [ -1.66306 ]
	p( me | told ...) 	= [3gram] 0.00838321 [ -2.07659 ]
	p( to | me ...) 	= [4gram] 0.0552748 [ -1.25747 ]
	p( camus | to ...) 	= [2gram] 1.8308e-07 [ -6.73736 ]
	p( . | camus ...) 	= [3gram] 0.55815 [ -0.253249 ]

    0 sentences, 15 words, 0 OOVs
    0 zeroprobs, logprob= -30.722 ppl= 111.721 ppl1= 111.721

    ******END-Example

    * Other example:
    surgeons in los angeles , it said they were also told me to camus .
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
    --> co nghia la: chuoi "(1) (2) (3) said" co trong LM, nhung khong co 5 gram; 0.0330624 la xac suat cua 4-gram; [ -1.48067 ] : duoc tinh tu ham log xac suat trong Phrase-based Model
    Chu y: trong n-gram, n lon --> Do phuc tap lon
    =============================================================

    :type file_input_path: string
    :param file_input_path: file output of script "get_probability_from_language_model".

    :type file_output_path: string
    :param file_output_path: contains the longest target gram length of each word of each sentence. Among the sentences, there is a empty line.

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')

    current_config = load_configuration()

    path_script = current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH #Path to the shell script in directory "lib"

    command_line = path_script + " " + file_input_path + " " + file_output_path
    """
    #print("Command line:")
    #print(command_line)

    args = shlex.split(command_line)

    #print("args")
    #print(args)


    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH))

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
    """
    #call_script(command_line, path_to_script)
    #script_path=current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH
    #l_threads = []
    #for l_inc in range(1,current_config.THREADS+1):
      #command_line_thread = path_script + " " + file_input_path+"."+str(l_inc) + " " + file_output_path+"."+str(l_inc)
      #print(command_line_thread)
      #ts = threading.Thread(target=call_script, args=(command_line_thread, script_path))
      #l_threads.append(ts)
      #ts.start()
    #for myT in l_threads:
      #myT.join()    
    call_script(command_line, current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH)
#**************************************************************************#
#HYPOTHESIS_ROW_CORPUS
def create_longest_target_gram_length_threads(file_input_path, file_output_path, current_config):
    """
    Using script for extracting the longest target gram length of the word in the sentence of hypothesis
    =============================================================
    Example:
    file_input_path:
    ******BEGIN-Example

    surgeons in los angeles , it said they were also told me to camus .

	p( surgeons |  ) 	= [1gram] 2.63551e-05 [ -4.57914 ]
	p( in | surgeons ...) 	= [2gram] 0.0349445 [ -1.45662 ]
	p( los | in ...) 	= [2gram] 0.00100078 [ -2.99966 ]
	p( angeles | los ...) 	= [3gram] 0.992084 [ -0.00345142 ]
	p( , | angeles ...) 	= [4gram] 0.268746 [ -0.570658 ]
	p( it | , ...) 	= [4gram] 0.00495355 [ -2.30508 ]
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
	p( they | said ...) 	= [4gram] 0.00135257 [ -2.86884 ]
	p( were | they ...) 	= [4gram] 0.37974 [ -0.420514 ]
	p( also | were ...) 	= [4gram] 0.00891918 [ -2.04967 ]
	p( told | also ...) 	= [4gram] 0.0217238 [ -1.66306 ]
	p( me | told ...) 	= [3gram] 0.00838321 [ -2.07659 ]
	p( to | me ...) 	= [4gram] 0.0552748 [ -1.25747 ]
	p( camus | to ...) 	= [2gram] 1.8308e-07 [ -6.73736 ]
	p( . | camus ...) 	= [3gram] 0.55815 [ -0.253249 ]

    0 sentences, 15 words, 0 OOVs
    0 zeroprobs, logprob= -30.722 ppl= 111.721 ppl1= 111.721

    ******END-Example

    * Other example:
    surgeons in los angeles , it said they were also told me to camus .
	p( said | it ...) 	= [4gram] 0.0330624 [ -1.48067 ]
    --> co nghia la: chuoi "(1) (2) (3) said" co trong LM, nhung khong co 5 gram; 0.0330624 la xac suat cua 4-gram; [ -1.48067 ] : duoc tinh tu ham log xac suat trong Phrase-based Model
    Chu y: trong n-gram, n lon --> Do phuc tap lon
    =============================================================

    :type file_input_path: string
    :param file_input_path: file output of script "get_probability_from_language_model".

    :type file_output_path: string
    :param file_output_path: contains the longest target gram length of each word of each sentence. Among the sentences, there is a empty line.

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    #if not os.path.exists(file_input_path):
        #raise TypeError('Not Existed file corpus input with format - column')

    #current_config = load_configuration()

    path_script = current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH #Path to the shell script in directory "lib"

    #command_line = path_script + " " + file_input_path + " " + file_output_path
    """
    #print("Command line:")
    #print(command_line)

    args = shlex.split(command_line)

    #print("args")
    #print(args)


    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh ngram -> run script
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH))

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
    """
    #call_script(command_line, path_to_script)
    #call_script(command_line, current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH)
    script_path = current_config.TOOL_CREATE_LONGEST_TARGET_GRAM_LENGTH
    l_threads = []
    for l_inc in range(1,current_config.THREADS+1):
      if not os.path.exists(file_input_path+"."+str(l_inc)):
          raise TypeError('Not Existed file corpus input with format - column')
      command_line_thread = path_script + " " + file_input_path+"."+str(l_inc) + " " + file_output_path+"."+str(l_inc)
      print(command_line_thread)
      ts = threading.Thread(target=call_script, args=(command_line_thread, script_path))
      l_threads.append(ts)
      ts.start()
    for myT in l_threads:
      myT.join()    
    
#**************************************************************************#
#HYPOTHESIS_ROW_CORPUS
if __name__ == "__main__":
    current_config = load_configuration()

    #Buoc 1: Tao file chua xac suat theo tung gram (Language Model)
    #Goi ham ngram tu SRILM
    #Test case: checking the function
    #get_probability_from_language_model(file_input_path, language_model_path,  n_gram, file_output_path)
    #get_probability_from_language_model(current_config.HYPOTHESIS_ROW_CORPUS, current_config.LANGUAGE_MODEL_EN, 5, current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS)
    get_probability_from_language_model( current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_MODEL_TGT, 5, current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS)

    #Buoc 2:
    #create_longest_target_gram_length(file_input_path, file_output_path)
    create_longest_target_gram_length( current_config.PROBABILITY_HYPOTHESIS_ROW_CORPUS,  current_config.LONGEST_TARGET_GRAM_LENGTH)

    print ('OK')

#**************************************************************************#
#**************************************************************************#
