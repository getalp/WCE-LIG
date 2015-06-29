# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 16:51:33 2014
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

#Purpose: Extracting the following features: WPP any, Nodes, Min, Max

"""
Buoc 1: Tao Constituent Tree

#head
~/Documents/Develops/GeTools/Lingua-LinkParser-1.17/scripts$ ./getConstituentTree_head.sh thu.txt result_head

#tail
~/Documents/Develops/GeTools/Lingua-LinkParser-1.17/scripts$ ./getConstituentTree_tail.sh thu.txt result_tail

Buoc 2: Constituent Label & Distance to Root
#head
~/Documents/Develops/GeTools/Lingua-LinkParser-1.17/scripts$ java ConstituentLabel result_head result_head_constituentlabel

#tail
~/Documents/Develops/GeTools/Lingua-LinkParser-1.17/scripts$ java ConstituentLabel result_tail result_tail_constituentlabel

Buoc 3: NULL link
THU: Target sentences, recased
log: OUtput file with NULL LINK

~/Documents/Develops/GeTools/Lingua-LinkParser-1.17/scripts$ ./generate_null_link_feature.sh thu.txt result
"""

import os
import string
import re
import sys

#for call shell script
#import shlex, subprocess
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
from nltk.tree import Tree

from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import is_existed_file, get_line_given_number_of_sentence
from common_module.cm_script import call_script


#b1: nen hoan chinh phan preprocessing & chuan hoa ten cua corpus trong qua trinh preprocessing

#b2: dang chinh sua o distance to root

#b3: nen hoan chinh ham find_and_replace_string_dong_ngoac vi no can cho tuong lai

#**************************************************************************#
#ky niem 3 ngay chien dau de hieu nltk va lam duoc ham nay :)
def get_list_distance_to_root(tree, h=0):
    """
    Getting the distances from leaves to root

    :type tree: string
    :param tree: output from Tree.fromstring in NLTK toolkit

    :type h: string
    :param h: height or distance from leaf to root

    :rtype: list of distances from leaves to root
    """
    result = []
    for child in tree:
        if isinstance(child, Tree):
            result.extend(get_list_distance_to_root(child, h+1))
        else:
            result.append(h)
    #end for
    return result
#**************************************************************************#
def get_list_constituent_label(tree):
    """
    Getting the constituent label from leaves to root

    :type tree: string
    :param tree: output from Tree.fromstring in NLTK toolkit

    :type h: string
    :param h: height or distance from leaf to root

    :rtype: list of distances from leaves to root
    """
    result = [pos for word, pos in tree.pos()]

    return result
#**************************************************************************#
#http://www.link.cs.cmu.edu/link/null-explanation.html
#http://www.link.cs.cmu.edu/cgi-bin/link/construct-page-4.cgi#submit
#str3 = "(S (NP (NP The government) (PP in (NP Serbia))) (VP has (VP been (VP trying (S (VP to (VP convince (NP the West) (S (VP to (VP defer (NP the decision) until (PP by mid (NP 2007))))))))))).)"
#until & mid : NULL link
def null_link(tree):
    #Vi output lay bang Berkeley Parser nen KHONG DUNG feature nay
    return ""

#**************************************************************************#
#ky niem 2 ngay chien dau de hieu nltk & berkeley "KHONG HIEU NHAU" cho nao va lam duoc ham nay :)
def find_and_replace_string_dong_ngoac(string_input):
    """
    Replace the ambiguous phrases in output of Berkeley Parser

    :type string_input: string
    :param string_input: line output with format constituent tree

    :rtype: return string after preprocessing
    """

    #"(SYM )" --> "(SYM dong_ngoac)"
    #p = re.compile(r'({1}[A-Z]+\b){1}')
    #print([(a.start(), a.end()) for a in list(re.finditer(r'\(+[A-Z]+\b \)', astring))])

    end_match = [a.end() for a in list(re.finditer(r'\(+[A-Z]+\b \)', string_input))]

    if len(end_match) ==0:
        return string_input #van giu nguyen
    else:
        str_dong_ngoac = " dong_ngoac" # just for Tien Ngoc LE :), purpose: normalized the output of Berkeley Parser

        #duyet nguoc lai va them vao
        j = len(end_match) - 1
        while j >= 0:
            index_temp = end_match[j] - 1

            temp_2 = string_input[:index_temp] + str_dong_ngoac + string_input[index_temp:]

            string_input = temp_2

            j = j - 1
        #end while

    return string_input
