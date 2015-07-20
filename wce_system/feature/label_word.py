# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 16:59:10 2015
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

#from feature.common_functions import *
#from config.configuration import *
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import is_existed_file
from common_module.cm_script import call_script, run_chmod
from common_module.cm_util import get_right_content, is_start_with

"""
Buoc 0: Cai dat Terp-a. Thay doi duong dan cai dat Terp_a trong "config_end_user.yml" trong thu muc "input_data"

Buoc 1: chuyen format txt sang format sgml
ref = output of Machine Translation
hyp = post-edition

#lenh nay dung de dua vao code python
#$1: refset or tstset
#$2: input_extension, default = fr
#$3: output_extension, default = en
#$4: raw-text-corpus with format row
#$5: sgml-text-corpus
#perl ${lib_script}/wrap_text_to_sgm.perl $1 $2 $3 $4 $5

#ref set
perl ${lib_script}/wrap_text_to_sgm.perl refset ${input_extension} ${output_extension} tgt-mt-all.en tgt-mt-all.en.sgm

#hypothesis set
perl ${lib_script}/wrap_text_to_sgm.perl tstset ${input_extension} ${output_extension} tgt-pe-all.en tgt-pe-all.en.sgm

Buoc 2: $ bin/terpa -r ../data-10881/10tgt-mt-all.en.sgm -h ../data-10881/10tgt-pe-all.en.sgm --> co normalized trong qua trinh thuc thi terpa
$ bin/terpa_TienLE_TanLE -r ../data-10881/10tgt-mt-all.en.sgm -h ../data-10881/10tgt-pe-all.en.sgm --> ap dung cho cac ngon ngu khac thi ok, neu ap dung cho tieng Anh thi lam Terp-score tang len

Buoc 3: Trich du lieu can thiet trong result of terp-a & Xoa cac file khong dung nua
--> dung ham "def create_script_temp(command_lines)" line 1139 trong file "common_functions.py" & ref 1171, 1249 ve cach dung script_temp

rm -rf terp.*
rm -rf TienNLe_TanNLe_system.*.*

--> def delete_all_files_temporary_terpa() line 1275

"""
#**************************************************************************#
def convert_format_txt_to_sgml(file_input_path, file_output_type, input_extension, output_extension, file_output_path):
    """
    Converting format text to format sgml with two type: refset & tstset

    :type file_input_path: string
    :param file_input_path: contains corpus with format row.

    :type file_output_type: string
    :param file_output_type: refset OR tstset

    :type input_extension: string
    :param input_extension: en/fr/es/...

    :type output_extension: string
    :param output_extension: en/fr/es/...

    :type file_output_path: string
    :param file_output_path: contains corpus with format sgml

    :raise ValueError: if any path is not existed
    """

    """
    Buoc 1: chuyen format txt sang format sgml
    ref = output of Machine Translation
    hyp = post-edition

    #lenh nay dung de dua vao code python
    #$1: refset or tstset
    #$2: input_extension, default = fr
    #$3: output_extension, default = en
    #$4: raw-text-corpus with format row
    #$5: sgml-text-corpus
    #perl ${lib_script}/wrap_text_to_sgm.perl $1 $2 $3 $4 $5

    #ref set
    perl ${lib_script}/wrap_text_to_sgm.perl refset ${input_extension} ${output_extension} tgt-mt-all.en tgt-mt-all.en.sgm

    #hypothesis set
    perl ${lib_script}/wrap_text_to_sgm.perl tstset ${input_extension} ${output_extension} tgt-pe-all.en tgt-pe-all.en.sgm
    """
    #self.LANGUAGE_ENGLISH = "en"
    #self.LANGUAGE_FRENCH = "fr"
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file input')
    """
    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    current_config = load_configuration()

    command_line = "perl " #Path to the shell script in Tools lib
    script_path = current_config.TOOL_WRAP_TEXT_TO_SGM

    command_line = command_line + script_path + " " + file_output_type + " " + input_extension + " " + output_extension + " " + file_input_path + " " + file_output_path

    call_script(command_line, script_path)
#**************************************************************************#

#**************************************************************************#
def get_output_terplus(file_hypythesis_path, file_reference_path, input_extension, output_extension):
    """
    Getting the output using tool Ter_Plus (terpa). The result path is file "terp.pra" in folder "output_path"

    :type file_hypythesis_path: string
    :param file_hypythesis_path: path of hypothesis file

    :type file_reference_path: string
    :param file_reference_path: path of reference file

    :type input_extension: string
    :param input_extension: input extension = en/fr/es/ar/...

    :type output_extension: string
    :param output_extension: output extension = en/fr/es/ar/...

    :raise ValueError: if any path is not existed
    """
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #convert_format_txt_to_sgml(file_input_path, file_output_type, input_extension, output_extension, file_output_path)
    #current_config.HYPOTHESIS_SET_SGM
    convert_format_txt_to_sgml(file_hypythesis_path, current_config.HYPOTHESIS_SET, input_extension,  output_extension, current_config.HYPOTHESIS_SET_SGM)

    #current_config.POST_EDITION_SGM
    convert_format_txt_to_sgml(file_reference_path, current_config.POST_EDITION_SET, input_extension,  output_extension, current_config.POST_EDITION_SGM)

    #Buoc 0: Thay the cac chuoi dac biet lam cho terpa khong the chay duoc
    #<unk> thanh unk
    #<UNK> thanh unk
    customize_input_before_using_terpa_format_row( current_config.HYPOTHESIS_SET_SGM, current_config.HYPOTHESIS_SET_SGM)
    customize_input_before_using_terpa_format_row( current_config.POST_EDITION_SGM, current_config.POST_EDITION_SGM)

    #print("tam thoi ok")


    #command_line = current_config.TOOL_TERPA #Path to the terpa Tool
    command_line = config_end_user.TOOL_TERPA #Path to the terpa Tool

    #run_chmod(current_config.TOOL_TERPA)
    run_chmod(config_end_user.TOOL_TERPA)

    command_line = command_line + " -h " + current_config.HYPOTHESIS_SET_SGM + " -r " + current_config.POST_EDITION_SGM
    script_path = current_config.SCRIPT_TEMP #path contains output of tool terpa

    print(command_line)
    call_script(command_line, script_path)

#**************************************************************************#
def get_output_terplus_no_shift_cost(file_hypythesis_path, file_reference_path, input_extension, output_extension):
    """
    Getting the output using tool Ter_Plus (terpa). The result path is file "terp.pra" in folder "output_path"

    :type file_hypythesis_path: string
    :param file_hypythesis_path: path of hypothesis file

    :type file_reference_path: string
    :param file_reference_path: path of reference file

    :type input_extension: string
    :param input_extension: input extension = en/fr/es/ar/...

    :type output_extension: string
    :param output_extension: output extension = en/fr/es/ar/...

    :raise ValueError: if any path is not existed
    """
    current_config = load_configuration()

    #convert_format_txt_to_sgml(file_input_path, file_output_type, input_extension, output_extension, file_output_path)
    #current_config.HYPOTHESIS_SET_SGM
    convert_format_txt_to_sgml(file_hypythesis_path, current_config.HYPOTHESIS_SET, input_extension,  output_extension, current_config.HYPOTHESIS_SET_SGM)

    #current_config.POST_EDITION_SGM
    convert_format_txt_to_sgml(file_reference_path, current_config.POST_EDITION_SET, input_extension,  output_extension, current_config.POST_EDITION_SGM)

    command_line = current_config.TOOL_TERPA_NO_SHIFT_COST #Path to the terpa Tool

    run_chmod(current_config.TOOL_TERPA_NO_SHIFT_COST)

    command_line = command_line + " -h " + current_config.HYPOTHESIS_SET_SGM + " -r " + current_config.POST_EDITION_SGM
    script_path = current_config.SCRIPT_TEMP #path contains output of tool terpa

    #print(command_line)
    call_script(command_line, script_path)
#**************************************************************************#
def get_output_terplus_within_tokenizing(file_hypythesis_path, file_reference_path, input_extension, output_extension):
    """
    After tokenizing hypothesis and then getting the output using tool Ter_Plus (terpa). The result path is file "terp.pra" in folder "output_path"

    :type file_hypythesis_path: string
    :param file_hypythesis_path: path of hypothesis file

    :type file_reference_path: string
    :param file_reference_path: path of reference file

    :type input_extension: string
    :param input_extension: input extension = en/fr/es/ar/...

    :type output_extension: string
    :param output_extension: output extension = en/fr/es/ar/...

    :raise ValueError: if any path is not existed
    """
    current_config = load_configuration()

    #convert_format_txt_to_sgml(file_input_path, file_output_type, input_extension, output_extension, file_output_path)
    #current_config.HYPOTHESIS_SET_SGM
    convert_format_txt_to_sgml( file_hypythesis_path, current_config.HYPOTHESIS_SET, input_extension, output_extension, current_config.HYPOTHESIS_SET_SGM)

    #current_config.POST_EDITION_SGM
    convert_format_txt_to_sgml( file_reference_path, current_config.POST_EDITION_SET, input_extension, output_extension, current_config.POST_EDITION_SGM)


    command_line = current_config.TOOL_TERPA_WITHIN_TOKENIZING #Path to the terpa Tool

    run_chmod(current_config.TOOL_TERPA_WITHIN_TOKENIZING)

    command_line = command_line + " -h " + current_config.HYPOTHESIS_SET_SGM + " -r " + current_config.POST_EDITION_SGM
    script_path = current_config.SCRIPT_TEMP #path contains output of tool terpa

    #print(command_line)
    call_script(command_line, script_path)
#**************************************************************************#
class Sentence_Terpa(object):
    """ Contains content of each sentence in output terp_a

    Example:
    -----------------
    Sentence ID: [TienLe_TanLe][Tien_Tan_system][TienNgocLe_TanNgocLe][4]
    Original Reference: i have heard about a possible legal action to come , he said .
    Original Hypothesis: i have heard about a possible legal procedures to come , a-t-il said .
    Reference: i have heard about a possible legal action to come , he said .
    Hypothesis: i have heard about a possible legal procedures to come , a-t-il said .
    Hypothesis After Shift: i have heard about a possible legal procedures to come , a-t-il said .
    Alignment1: (       P  S  )
    Alignment2: (EEEEEEEPPESEE)
    HypErrs: 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,289 0,289 0,000 0,000 1,557 0,000 0,000
    OtherErr: 0,000
    HypLocMap: 0 1 2 3 4 5 6 7 8 9 10 11 12 13
    NumShifts: 0
    Num Phrase Substitutions: 1
      NewCost: 0.5788883856766118 OrigCost: 0.004606 <p>action to</p> <p>procedures to</p>
    Score: 0,153 (2,135 / 14,000)
    """
    original_reference = ""
    original_hypothesis = ""
    reference = ""
    hypothesis = ""
    hypothesis_after_shift = ""
    alignment = ""
    hypothesis_errors = ""
    hypothesis_location_map = ""
    num_shifts = ""
    num_phrase_substitutions = ""
    new_cost = []
    score = ""

    def __init__(self):
        self.original_reference = ""
        self.original_hypothesis = ""
        self.reference = ""
        self.hypothesis = ""
        self.hypothesis_after_shift = ""
        self.alignment = ""
        self.hypothesis_errors = ""
        self.hypothesis_location_map = ""
        self.num_shifts = ""
        self.num_phrase_substitutions = ""
        self.new_cost = []
        self.score = ""

    def __init__(self, original_reference, original_hypothesis, reference, hypothesis, hypothesis_after_shift, alignment, hypothesis_errors, hypothesis_location_map, num_shifts, num_phrase_substitutions, new_cost, score):
        self.original_reference = original_reference
        self.original_hypothesis = original_hypothesis
        self.reference = reference
        self.hypothesis = hypothesis
        self.hypothesis_after_shift = hypothesis_after_shift
        self.alignment = alignment
        self.hypothesis_errors = hypothesis_errors
        self.hypothesis_location_map = hypothesis_location_map
        self.num_shifts = num_shifts
        self.num_phrase_substitutions = num_phrase_substitutions
        self.score = score

        #self.new_cost = new_cost
        self.new_cost = []
        if len(new_cost) != 0:
            for item in new_cost:
                self.new_cost.append(item)

    #set
    def set_original_reference(self, original_reference=""):
        self.original_reference = original_reference

    def set_original_hypothesis(self, original_hypothesis=""):
        self.original_hypothesis = original_hypothesis

    def set_reference(self, reference=""):
        self.reference = reference

    def set_hypothesis(self, hypothesis=""):
        self.hypothesis = hypothesis

    def set_hypothesis_after_shift(self, hypothesis_after_shift=""):
        self.hypothesis_after_shift = hypothesis_after_shift

    def set_alignment(self, alignment=""):
        self.alignment = alignment

    def set_hypothesis_errors(self, hypothesis_errors=""):
        self.hypothesis_errors = hypothesis_errors

    def set_hypothesis_location_map(self, hypothesis_location_map=""):
        self.hypothesis_location_map = hypothesis_location_map

    def set_num_shifts(self, num_shifts=""):
        self.num_shifts = num_shifts

    def set_num_phrase_substitutions(self, num_phrase_substitutions=""):
        self.num_phrase_substitutions = num_phrase_substitutions

    def set_new_cost(self, new_cost=[]):
        #self.new_cost = new_cost
        self.new_cost = []
        if len(new_cost) != 0:
            for item in new_cost:
                self.new_cost.append(item)

    def set_score(self, score=""):
        self.score = score

    #get
    def get_original_reference(self):
        return self.original_reference

    def get_original_hypothesis(self):
        return self.original_hypothesis

    def get_reference(self):
        return self.reference

    def get_hypothesis(self):
        return self.hypothesis

    def get_hypothesis_after_shift(self):
        return self.hypothesis_after_shift

    def get_alignment(self):
        return self.alignment

    def get_hypothesis_errors(self):
        return self.hypothesis_errors

    def get_hypothesis_location_map(self):
        return self.hypothesis_location_map

    def get_num_shifts(self):
        return self.num_shifts

    def get_num_phrase_substitutions(self):
        return self.num_phrase_substitutions

    def get_new_cost(self):
        return self.new_cost

    def get_score(self):
        return self.score

#**************************************************************************#
def get_list_sentences_terpa(file_input_path):
    """
    :type file_input_path: string
    :param file_input_path: contains output of tool terpa

    :raise ValueError: if any path is not existed
    """
    #check existed path
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output of tool terpa')
    """
    str_message_if_not_existed = "Not Existed file output of tool Terpa"
    is_existed_file(file_input_path, str_message_if_not_existed)

    result = []

    #open file:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')

    """
    Sentence ID: [TienLe_TanLe][Tien_Tan_system][TienNgocLe_TanNgocLe][5]
    Original Reference: but he is also a doctor with a dodgy reputation , who was repeatedly condemned by the justice system in medical liability cases , as well as for tax fraud and swindling .
    Original Hypothesis: but it is also a doctor the reputation sulfureuse , repeatedly condemned by the courts in cases in medical liability as well as tax fraud and deception .
    Reference: but he is also a doctor with a dodgy reputation , who was repeatedly condemned by the justice system in medical liability cases , as well as for tax fraud and swindling .
    Hypothesis: but it is also a doctor the reputation sulfureuse , repeatedly condemned by the courts in cases in medical liability as well as tax fraud and deception .
    Hypothesis After Shift: but it is also a doctor the reputation sulfureuse , repeatedly condemned by the courts in in medical liability cases as well as tax fraud and deception .
    Alignment: (ESEEEEDDSEIEDDEEEEPSEEEEDEEEDEEEPE)
    HypErrs: 0,000 1,557 0,000 0,000 0,000 0,000 1,557 0,000 0,259 0,000 0,000 0,000 0,000 0,000 0,456 1,557 0,562 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,491 0,000
    OtherErr: 8,562
    HypLocMap: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 18 19 16 20 21 22 23 24 25 26 27
    NumShifts: 1
      [16, 16, 22/19] (cases) -> (cases)
    Num Phrase Substitutions: 2
      NewCost: 0.4557247063398646 OrigCost: 0.015699 <p>justice</p> <p>courts</p>
      NewCost: 0.49066675393177217 OrigCost: 0.011106 <p>swindling</p> <p>deception</p>
    Score: 0,455 (14,999 / 33,000)
    """

    #str_sentence_id = "Sentence ID:"
    str_original_reference = "Original Reference:"
    str_original_hypothesis = "Original Hypothesis:"
    str_reference = "Reference:"
    str_hypothesis = "Hypothesis:"
    str_hypothesis_after_shift = "Hypothesis After Shift:"
    str_alignment = "Alignment:"
    str_hyperrs = "HypErrs:"
    str_hyp_loc_map = "HypLocMap:"
    str_num_shifts = "NumShifts:"
    str_num_phrase_substitutions = "Num Phrase Substitutions:"
    str_new_cost = "NewCost:"
    str_score = "Score:"

    #val_sentence_id = ""
    val_original_reference = ""
    val_original_hypothesis = ""
    val_reference = ""
    val_hypothesis = ""
    val_hypothesis_after_shift = ""
    val_alignment = ""
    val_hyperrs = ""
    val_hyp_loc_map = ""
    val_num_shifts = ""
    val_num_phrase_substitutions = ""
    val_new_cost = []
    val_score = ""

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

        #is_start_with(string_parent, substring)

        #neu bat dau bang "str_score" thi het 1 cau
        #lay du lieu score --> dua cac du lieu vao trong doi tuong "Sentence_Terpa" va them vao list cac object

        #Score
        if is_start_with(line, str_score):
            val_score = get_right_content(line, str_score)

            #dua du lieu vao danh sach ket qua
            result.append(Sentence_Terpa(val_original_reference, val_original_hypothesis, val_reference, val_hypothesis, val_hypothesis_after_shift, val_alignment, val_hyperrs, val_hyp_loc_map, val_num_shifts, val_num_phrase_substitutions, val_new_cost, val_score))
        #end if

        #nguoc lai, tuy moi phan bat dau ma dua vao cac du lieu tuong ung
        #get_right_content(line, start_by_string)
        """
        str_sentence_id = "Sentence ID:"
        str_original_reference = "Original Reference:"
        str_original_hypothesis = "Original Hypothesis:"
        str_reference = "Reference:"
        str_hypothesis = "Hypothesis:"
        str_hypothesis_after_shift = "Hypothesis After Shift:"
        str_alignment = "Alignment:"
        str_hyperrs = "HypErrs:"
        str_hyp_loc_map = "HypLocMap:"
        str_num_shifts = "NumShifts:"
        str_num_phrase_substitutions = "Num Phrase Substitutions:"
        str_new_cost = "NewCost:"
        str_score = "Score:"
        """

        #str_sentence_id
        #if is_start_with(line, str_sentence_id):
        #    val_sentence_id = get_right_content(line, str_sentence_id)

        #str_original_reference
        if is_start_with(line, str_original_reference):
            val_original_reference = get_right_content(line, str_original_reference)
        #end if

        #str_original_hypothesis
        if is_start_with(line, str_original_hypothesis):
            val_original_hypothesis = get_right_content(line, str_original_hypothesis)

        #str_reference
        if is_start_with(line, str_reference):
            val_reference = get_right_content(line, str_reference)

        #str_hypothesis
        if is_start_with(line, str_hypothesis):
            val_hypothesis = get_right_content(line, str_hypothesis)

        #str_hypothesis_after_shift
        if is_start_with(line, str_hypothesis_after_shift):
            val_hypothesis_after_shift = get_right_content(line, str_hypothesis_after_shift)

        #str_alignment
        if is_start_with(line, str_alignment):
            val_alignment = get_right_content(line, str_alignment)

        #str_hyperrs
        if is_start_with(line, str_hyperrs):
            val_hyperrs = get_right_content(line, str_hyperrs)

        #str_hyp_loc_map
        if is_start_with(line, str_hyp_loc_map):
            val_hyp_loc_map = get_right_content(line, str_hyp_loc_map)

        #str_num_shifts
        if is_start_with(line, str_num_shifts):
            val_num_shifts = get_right_content(line, str_num_shifts)

        #str_num_phrase_substitutions
        if is_start_with(line, str_num_phrase_substitutions):
            val_num_phrase_substitutions = get_right_content(line, str_num_phrase_substitutions)

        #str_new_cost
        if is_start_with(line, str_new_cost):
            val_new_cost.append(get_right_content(line, str_new_cost))

    #end for

    #close file
    file_reader.close()

    return result

