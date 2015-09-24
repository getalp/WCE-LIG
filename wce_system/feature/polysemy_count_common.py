# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 11:45:30 2014
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
Buoc 1:
    input: file output cua TreeTagger doi voi tung ngon ngu (EN, FR, ES, VI ...)
    output: file voi moi dong co dang
        stemmed_word NOUN/VERB/ADJECTIVE/ADVERB/OTHER

Buoc 2: Tinh so luong nghia cua tu (goi ham dem so luong nghia bang babelnet)

Buoc 3: Xoa cac dong khong can thiet; Thay the cac doan khong dung; Loc cac dong chua du lieu can thiet

********************************
--> Phan chung: da so cac ham
--> Phan rieng: khai bao dict tagset cho tung ngon ngu khac nhau (Doi voi TreeTagger). Dung dict & list de bieu dien mang 2 chieu doi voi yeu cau o buoc 1.
"""

#common module - for polysemy-counting
import os
import sys

#for call shell script
#import shlex, subprocess

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
from common_module.cm_util import split_string_to_list_delimeter_tab, is_in_list, is_in_string
from common_module.cm_file import is_existed_file
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_script import call_script
#**************************************************************************#
def get_pos_in_format_babelnet( pos_treetager, dict_tagset_language):
    """
    Converting POS from format of TreeTagger to format of BabelNet. The POS in TreeTagger is assigned to one of five main types such as NOUN/VERB/ADJECTIVE/ADVERB/OTHER
    =============================================================
    Example:
    TreeTagger Format:  Pero	CCAD	pero
    BabelNet Format:    pero	OTHER

    :type pos_treetager: string
    :param pos_treetager: POS of TreeTagger

    :type dict_tagset_language: string
    :param dict_tagset_language: Dictionary contains list of tagset of language.

    :rtype: String of POS in BabelNet

    :raise ValueError: if any path is not existed
    """
    result = "OTHER"

    for i in dict_tagset_language:
        #Checking POS-TreeTagger in which type of dict-tagset
        if is_in_list(pos_treetager.strip(), dict_tagset_language[i]):
            return i

    #if not existed in dict-tagset
    return result
#**************************************************************************#
"""
Buoc 1:
    input: file output cua TreeTagger doi voi tung ngon ngu (EN, FR, ES, VI ...)
    output: file voi moi dong co dang
        stemmed_word NOUN/VERB/ADJECTIVE/ADVERB/OTHER