#**************************************************************************#
#Buoc: tien xu ly de xu dung nltk
#dem so dau ngoac dong va ngoac mo phai bang nhau. Neu khong bang thi bao loi dong do
#replace (SYM )) --> (SYM mo_ngoac); (SYM )) --> (SYM dong_ngoac)
#new_str = string.replace(our_str, 'World', 'Jackson')
def pre_processing(string_input):
    """
    Replace the ambiguous phrases in output of Berkeley Parser

    :type string_input: string
    :param string_input: line output with format constituent tree

    :rtype: return string after preprocessing
    """
    result = ""

    #replace (SYM ()) hay (NN ()) hay (FW ()) --> (SYM mo_ngoac); (SYM )) hay (NN ) --> (SYM dong_ngoac)
    result = string_input.replace("()", "mo_ngoac")
    #result = string_input.replace("SYM (", "SYM mo_ngoac")
    #result = string_input.replace("(SYM ())", "(SYM mo_ngoac)")
    #result = result.replace("(NN ())", "(NN mo_ngoac)")
    #result = result.replace("(FW ())", "(FW mo_ngoac)")

    #Khong tim thay trong Regular Expression --> viet code de choi voi cai nay thui :)
    result = find_and_replace_string_dong_ngoac(result)
    #result = result.replace("(SYM )", "(SYM dong_ngoac)")
    #result = result.replace("(NN )", "(NN dong_ngoac)")

    #can viet theo regular expression, vi da tim ra cong thuc chung bi hieu nham giua NLTK va Berkeley Parser

    return result
#**************************************************************************#
def feature_distance_to_root(file_input_path, file_corpus_format_row, file_output_path):
    """
    Getting distances from leaves to root

    :type file_input_path: string
    :param file_input_path: output with format constituent tree

    :type file_corpus_format_row: string
    :param file_corpus_format_row: file raw corpus after pre-processing

    :type file_output_path: string
    :param file_output_path: contains feature distance to root of each "word"; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output from TreeTagger')
    """
    str_message_if_not_existed = "Not Existed file output from TreeTagger"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    number_of_sentence = 1
    #number_of_words_in_sentence = 0

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

        #preprocessing with output of Berkeley Parser
        #line = pre_processing(line)

        print(line)

        #BEGIN-xu ly neu dong chua cau khong the parser bang Berkeley Parser
        current_config = load_configuration()

        if line == current_config.RESULT_BERKELEY_PARSER_UNKNOWN:
            #lay so tu cua dong trong du lieu goc
            #get_line_given_number_of_sentence(file_input_path, number_of_sentence)
            line_corpus = get_line_given_number_of_sentence(file_corpus_format_row, number_of_sentence)

            number_of_words_in_sentence = len(line_corpus.strip().split())

            ## tuy vao kieu du lieu output ma chung ta them vao trong file_output_path
            ## OUT_OF_KNOWDLEGE_INT = -1
            type_out_of_knowledge = str(current_config.OUT_OF_KNOWDLEGE_INT)
            range_item = range(number_of_words_in_sentence)
            for i in range_item:
                file_writer.write(type_out_of_knowledge)
                file_writer.write("\n")
            #end for

            file_writer.write("\n") # empty line for seperating the "lines"

            print("Da xu ly xong cau thu %d." %number_of_sentence)
            number_of_sentence += 1

            continue
        #end if
        #END-xu ly neu dong chua cau khong the parser bang Berkeley Parser

        tree = Tree.fromstring(line)

        # distances to root
        distances = get_list_distance_to_root(tree)

        if len(distances) == 0:
            print("Kiem tra loi nay gap... Contact to Tien Ngoc LE :)")
            break

        #write to output file
        for item in distances:
            line_out = str(item)
            file_writer.write(line_out)
            file_writer.write("\n")

            #number_of_words_in_sentence += 1
            #file_writer.write(" ") #just for testing
        #end for

        #file_writer.write(str(number_of_words_in_sentence))
        file_writer.write("\n") # empty line for seperating the "lines"
        #number_of_words_in_sentence = 0
        print("Da xu ly xong cau thu %d." %number_of_sentence)

        number_of_sentence += 1
    #end for

    #close 2 files
    file_reader.close()
    file_writer.close()