#**************************************************************************#
def extracting_corresponding_label_format_column(list_sentences_terpa, file_output_path):
    """
    Extracting label of word within format column

    :type list_sentences_terpa: list
    :param list_sentences_terpa: list of object Sentences_Terpa

    :type file_output_path: string
    :param file_output_path: path of result

    :raise ValueError: if any path is not existed
    """

    if len(list_sentences_terpa) == 0:
        raise Exception("You should check output of terpa. We can not see the file output.")

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    for sent in list_sentences_terpa:
        #get_hypothesis_errors(self):
        str_hypothesis_error = sent.get_hypothesis_errors()

        for item in str_hypothesis_error.split():
            #.replace(',', ':')
            #ValueError: could not convert string to float: '0,259'
            item = item.replace(",", ".")

            #chuyen tu string sang so thuc
            word_err = float(item)

            if word_err > 0: #using edit-method
                file_writer.write("B") #Bad
            else:
                file_writer.write("G") #Good
            #end if

            #add empty line
            file_writer.write("\n")
        #end for

        #add empty line
        file_writer.write("\n")
    #end for

    #close file
    file_writer.close()
#**************************************************************************#
#replace "<UNK>" --> "unk" trong format dong
def customize_input_before_using_terpa_format_row(file_input_path, file_output_path):
    """
    Getting output from TreeTagger with format row

    :type file_input_path: string
    :param file_input_path: contains raw corpus with format ROW.

    :type file_output_path: string
    :param file_output_path: contains corpus after normalizing punctuation and tokenizing

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format - column')
    """
    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    current_config = load_configuration()

    script_path = current_config.CUSTOMIZE_INPUT_BEFORE_USING_TERPA

    run_chmod(script_path)

    command_line = "sh " + script_path + " " + file_input_path + " " + file_output_path

    #print(command_line)
    call_script(command_line, script_path)