"""
def convert_format_treetagger_to_format_babelnet( file_input_path, dict_tagset_language, file_output_path):
    """
    Converting from format of TreeTagger to format of BabelNet. The POS in TreeTagger is assigned to one of five main types such as NOUN/VERB/ADJECTIVE/ADVERB/OTHER
    =============================================================
    Example:
    TreeTagger Format:  Pero	CCAD	pero
    BabelNet Format:    pero	OTHER

    :type file_input_path: string
    :param file_input_path: file output of TreeTagger whose each line has format 'word POS stemmed'. Among 'sentences' there is an empty line.

    type dict_tagset_language: string
    :param dict_tagset_language: Dictionary contains list of tagset of language.

    :type file_output_path: string
    :param file_output_path: each line contains format stemmed-word and POS converted; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #get list of recognition Proper name
    list_of_proper_name = ['<UNK>','<unknown>']

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')
            continue

        """Line 46755
        florence	NN	<unknown>
        <UNK>
        believes	VVZ	believe
        """
        """
        #Truong hop dac biet: khi du lieu chi chua UNK
        str_UNK = "<UNK>"
        if line == str_UNK:
            result_line = str_UNK.lower() + '\tOTHER\n'

            file_writer.write(result_line) #new line
            continue
        #end if
        """

        #Get column 2nd and 3rd (POS Stemmed_word)
        #get value at 3rd column (column stem) -> index=2
        #angeles NNS <unknown>
        values_cols = split_string_to_list_delimeter_tab(line)

        value_col_pos = values_cols[1] #POS, index=1
        value_col_stem = values_cols[2] #Stemmed_word, index=2

        #updating POS in BabelNet
        #get_pos_in_format_babelnet(pos_treetager, dict_tagset_language)
        value_col_pos_babel_net = get_pos_in_format_babelnet(value_col_pos, dict_tagset_language)

        #updating stemmed_word = <unknown> to values_cols[0]
        if is_in_list(value_col_stem, list_of_proper_name):
            value_col_stem = values_cols[0]

        #lowercasing the value in 'value_col_stem'
        result_line = value_col_stem.lower() + '\t' + value_col_pos_babel_net + '\n'

        file_writer.write(result_line) #new line

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
"""
Buoc 2: Tinh so luong nghia cua tu (goi ham dem so luong nghia bang babelnet)
"""
def feature_polysemy_count_language( file_input_path, target_language, file_output_path):
    """
    Counting each stemmed - word (w) of each line (in file_input_path) and POS optimized by converting to 5 main types such as NOUN/VERB/ADJECTIVE/ADVERB/OTHER

    :type file_input_path: string
    :param file_input_path: file output after preprocessing whose each line has format 'stemmed_word POS_after_preprocessing_in_5_types'. Among 'sentences' there is an empty line.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains corpus with format each "word" in each line is the number of polysemy count and -1 if POS is OTHER; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #~GeTools/BabelSenseCount_v25/BabelNet-2.5$ ./calculateSenses2.sh 328-result_Stemming.txt 328-result-senses.txt
    #Chu y: trong file "calculateSenses2.sh" --> "sense2.sh"
    #Chu y: trong file "calculateSenses2.sh": Can thay doi, neu muon tinh so luong nghia cho ngon ngu khac nhu: EN, FR
    #Goi script shell tren bang duong dan tuyet doi
    #/home/tienle/Documents/Develops/GeTools/BabelSenseCount_v25/BabelNet-2.5

    current_config = load_configuration()
    config_end_user = load_config_end_user()
    #print("Shell script name:")
    #print (current_config.TOOL_BABEL_NET_ES)

    path_script = "" #Path to the shell script in BabelNet Tool

    if target_language == current_config.LANGUAGE_SPANISH:
        #path_script = current_config.TOOL_BABEL_NET_ES
        path_script = config_end_user.TOOL_BABEL_NET_ES

    elif target_language == current_config.LANGUAGE_FRENCH:
        #path_script = current_config.TOOL_BABEL_NET_FR
        path_script = config_end_user.TOOL_BABEL_NET_FR

    elif target_language == current_config.LANGUAGE_ENGLISH:
        #path_script = current_config.TOOL_BABEL_NET_EN
        path_script = config_end_user.TOOL_BABEL_NET_EN

    command_line = path_script + " " + file_input_path + " " + file_output_path

    """
    #print("Command line:")
    #print(command_line)

    args = shlex.split(command_line)

    print("args")
    print(args)


    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh BabelNet -> run script
    #TOOL_BABEL_NET_DIR
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(current_config.TOOL_BABEL_NET_ES))

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
    """

    #call_script(command_line, path_to_script)
    if target_language == current_config.LANGUAGE_SPANISH:
        #path_script = current_config.TOOL_BABEL_NET_ES
        call_script(command_line, config_end_user.TOOL_BABEL_NET_ES)

    elif target_language == current_config.LANGUAGE_FRENCH:
        #path_script = current_config.TOOL_BABEL_NET_FR
        call_script(command_line, config_end_user.TOOL_BABEL_NET_FR)

    elif target_language == current_config.LANGUAGE_ENGLISH:
        #path_script = current_config.TOOL_BABEL_NET_EN
        call_script(command_line, config_end_user.TOOL_BABEL_NET_EN)
        #print("command_line: %s" %command_line)

#**************************************************************************#
def feature_polysemy_count_language_threads( file_input_path, target_language, file_output_path, current_config, config_end_user):
    """
    Counting each stemmed - word (w) of each line (in file_input_path) and POS optimized by converting to 5 main types such as NOUN/VERB/ADJECTIVE/ADVERB/OTHER

    :type file_input_path: string
    :param file_input_path: file output after preprocessing whose each line has format 'stemmed_word POS_after_preprocessing_in_5_types'. Among 'sentences' there is an empty line.

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_path: string
    :param file_output_path: contains corpus with format each "word" in each line is the number of polysemy count and -1 if POS is OTHER; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input with format - column"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #~GeTools/BabelSenseCount_v25/BabelNet-2.5$ ./calculateSenses2.sh 328-result_Stemming.txt 328-result-senses.txt
    #Chu y: trong file "calculateSenses2.sh" --> "sense2.sh"
    #Chu y: trong file "calculateSenses2.sh": Can thay doi, neu muon tinh so luong nghia cho ngon ngu khac nhu: EN, FR
    #Goi script shell tren bang duong dan tuyet doi
    #/home/tienle/Documents/Develops/GeTools/BabelSenseCount_v25/BabelNet-2.5

    #current_config = load_configuration()
    #config_end_user = load_config_end_user()
    #print("Shell script name:")
    #print (current_config.TOOL_BABEL_NET_ES)

    path_script = "" #Path to the shell script in BabelNet Tool

    if target_language == current_config.LANGUAGE_SPANISH:
        #path_script = current_config.TOOL_BABEL_NET_ES
        path_script = config_end_user.TOOL_BABEL_NET_ES

    elif target_language == current_config.LANGUAGE_FRENCH:
        #path_script = current_config.TOOL_BABEL_NET_FR
        path_script = config_end_user.TOOL_BABEL_NET_FR

    elif target_language == current_config.LANGUAGE_ENGLISH:
        #path_script = current_config.TOOL_BABEL_NET_EN
        path_script = config_end_user.TOOL_BABEL_NET_EN

    command_line = path_script + " " + file_input_path + " " + file_output_path
    print(command_line)
    """
    #print("Command line:")
    #print(command_line)

    args = shlex.split(command_line)

    print("args")
    print(args)


    #y tuong:
    #luu thu muc hien tai vao bien tam
    #get current working directory
    current_working_directory = os.getcwd()

    #vao thu muc chua chuong trinh BabelNet -> run script
    #TOOL_BABEL_NET_DIR
    #To change current working dir to the one containing your script
    os.chdir(os.path.dirname(current_config.TOOL_BABEL_NET_ES))

    #run script
    p = subprocess.Popen(args)
    #subprocess.call(args)
    output, err = p.communicate()
    #print("output: %s ; error: %s" % (output, err))

    #ra thu muc hien hanh ban dau
    os.chdir(current_working_directory)
    """

    #call_script(command_line, path_to_script)
    if target_language == current_config.LANGUAGE_SPANISH:
        #path_script = current_config.TOOL_BABEL_NET_ES
        call_script(command_line, config_end_user.TOOL_BABEL_NET_ES)

    elif target_language == current_config.LANGUAGE_FRENCH:
        #path_script = current_config.TOOL_BABEL_NET_FR
        call_script(command_line, config_end_user.TOOL_BABEL_NET_FR)

    elif target_language == current_config.LANGUAGE_ENGLISH:
        #path_script = current_config.TOOL_BABEL_NET_EN
        call_script(command_line, config_end_user.TOOL_BABEL_NET_EN)
        #print("command_line: %s" %command_line)