#**************************************************************************#
def feature_constituent_label(file_input_path, file_corpus_format_row, file_output_path):
    """
    Getting constituent label of each word

    :type file_input_path: string
    :param file_input_path: output with format constituent tree

    :type file_corpus_format_row: string
    :param file_corpus_format_row: file raw corpus after pre-processing

    :type file_output_path: string
    :param file_output_path: contains feature distance to root of each "word"; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output from TreeTagger')

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    number_of_sentence = 1
    #number_of_words_in_sentence = 0

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

        #preprocessing with output of Berkeley Parser
        #line = pre_processing(line)

        print(line)

        #BEGIN-xu ly neu dong chua cau khong the parser bang Berkeley Parser
        current_config = load_configuration()

        if line == current_config.RESULT_BERKELEY_PARSER_UNKNOWN:
            #lay so tu cua dong trong du lieu goc
            #get_line_given_number_of_sentence(file_input_path, number_of_sentence)
            line_corpus = get_line_given_number_of_sentence(file_corpus_format_row, number_of_sentence)

            number_of_words_in_sentence = len(line_corpus.strip().split())

            ## tuy vao kieu du lieu output ma chung ta them vao trong file_output_path
            ## OUT_OF_KNOWDLEGE_STRING = OOK
            type_out_of_knowledge = current_config.OUT_OF_KNOWDLEGE_STRING
            range_item = range(number_of_words_in_sentence)
            for i in range_item:
                file_writer.write(type_out_of_knowledge)
                file_writer.write("\n")
            #end for

            file_writer.write("\n") # empty line for seperating the "lines"

            print("Da xu ly xong cau thu %d." %number_of_sentence)
            number_of_sentence += 1

            continue
        #end if
        #END-xu ly neu dong chua cau khong the parser bang Berkeley Parser

        tree = Tree.fromstring(line)

        # constituent label
        labels = get_list_constituent_label(tree)

        if len(labels) == 0:
            print("Kiem tra loi nay gap... Contact to Tien Ngoc LE :)")
            break

        #write to output file
        for item in labels:
            file_writer.write(item)
            file_writer.write("\n")

            #number_of_words_in_sentence += 1
            #file_writer.write(" ") #just for testing
        #end for

        #file_writer.write(str(number_of_words_in_sentence))
        file_writer.write("\n") # empty line for seperating the "lines"
        #number_of_words_in_sentence = 0
        print("Da xu ly xong cau thu %d." %number_of_sentence)

        number_of_sentence += 1
    #end for

    #close 2 files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
#Do tieng Anh dau ngoac don trong qua trinh xay dung constituent tree co van de
#--> nen chuyen dau ( thanh dau [ va ) --> ]
def replace_parenthesis_for_english(file_input_path, file_output_path):
    """
    Replace parenthesis to brackets

    :type file_input_path: string
    :param file_input_path: corpus

    :type file_output_path: string
    :param file_output_path: corpus that is Replaced parenthesis to brackets

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file input')
    """
    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    current_config = load_configuration()

    command_line = "" #Path to the shell script in Tools lib
    script_path = current_config.REPLACE_PARENTHESIS

    command_line = script_path + " " + file_input_path + " " + file_output_path

    call_script(command_line, script_path)
#**************************************************************************#
"""
Buoc 1: Tao Constituent Tree

#head -> first Constituent Tree
~/Documents/Develops/GeTools/Lingua-LinkParser-1.17/scripts$ ./getConstituentTree_head.sh thu.txt result_head