#**************************************************************************#
"""
Buoc: Trich du lieu can thiet trong result of terp-a
"""
def extracting_label_for_word_format_column(file_hypythesis_path, file_reference_path, input_extension, output_extension, file_output_path):
    """
    Extracting label for word format column and each sentence separates by an empty line

    :type file_hypythesis_path: list
    :param file_hypythesis_path: path of hypothesis file

    :type file_reference_path: string
    :param file_reference_path: path of reference file

    :type input_extension: string
    :param input_extension: en/fr/es/...

    :type output_extension: string
    :param output_extension: en/fr/es/...

    :type file_output_path: string
    :param file_output_path: path of file that contains label of word with format column; each "sentence" separates by an empty line

    :raise ValueError: if any path is not existed
    """

    #Buoc 0: Thay the cac chuoi dac biet lam cho terpa khong the chay duoc
    #<unk> thanh unk
    #<UNK> thanh unk

    #Buoc 1: Lay ket qua cua terp_a
    #cach 1: khong can tokenize
    get_output_terplus(file_hypythesis_path, file_reference_path, input_extension, output_extension)

    #cach 2; chua bo sung Buoc 0
    #get_output_terplus_no_shift_cost(file_hypythesis_path, file_reference_path, input_extension, output_extension)

    #cach 3 : within tokenizing; chua bo sung Buoc 0
    #get_output_terplus_within_tokenizing(file_hypythesis_path, file_reference_path, input_extension, output_extension)

    #Buoc 2: Lay cau truc tung cau dua vao trong danh sach cac doi tuong "Sentence_Terpa"
    current_config = load_configuration()
    list_sentences = get_list_sentences_terpa(current_config.TERP_PRA)
    print(current_config.TERP_PRA)
    """
    #for verifying old output Terpa "Labels-MT"
    #TERP_PRA_FROM_WCE_SLT_LIG
    current_config = load_configuration()
    list_sentences = get_list_sentences_terpa(current_config.TERP_PRA_FROM_WCE_SLT_LIG)
    """
    #Trich nhung thong tin phu hop de ghi vao output file
    extracting_corresponding_label_format_column(list_sentences, file_output_path)

    #Buoc 3: xoa file khong can thiet ~ output from tool terpa
    #delete_all_files_temporary_terpa()