#**************************************************************************#
"""
Buoc 3: Xoa cac dong khong can thiet; Thay the cac doan khong dung; Loc cac dong chua du lieu can thiet
"""
def filter_number_of_polysemy( file_input_path, file_output_path):
    """
    Filter the lines that contain string "Number of senses:"

    :type file_input_path: string
    :param file_input_path: file output after feature_polysemy_count Among 'sentences' there is an empty line.

    :type file_output_path: string
    :param file_output_path: contains the number of polysemy count and -1 if POS is OTHER; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input')
    """
    str_message_if_not_existed = "Input file does not exist: " + file_input_path
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    pattern = "Number of senses:"

    #read data in openned file
    for line in file_reader:
        #trim line
        line = line.strip()

        #if empty line then write empty line in result_file
        #line in ('\n', '\r\n')
        #if line in ['\n', '\r\n']:
        if len(line)==0:
            file_writer.write('\n')

        elif is_in_string(pattern, line): #is_start_with(line.lower(), pattern.lower()) #old version: is_in_string(pattern, line)
            #Delete pattern & write the number
            line = line.replace(pattern,'')
            file_writer.write(line)
            file_writer.write('\n')
        #end if
    #end for

    #close 2 files
    file_reader.close()
    file_writer.close()
#**************************************************************************#