#tail -> last Constituent Tree
~/Documents/Develops/GeTools/Lingua-LinkParser-1.17/scripts$ ./getConstituentTree_tail.sh thu.txt result_tail
"""
def generate_constituent_tree(file_input_path, target_language, file_output_constituent_tree_temp_path):
    """
    :type file_input_path: string
    :param file_input_path: corpus that is tokenized

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_constituent_tree_temp_path: string
    :param file_output_constituent_tree_temp_path: contains output path of the first constituent tree

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file input')
    """
    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    current_config = load_configuration()
    config_end_user = load_config_end_user()

    """
    #Lam theo y tuong: Lingua_Parser
    #file_output_first_constituent_tree_temp_path
    script_path = current_config.TOOL_GET_CONSTITUENT_FIRST
    command_line = script_path + " " + file_input_path + " " + file_output_first_constituent_tree_temp_path
    #call_script(command_line, script_path)
    print("Command for Get Constituent First-BEGIN")
    print(command_line)
    print("Command for Get Constituent First-END")

    #file_output_last_constituent_tree_temp_path
    script_path = current_config.TOOL_GET_CONSTITUENT_LAST
    command_line = script_path + " " + file_input_path + " " + file_output_last_constituent_tree_temp_path
    #call_script(command_line, script_path)
    print("Command for Get Constituent Last-BEGIN")
    print(command_line)
    print("Command for Get Constituent Last-END")
    """
    command_line = "" #Path to the shell script in BabelNet Tool
    script_path = ""
    grammar_path = ""

    if target_language == current_config.LANGUAGE_FRENCH: # the best for French :)
        #script_path = current_config.TOOL_GET_CONSTITUENT_FR
        script_path = config_end_user.TOOL_GET_CONSTITUENT_FR
        str_export_path = os.path.dirname(script_path) + "/../"
        command_line = script_path + " " + file_input_path + " " + file_output_constituent_tree_temp_path + " " + str_export_path

    else:
        if target_language == current_config.LANGUAGE_ENGLISH:
            #for english
            #~/Develops/Solution/eval_agent/tool/berkeley_parser$ ./berkeley_parser.sh eng_sm6.gr 1sentence.en 1sentence.en.result
            #note: khong the parser constituent tree cua "Guess why." --> result ="(())"

            #chuyen sang lam manual
            #Buoc 1: Them vao chu ngu "You guess why."
            #Buoc 2: ( (S (@S (NP (PRP You)) (VP (VBP guess) (SBAR (WHADVP (WRB why))))) (. .)) )
            #Buoc 3-Bo phan phan tich cua You: ( (S (@S (VP (VBP guess) (SBAR (WHADVP (WRB why))))) (. .)) )

            #grammar_path = current_config.GRAMMAR_EN_FOR_BERKELEY_PARSER_PATH
            grammar_path = config_end_user.GRAMMAR_EN_FOR_BERKELEY_PARSER_PATH

            """
            ##neu la tieng Anh thi thay the dau ( thanh [ va ) thanh ] --> result la file temp trong configuation
            file_input_path_temp = current_config.BERKELEY_PARSER_INPUT_EN
            replace_parenthesis_for_english(file_input_path, file_input_path_temp)
            ##va cap nhat duong dan file_input_path thanh duong dan chi dinh san trong configuration
            file_input_path = file_input_path_temp
            """

        elif target_language == current_config.LANGUAGE_SPANISH:
            #for Spanish
            #khong can dung binarize
            #java -jar BerkeleyParser-1.7.jar -gr spa_ancora.gr -inputFile 5sentences-EN_ES.hypothesis -outputFile result-5sentences
            #java -jar BerkeleyParser-1.7.jar -gr Grammar_File_Path -inputFile Input_Path -outputFile Result_Path
            #old version#java -jar BerkeleyParser-1.7.jar -gr spa_ancora.gr -binarize -inputFile 5sentences-EN_ES.hypothesis -outputFile result-5sentences

            #grammar_path = current_config.GRAMMAR_ES_FOR_BERKELEY_PARSER_PATH
            grammar_path = config_end_user.GRAMMAR_ES_FOR_BERKELEY_PARSER_PATH
        #end if

        ##neu la tieng Anh thi thay the dau ( thanh [ va ) thanh ] --> result la file temp trong configuation
        file_input_path_temp = current_config.BERKELEY_PARSER_INPUT
        replace_parenthesis_for_english(file_input_path, file_input_path_temp)
        ##va cap nhat duong dan file_input_path thanh duong dan chi dinh san trong configuration
        file_input_path = file_input_path_temp

        #for es; en; ar
        #script_path = current_config.TOOL_BERKELEY_PARSER_PATH
        script_path = config_end_user.TOOL_BERKELEY_PARSER_PATH
        # $1: grammar for Berkeley Parser
        # $2: input file
        # $3: output file
        command_line = script_path + " " + grammar_path + " " + file_input_path + " " + file_output_constituent_tree_temp_path
    #end if

    """
    print("Command for Get Constituent Tree - BEGIN")
    print("command_line=%s" %command_line)
    print("script_path=%s"%script_path)
    print("target_language= %s" %target_language)
    print("Command for Get Constituent Tree - END")
    """

    #export BONSAI=/home/lent/Téléchargements/a_moses/bonsai_v3.2
    call_script(command_line, script_path)
    #call_script_included_export(command_line, script_path, "BONSAI", "..")


    """
    /home/lent/Develops/Solution/eval_agent/eval_agent/feature/../../tool/bonsai_v3.2/bin/get_constituent_tree.sh /home/lent/Develops/Solution/eval_agent/eval_agent/feature/../corpus/preprocessing/881_output_preprocessing.fr /home/lent/Develops/Solution/eval_agent/eval_agent/feature/../extracted_features/en.column.feature_constituent_tree_temp.txt