#**************************************************************************#
""" --> Da cai dat trong "common_functions.py"
*** Xoa cac file khong dung nua
--> dung ham "def create_script_temp(command_lines)" line 1139 trong file "common_functions.py" & ref 1171, 1249 ve cach dung script_temp

rm -rf terp.*
rm -rf TienNLe_TanNLe_system.*.*

--> def delete_all_files_temporary_terpa() line 1275
"""
#**************************************************************************#
"""Bi lech, do w. --> w . --> cau hoi: Lam cach nao de Terpa khong tokenize nua ???
--> thay doi lai tham so:
-N
    Normalize and Tokenize ref and hyp

--> Normalize (boolean) 	BOOLEAN 	FALSE 	-N (sets to TRUE) 	Enables tokenization on the source and target input files and is recommended unless your input is pre-tokenized. This tokenization is meant to parallel the tokenization done in the mteval-0.6b.pl program, although slight differences exist.

ref: http://www.umiacs.umd.edu/~snover/terp/doc_v1.html

Sentence ID: [TienLe_TanLe][Tien_Tan_system][TienNgocLe_TanNgocLe][61]
Original Reference: Although President George W. Bush apologized twice for the deaths of two girls, demand continued to grow for modification of the agreement on the status of the armed forces (Status of Force Agreement, SOFA) which governs the legal treatment reserved for American troops stationed in South Korea.
Original Hypothesis: although president George W. Bush has apologised to two times for the deaths of two girls , the continued to accumulate for amending the agreement on the status of the armed forces ( Status of Force Agreement , SOFA ) , which governs the treatment legal reserved for american troops stationed in Corée of Sud .
Reference: although president george w . bush apologized twice for the deaths of two girls , demand continued to grow for modification of the agreement on the status of the armed forces ( status of force agreement , sofa ) which governs the legal treatment reserved for american troops stationed in south korea .
Hypothesis: although president george w . bush has apologised to two times for the deaths of two girls , the continued to accumulate for amending the agreement on the status of the armed forces ( status of force agreement , sofa ) , which governs the treatment legal reserved for american troops stationed in corée of sud .
Hypothesis After Shift: although president george w . bush has apologised to two times for the deaths of two girls , the continued to accumulate for amending the agreement on the status of the armed forces ( status of force agreement , sofa ) , which governs the legal treatment reserved for american troops stationed in corée of sud .
Alignment: (      IYIP       S  S P                 I           SSI )
HypErrs: 0,000 0,000 0,000 0,000 0,000 0,000 0,259 0,000 0,259 0,229 0,229 0,000 0,000 0,000 0,000 0,000 0,000 0,000 1,557 0,000 0,000 1,557 0,000 1,302 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,000 0,259 0,000 0,000 0,000 0,000 0,562 0,000 0,000 0,000 0,000 0,000 0,000 1,557 1,557 0,259 0,000
OtherErr: 0,000
HypLocMap: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 46 45 47 48 49 50 51 52 53 54 55 56

NumShifts: 1
  [46, 46, 42/44] (legal) -> (legal)
Num Phrase Substitutions: 2
  NewCost: 0.45759683456907074 OrigCost: 0.04015 <p>twice</p> <p>two times</p>
  NewCost: 1.3020756374010238 OrigCost: 0.005085 <p>modification of</p> <p>amending</p>

Score: 0,181 (9,583 / 53,000)
"""
#**************************************************************************#
#**************************************************************************#
def extracting_given_label(file_tags_path, file_output_path):
    """
    Extracting label for word format column and each sentence separates by an empty line

    :type file_tags_path: list
    :param file_tags_path: path of tags file within format-row. For example: OK BAD OK OK OK

    :type file_output_path: string
    :param file_output_path: path of file that contains label of word with format column; each "sentence" separates by an empty line

    :raise ValueError: if any path is not existed
    """

    #check existed paths
    """
    if not os.path.exists(file_tags_path):
        raise TypeError('Not Existed tags-file within format-row')
    """
    str_message_if_not_existed = "Not Existed tag-file input"
    is_existed_file(file_tags_path, str_message_if_not_existed)

    #open file:
    #for reading: file_input_path
    file_reader = open(file_tags_path, mode = 'r', encoding = 'utf-8')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    """
    OK OK OK OK OK OK OK OK OK OK
    OK BAD BAD BAD BAD OK OK OK BAD OK OK OK OK
    """
    current_config = load_configuration()
    good_label = current_config.LABEL_GOOD
    bad_label = current_config.LABEL_BAD
    str_good = "OK"
    str_bad = "BAD"

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
        #end if

        items = line.split()
        for item in items:
            item = item.strip()
            if item == str_good:
                file_writer.write(good_label)
            elif item == str_bad:
                file_writer.write(bad_label)
            #end if

            file_writer.write('\n')
        #end for

        file_writer.write('\n')
    #end for

    #close 2 files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
if __name__ == "__main__":
    #Test case:

    current_config = load_configuration()
    config_end_user = load_config_end_user()

    #extracting_given_label(file_tags_path, file_output_path)
    """extracting_given_label(config_end_user.TAGS_FILE_PATH, current_config.LABEL_OUTPUT)"""

    #normal command
    #extracting_label_for_word_format_column( current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT)

    #checking_moses_2009
    #config: model
    #extracting_label_for_word_format_column(current_config.TRANSLATED_MODEL_NO_INCLUDED_ALIGNMENT, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING_CHECKING_MOSES_2009, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT)

    #config: output10881
    #extracting_label_for_word_format_column(current_config.TRANSLATED_OUTPUT10881_NO_INCLUDED_ALIGNMENT, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING_CHECKING_MOSES_2009, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT)

    #TARGET_MT_ALL_FORMAT_ROW
    #note: file nay copy tu 'WCE-SLT-LIG-master' vao thu muc 'extracted_features'
    #extracting_label_for_word_format_column(current_config.TARGET_MT_ALL_FORMAT_ROW, current_config.POST_EDITION_OF_MACHINE_TRANSLATION_SENTENCES_TARGET_LANGUAGE, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT)

    extracting_label_for_word_format_column(current_config.TARGET_REF_TEST_FORMAT_ROW, current_config.POST_EDITION_AFTER_TOKENIZING_LOWERCASING, current_config.LANGUAGE_FRENCH, current_config.LANGUAGE_ENGLISH, current_config.LABEL_OUTPUT)

    """10881 FR-EN
    Total TER: 0,48 (120847,98 / 251410,00)
    """

    print ('OK')