./bonsai_bky_parse.sh: 98: ./bonsai_bky_parse.sh: /home/lent/Téléchargements/a_moses/bonsai_v3.2/src/do_prebky.pl: not found
Error: Unable to access jarfile /home/lent/Téléchargements/a_moses/bonsai_v3.2/resources/bkyjar/berkeleyParser-V1_0-fr.jar

    --> ERROR nay do thieu "export BONSAI=/home/lent/Develops/Solution/eval_agent/eval_agent/feature/../../tool/bonsai_v3.2/bin/../"
    """

#**************************************************************************#
def feature_constituent_label_get_list_distance_to_root_null_link( file_input_path, target_language, file_output_constituent_tree_temp_path, file_output_distance_to_root_path, file_output_constituent_label_path):
    """
    Getting the features Constituent Label & Distance to Root & NULL link

    :type file_input_path: string
    :param file_input_path: corpus that is tokenized

    :type target_language: string
    :param target_language: Target Language (EN, ES, FR)

    :type file_output_constituent_tree_temp_path: string
    :param file_output_constituent_tree_temp_path: contains output path of the first constituent tree

    :type file_output_distance_to_root_path: string
    :param file_output_distance_to_root_path: contains feature distance to root of each "word"; there is a empty line among the sentences.

    :type file_output_constituent_label_path: string
    :param file_output_constituent_label_path: contains feature constituent label of each "word"; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #Buoc 1: Tao Constituent Tree
    generate_constituent_tree(file_input_path, target_language, file_output_constituent_tree_temp_path)

    #Buoc: tien xu ly de xu dung nltk
    #dem so dau ngoac dong va ngoac mo phai bang nhau. Neu khong bang thi bao loi dong do
    #replace (SYM )) --> (SYM mo_ngoac); (SYM )) --> (SYM dong_ngoac)
    #new_str = string.replace(our_str, 'World', 'Jackson')


    #replace: (, ,) --> (PUNCT ,)
    #replace: (. .) --> (PUNCT .)
    #(! !)
    #(: -) --> (PUNCT -)
    #(: :) --> (PUNCT :)
    #(: ...)

    #Buoc 2: Distance to Root
    feature_distance_to_root(file_output_constituent_tree_temp_path, file_input_path, file_output_distance_to_root_path)

    #Buoc 3: Constituent Label
    feature_constituent_label(file_output_constituent_tree_temp_path, file_input_path, file_output_constituent_label_path)

    """
    Constituent Label

    >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
    >>> for s in t.subtrees(lambda t: t.height() == 2):
    ...     print(s)
            (D the)
            (N dog)
            (V chased)
            (D the)
            (N cat)
    """

    # NULL link --> #Vi output lay bang Berkeley Parser nen KHONG DUNG feature nay

#**************************************************************************#
if __name__=="__main__":
    #split sentences with ID from n-best-list
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #You should update target language
    target_language = config_end_user.TARGET_LANGUAGE

    #target_language = current_config.LANGUAGE_SPANISH # Spanish
    #target_language = current_config.LANGUAGE_ENGLISH # English
    #target_language = current_config.LANGUAGE_FRENCH # French

    #ES not for Spanish now !!!!! not tested
    #feature_constituent_label_get_list_distance_to_root_null_link(current_config.SRC_REF_TEST, current_config.LANGUAGE_SPANISH, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL)

    #chu y: cau 7006 chua dau "." o dau cau

    #EN --> OK
    #feature_constituent_label_get_list_distance_to_root_null_link( current_config.TARGET_REF_TEST_FORMAT_ROW,  current_config.LANGUAGE_ENGLISH, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL)

    #FR --> better within output of bonsai
    #feature_constituent_label_get_list_distance_to_root_null_link(current_config.SRC_REF_TEST_FORMAT_ROW, current_config.LANGUAGE_FRENCH, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL)

    #ES
    #feature_constituent_label_get_list_distance_to_root_null_link( current_config.TARGET_REF_TEST_FORMAT_ROW,  current_config.LANGUAGE_SPANISH, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL)

    #Doc lap ngon ngu
    feature_constituent_label_get_list_distance_to_root_null_link( current_config.TARGET_REF_TEST_FORMAT_ROW, target_language, current_config.CONSTITUENT_TREE_TEMP, current_config.DISTANCE_TO_ROOT, current_config.CONSTITUENT_LABEL)

    #testing for get distance to root with NLTK
    #import nltk
    #print(nltk.__path__)

    #from nltk.corpus import treebank
    #t = treebank.parsed_sents('wsj_0001.mrg')[0]
    #print (t)

    """
    #nen de 2 dau ngoac don giong nhu trong output cua Berkeley Parser --> khong can cong them 1 don vi cho distance to root
    str = "((SENT (NP (DET l') (PREF ex) (NC mannequin) (ADJ jerry) (NC hall) (COORD (CC et) (NP (DET sa) (NC fille)))) (PONCT ,) (VN (V georgia)) (PP (P may) (VPinf (VN (VINF jagger)))) (PONCT ,) (PP (P ï¿½lue) (NP (ADJ meilleur) (NC mannequin) (PP (P de) (NP (DET l') (NC annï¿½e))))) (PONCT .)))"
    str1 = "(SENT (NP (DET l') (PREF ex) (NC mannequin) (ADJ jerry) (NC hall) (COORD (CC et) (NP (DET sa) (NC fille)))) (PONCT ,) (VN (V georgia)) (PP (P may) (VPinf (VN (VINF jagger)))) (PONCT ,) (PP (P ï¿½lue) (NP (ADJ meilleur) (NC mannequin) (PP (P de) (NP (DET l') (NC annï¿½e))))) (PONCT .))"

    #dung de test is "NULL link"
    str3 = "((S (NP (NP The government) (PP in (NP Serbia))) (VP has (VP been (VP trying (S (VP to (VP convince (NP the West) (S (VP to (VP defer (NP the decision) until (PP by mid (NP 2007))))))))))).))"

    str4 = "( (X (@X (@X (@X (@X (@X (X (PP (IN with) (NP (NP (@NP (@NP (DT the) (JJ \")) (JJ clear)) (NN reduction)) (PP (IN of) (NP (@NP (DT the) (NN examination)) (NN load)))))) (, ,)) (X (SYM \"))) (X (VP (VBZ explains) (NP (@NP (NN accreditation) (NN council)) (NN chairman))))) (X (@X (@X (@X (FW reinhold) (FW grimm)) (X (SYM \"))) (S (NP (@NP (DT an) (JJ undesirable)) (NN development)) (VP (VBZ is) (VP (@VP (VP (TO to) (VP (VB be) (VP (VBN stopped)))) (, ,)) (SBAR (WHNP (WDT which)) (S (VP (VBD had) (NP (NP (@NP (DT a) (JJ grave)) (NN impact)) (PP (IN on) (NP (NN studiability))))))))))) (. .))) (X (SYM \"))) (. .)) )" #cau 384 trong 881 cau

    #Thay dau " bang tu quot
    str5 = "( (X (@X (@X (@X (@X (@X (X (PP (IN with) (NP (NP (@NP (@NP (DT the) (JJ quot)) (JJ clear)) (NN reduction)) (PP (IN of) (NP (@NP (DT the) (NN examination)) (NN load)))))) (, ,)) (X (SYM quot))) (X (VP (VBZ explains) (NP (@NP (NN accreditation) (NN council)) (NN chairman))))) (X (@X (@X (@X (FW reinhold) (FW grimm)) (X (SYM quot))) (S (NP (@NP (DT an) (JJ undesirable)) (NN development)) (VP (VBZ is) (VP (@VP (VP (TO to) (VP (VB be) (VP (VBN stopped)))) (, ,)) (SBAR (WHNP (WDT which)) (S (VP (VBD had) (NP (NP (@NP (DT a) (JJ grave)) (NN impact)) (PP (IN on) (NP (NN studiability))))))))))) (. .))) (X (SYM quot))) (. .)) )"

    #*********************************************** do du lieu vo van :)
    # the education and science union ( gew deemed the bonn decisions to be not radical enough : it is demanding a legal claim which would allow every graduate with a bachelor degree admission on a further masters course .
    #******loi o cau 406 -> tu them 1 dau ngoac don o cuoi dong
    str6 = "( (S (@S (@S (S (NP (@NP (@NP (@NP (@NP (@NP (DT the) (NN education)) (CC and)) (NN science)) (NN union)) (NN ()) (NN gew)) (VP (VBD deemed) (NP (NP (@NP (DT the) (JJ bonn)) (NNS decisions)) (SBAR (S (VP (TO to) (VP (@VP (VB be) (ADJP (RB not) (JJ radical))) (ADVP (RB enough))))))))) (: :)) (S (NP (PRP it)) (VP (VBZ is) (VP (VBG demanding) (NP (NP (@NP (DT a) (JJ legal)) (NN claim)) (SBAR (WHNP (WDT which)) (S (VP (MD would) (VP (VB allow) (S (NP (NP (DT every) (NN graduate)) (PP (IN with) (NP (@NP (DT a) (NN bachelor)) (NN degree)))) (VP (NN admission) (PP (IN on) (NP (@NP (@NP (DT a) (JJ further)) (NNS masters)) (NN course)))))))))))))) (. .)) ))"

    #cau 406 moi, sau khi bo dau (
    str7 = "( (S (@S (@S (S (NP (@NP (@NP (@NP (@NP (DT the) (NN education)) (CC and)) (NN science)) (NN union)) (NN gew)) (VP (VBD deemed) (NP (NP (@NP (DT the) (JJ bonn)) (NNS decisions)) (SBAR (S (VP (TO to) (VP (@VP (VB be) (ADJP (RB not) (JJ radical))) (ADVP (RB enough))))))))) (: :)) (S (NP (PRP it)) (VP (VBZ is) (VP (VBG demanding) (NP (NP (@NP (DT a) (JJ legal)) (NN claim)) (SBAR (WHNP (WDT which)) (S (VP (MD would) (VP (VB allow) (S (NP (NP (DT every) (NN graduate)) (PP (IN with) (NP (@NP (DT a) (NN bachelor)) (NN degree)))) (VP (NN admission) (PP (IN on) (NP (@NP (@NP (DT a) (JJ further)) (NNS masters)) (NN course)))))))))))))) (. .)) )"

    #cau 17 / 881, result bi thieu 2 tu :(
    str8 = "( (FRAG (@FRAG (@FRAG (X (@X (@X (@X (@X (@X (@X (@X (@X (X (NP (@NP (DT the) (JJ udf)) (NN alliance))) (, ,)) (VP (VBN controlled) (PP (IN by) (NP (@NP (NP (@NP (NN françois) (NN bayrou)) (POS 's)) (JJ democratic)) (NN movement))))) (X (SYM mongoac))) (FW modem)) (X (SYM dong_ngoac))) (, ,)) (VP (VBN reacted) (PP (IN on) (NP (NN friday))))) (TO to)) (NP (DT the) (NN buy))) (: -)) (SBAR (IN out) (S (NP (NN bid)) (VP (@VP (@VP (@VP (VBN made) (PP (IN by) (NP (@NP (@NP (NP (NP (@NP (@NP (DT the) (JJ new)) (NN centre)) (POS 's)) (NN president)) (, ,)) (NP (NN hervé) (NN morin))) (, ,)))) (PP (IN for) (NP (NP (DT the) (NN acronym)) (PP (IN of) (NP (@NP (@NP (DT the) (JJ former)) (NN giscardian)) (NN party)))))) (, ,)) (PP (IN by) (S (VP (@VP (VBG ordering) (NP (PRP him))) (S (RB not) (VP (TO to) (VP (@VP (@VP (@VP (VB use) (NP (PRP it))) (PP (IN under) (NP (DT any) (NNS circumstances)))) (, ,)) (S (VP (@VP (VBG threatening) (NP (JJ legal) (NN action))) (ADVP (RB otherwise)))))))))))))) (. .)) )"
    ##***************************************************************************
    ## loi o cau 406 -> fix -> preprocessing cho tot
    ## Loi tiep cau 743 -> giong loi o cau 406, nghia la du dau (
    ## cau 878
    ##### Nhung cau nay deu do qua trinh pre_processing lam sai, co le la qua trinh tokenizer ???
    ##***************************************************************************

    #cau 24
    str9 = "( (X (@X (@X (@X (@X (@X (@X (@X (SBAR (IN as) (S (NP (PRP you)) (VP (VBP are) (ADJP (RB well) (JJ aware))))) (, ,)) (S (NP (PRP you)) (VP (VBP have) (NP (DT no) (NN right))))) (TO to)) (S (NP (NP (DT the) (NN use)) (PP (IN of) (NP (DT the) (NN acronym)))) (VP (@VP (@VP (VBZ explains) (NP (NP (@NP (DT the) (NN udf)) (POS 's)) (NN office))) (, ,)) (S (VP (VBG requiring) (SBAR (IN that) (S (NP (DT the) (NN nc)) (VP (VB remove))))))))) (X (SYM \"))) (X (@X (@X (@X (@X (@X (@X (ADVP (RB immediately)) (NP (@NP (NP (DT any) (NN mention)) (PP (IN of) (NP (@NP (DT the) (NN udf)) (NN nam)))) (PP (IN from) (NP (DT all) (NN material))))) (, ,)) (CC and)) (IN from)) (X (SYM ())) (NP (@NP (@NP (PRP$ their) (NN ))) (NN internet)) (NN site))) (. .))) (X (SYM \"))) (. .)) )"
    #as you are well aware , you have no right to the use of the acronym explains the udf 's office , requiring that the nc remove " immediately any mention of the udf nam from all material , and from ( their ) internet site . " .


    #####sau khi lam lai phan pre-processing
    #cau 17
    str10 = "( (S (@S (NP (@NP (@NP (NP (@NP (DT The) (NNP UDF)) (NN alliance)) (, ,)) (VP (VBN controlled) (PP (IN by) (NP (@NP (@NP (@NP (@NP (NP (@NP (NNP François) (NNP Bayrou)) (POS 's)) (NNP Democratic)) (NNP Movement)) (NN ()) (NNP MoDem)) (NNP )))))) (, ,)) (VP (@VP (@VP (@VP (@VP (@VP (VBD reacted) (PP (IN on) (NP (NNP Friday)))) (PP (TO to) (NP (@NP (NP (DT the) (NN buy)) (: -)) (ADVP (IN out) (NP (NP (NN bid)) (VP (@VP (VBN made) (PP (IN by) (NP (@NP (@NP (NP (NP (@NP (@NP (DT the) (NNP New)) (NNP Centre)) (POS 's)) (NN president)) (, ,)) (NP (NNP Hervé) (NNP Morin))) (, ,)))) (PP (IN for) (NP (NP (DT the) (NN acronym)) (PP (IN of) (NP (@NP (@NP (DT the) (JJ former)) (NNP Giscardian)) (NN party))))))))))) (, ,)) (PP (IN by) (S (VP (@VP (VBG ordering) (NP (PRP him))) (S (RB not) (VP (TO to) (VP (@VP (VB use) (NP (PRP it))) (PP (IN under) (NP (DT any) (NNS circumstances)))))))))) (, ,)) (S (VP (@VP (VBG threatening) (NP (JJ legal) (NN action))) (ADVP (RB otherwise)))))) (. .)) )"

    ##tool thu nghiem

    #t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
    #( (SENT (NP (DET les) (NC chirurgiens) (PP (P de) (NP (NC los) (AP (ADJ angeles))))) (VN (V ont) (V dit)) (Ssub (CS qu') (Sint (VN (CLS ils) (V ï¿½taient)) (ADV outrï¿½s) (PONCT ,) (VN (V a) (VPP dï¿½clarï¿½)) (AP (ADV m) (ADJ camus)))) (PONCT .)))
    #t = Tree.fromstring("")
    #t = Tree.fromstring("( (SENT (NP (DET les) (NC chirurgiens) (PP (P de) (NP (NC los) (AP (ADJ angeles))))) (VN (V ont) (V dit)) (Ssub (CS qu') (Sint (VN (CLS ils) (V ï¿½taient)) (ADV outrï¿½s) (PONCT ,) (VN (V a) (VPP dï¿½clarï¿½)) (AP (ADV m) (ADJ camus)))) (PONCT .)))")
    #t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")

    #preprocessing with output of Berkeley Parser
    line = pre_processing(str10)

    t = Tree.fromstring(line)

    print(t.pos())
    print(t.leaves())
    print(len(t.leaves()))

    #print(t.height())

    # distances to root
    distances = get_list_distance_to_root(t)
    print(distances)
    print("len of distances: %d" %len(distances))

    # constituent labels
    lbl = get_list_constituent_label(t)
    print(lbl)
    print("len of constituent labels: %d" %len(lbl))
    """

    print ('OK')
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#

