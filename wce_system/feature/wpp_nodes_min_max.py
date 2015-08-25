# -*- coding: utf-8 -*-

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

"""
Created on Tue Dec 23 14:30:00 2014

*** can built lai SRILM vi bi loi roi
/home/lent/Develops/Solution/eval_agent/eval_agent/feature/../lib/shell_script/nbestToLattice.sh: line 22: /home/tienle/Documents/Develops/DevTools/srilm/bin/i686-m64/nbest-lattice: No such file or directory
/home/lent/Develops/Solution/eval_agent/eval_agent/feature/../lib/shell_script/nbestToLattice.sh: line 23: /home/tienle/Documents/Develops/DevTools/srilm/bin/i686-m64/wlat-to-pfsg: No such file or directory
/home/lent/Develops/Solution/eval_agent/eval_agent/feature/../lib/shell_script/nbestToLattice.sh: line 24: /home/tienle/Documents/Develops/DevTools/srilm/bin/i686-m64/lattice-tool: No such file or directory
head: cannot open 'Phrase880' for reading: No such file or directory

/home/lent/Develops/Solution/eval_agent/eval_agent/feature/../lib/shell_script/nbestToLattice.sh 881
"""

#Purpose: Extracting the following features: WPP any, Nodes, Min, Max

"""
#Xac dinh WPP, Nodes, Min, Max trong Confusion Network
B0: chuan bi input voi 5 (cau) X 1000 = 5000 dong dau tien. Vi day la file trich tu
1000-bestList from MOSES

B1: Cat tung files chua tu file NBest-List dua vao ID
~GeTools/WPP-Nodes-Min-Max$ chmod +x split_Nbest.sh
~GeTools/WPP-Nodes-Min-Max$ ./split_Nbest.sh 5sentences-aligned-1000bestlists

B2:

B2.1.

$copy fastnc vao thu muc (Trong Experiment nay, fastnc de trong thu muc /home/tienle/Documents/Develops/GeTools/WPP-Nodes-Min-Max/fastnc/)
$chmod +x fastnc (trong thu muc fastnc/bin)
$chmod +x *.pl (cac file perl trong fastnc/scripts)

Chu y: Muon xoa cac file trong thu muc dung lenh: $rm Phrase*

*** Chu y: Co the dung file 'sua.sh' trong data/backup.homere/home/nluong/ForLuong/Sentenses-FinalWMT13/sua.sh
de thay doi cau truc trong 1 dong cua Phrase* truoc khi lam buoc 2.2 ***

B2.2. Copy tat ca cac file Phrase* co duoc tu B1 sang thu muc chua file 'nbestToLattice.sh'
$cp SentenceSet/Phrase* .

B3:
3.1: Chinh trong code 'nbestToLattice.sh': voi so dong se xu ly (Chu y: khong lay
phan nhan voi he so 1000BestList, ma chi lay so cau N khac nhau trong PhraseN); Ngoai ra, PHAI cap nhat PATH den SRILM va FASTNC trong file 'nBestToLattice.sh'

3.2. ~GeTools/WPP-Nodes-Min-Max$ ./nbestToLattice.sh

3.3. Sau khi chay xong dong lenh --> Ket qua o file: 'Results.txt'

Chu y: De xoa cac file trung gian va file Phrase* ban dau --> $rm Phrase*

Chu y: Neu file Results.txt rong thi xoa tat ca cac file da sinh ra va Goto B2

*** Results.txt co cau truc nhu sau:
* Chu y: a	0.51267 --> so 0.51267 chinh la WPP cua tu 'a'

Phrase0 1 0.00 1.00 yet 0.18901
Phrase0 1 1.00 3.00 a 0.51267
Phrase0 1 5.00 1.00 step 0.58710
Phrase0 1 6.00 4.00 the 1.00000
Phrase0 1 10.00 2.00 balkans 0.82912
Phrase0 1 12.00 2.00 !NULL 1.00000
a	0.51267 ( time=0 nodes=5 min=0.03497 max=0.51267 mean=0.20000 var=0.13312 svar=0.36486 )
crucial	0.15303 ( time=100 nodes=5 min=0.07066 max=0.34638 mean=0.20000 var=0.05109 svar=0.22602 )
step	0.58710 ( time=200 nodes=5 min=0.04761 max=0.58710 mean=0.20000 var=0.19684 svar=0.44367 )
for	0.25190 ( time=300 nodes=4 min=0.01560 max=0.44813 mean=0.25000 var=0.09539 svar=0.30885 )
the	1.00000 ( time=400 nodes=1 min=1.00000 max=1.00000 mean=1.00000 var=0.00000 svar=0.00000 )
balkans	0.82912 ( time=500 nodes=2 min=0.17088 max=0.82912 mean=0.50000 var=0.21664 svar=0.46544 )
Phrase1 1 0.00 1.00 since 1.00000
..........

B4: Lay cac thong tin can thiet tu file Results.txt nhu WPP, NODES, MIN, MAX
Chu y: WPP = 1 --> co nghia la: tat ca cac cau trong nBestList deu chua tu nay

Chu y: WPP = 0.00001 --> co nghia la: Ton tai it nhat 1 cau chua tu nay trong nBestList --> Tu nay co khi dich KHONG DUOC TOT

~GeTools/WPP-Nodes-Min-Max$ ./buildWPP_nodes_min_max_file.sh Results.txt final_Result_5features.txt

B5: chuan hoa cac thong so ve he so 10 hay 100
Chu y: Neu lam bang java thi phai update code va javac. Neu khong thi dung file
Shell.
~GeTools/WPP-Nodes-Min-Max$ ./round_WPP.sh final_Result_5features.txt final_Result_5features-Normalisation10-2.txt

*** Chu y: Neu muon chuyen sang he so 100 thi can phai cap nhat them trong CODE.
"""

"""
Tom lai:
* Buoc 0:
+ Xoa tat ca cac files trong thu muc SentenceSet.
Chu y: Muon xoa cac file trong thu muc dung lenh: $rm Phrase*

* Buoc 1:
+ Duyet tat ca cac dong trong n-best-list
+ Dua thong tin cua cac cau gom: ... vao cac file co ID tuong ung

*** Chu y: Co the dung file 'sua.sh' trong data/backup.homere/home/nluong/ForLuong/Sentenses-FinalWMT13/sua.sh
de thay doi cau truc trong 1 dong cua Phrase* truoc khi lam buoc 2 ***

* Buoc 2: Copy tat ca cac file Phrase* co duoc tu B1 sang thu muc chua file 'nbestToLattice.sh'
$cp SentenceSet/Phrase* .
$copy fastnc vao thu muc (Trong Experiment nay, fastnc de trong thu muc /home/tienle/Documents/Develops/GeTools/WPP-Nodes-Min-Max/fastnc/)
$chmod +x fastnc (trong thu muc fastnc/bin)
$chmod +x *.pl (cac file perl trong fastnc/scripts)
#../../../tool/fastnc/scripts/RefToCtm.pl
#../../../tool/fastnc/bin/fastnc

B3:
3.1: Chinh trong code 'nbestToLattice.sh': voi so dong se xu ly (Chu y: khong lay
phan nhan voi he so 1000BestList, ma chi lay so cau N khac nhau trong PhraseN); Ngoai ra, PHAI cap nhat PATH den SRILM va FASTNC trong file 'nBestToLattice.sh' --> nen viet ham xu ly replace trong giai doan "pre-processing"

3.2. ~GeTools/WPP-Nodes-Min-Max$ ./nbestToLattice.sh

3.3. Sau khi chay xong dong lenh --> Ket qua o file: 'Results.txt'

Chu y: Neu file Results.txt rong thi xoa tat ca cac file da sinh ra va Goto B2
"""

import os
import sys
import threading
import time

#for call shell script
#import shlex, subprocess

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

"""
from feature.common_functions import *
from config.config_end_user import *
from config.configuration import *
"""
from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import is_existed_file, delete_all_files_temporary
from common_module.cm_script import call_script, run_chmod
from common_module.cm_util import  is_in_string, get_str_value_given_key, print_time

#**************************************************************************#
def preprocessing_for_extracting():
    """
    + Deleting all files Phrase* in directory that contains code "nbestToLattice.sh"
    + Change mode execute for 2 files for fastnc & "nbestToLattice.sh"
    """

    """Deleting all files Phrase* in directory that contains code nbestToLattice.sh"""
    #self.TOOL_N_BEST_TO_LATTICE
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    """
    #using tool MOSES in order to generate n-best-list
    #path_script = current_config.TOOL_N_BEST_TO_LATTICE #Path to the TOOL_N_BEST_TO_LATTICE Tool

    #change mode execute script
    #run_chmod(path_script)

    command_line = " rm -rf Phrase*"

    #print(command_line)

    #generate shell script, roi goi lenh chay script
    #generate shell script
    list_of_commands = []

    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #goi lenh chay
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
    """

    #delete all file "Phrase*" --> moved to common_functions
    delete_all_files_temporary()

    #change quyen execute cho tool TOOL_N_BEST_TO_LATTICE & fastnc
    run_chmod(current_config.TOOL_N_BEST_TO_LATTICE)
    #run_chmod(current_config.TOOL_FASTNC)
    #run_chmod(current_config.TOOL_REFTOCTM)
    run_chmod(config_end_user.TOOL_FASTNC)
    run_chmod(config_end_user.TOOL_REFTOCTM)

#**************************************************************************#
#* Buoc 1:
#+ Duyet tat ca cac dong trong n-best-list
#+ Dua thong tin cua cac cau gom: ... vao cac file co ID tuong ung
def split_sentences_with_id(file_input_path, output_path):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type output_path: string
    :param output_path: contains path to script "nbestToLattice.sh"

    :rtype: the number of sentences in n-best-list. Default = 1000

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output from TreeTagger')
    """
    str_message_if_not_existed = "Not Existed file corpus input that is output from TreeTagger"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    delimiter = "|||"
    number_of_sentences = 0

    """MOSES >= 2013
0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15

0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , declared m camus .  ||| LexicalReordering0= -2.31489 0 0 -1.80126 0 0 Distortion0= 0 LM0= -147.721 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -6.58588 -6.62274 -4.26 -5.77525 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
    """

    """MOSES = 2009
    0 ||| yet a crucial step for the Balkans .  ||| d: 0 -1.39532 0 0 -1.10053 0 0 lm: -135.242 tm: -3.65122 -9.83896 -3.59304 -6.25423 3.99959 w: -8 ||| -164.237 ||| 0=0 1-4=1-4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7
    """
    current_index = -1 # gia su chua doc cau nao
    current_file_name = "PhraseN"
    int_number_of_sentences_in_PhraseN = 0
    max_number_of_sentences_in_PhraseN = 1000

    for line in file_reader:
        list_items = [] # set empty list

        line = line.strip() #trim line

        if len(line) == 0: #xuong dong hay het file
            break

        list_items = line.split(delimiter) # Split with delimiter "|||"

        if len(list_items) ==0:
            break

        #output: -23.1953 -52.1298 7 yet a crucial step for the balkans
        #weighted overall score ~ index_3; LM0= -147.721; number of words in hypothesis sentence; hypothesis sentence
        str_index = list_items[0].strip() # trim string

        #weighted overall score
        str_weighted_overall_score = list_items[3].strip() # trim string

        #LM0= -147.721
        str_scores = list_items[2].strip().lower() # trim string
        #lexicalreordering0= -2.31489 0 0 -1.80126 0 0 distortion0= 0 lm0= -147.721 wordpenalty0= -16 phrasepenalty0= 15 translationmodel0= -6.58588 -6.62274 -4.26 -5.77525
        start = str_scores.find('lm')

        config_end_user = load_config_end_user()

        if config_end_user.VERSION_MOSES == 2009:
            """d: 0 -1.39532 0 0 -1.10053 0 0 lm: -135.242 tm: -3.65122 -9.83896 -3.59304 -6.25423 3.99959 w: -8
            """
            end = str_scores.find('tm')
        else:
            """LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405
            """
            end = str_scores.find('wordpenalty')

        str_lm = str_scores[start:end].strip() #'lm0= -147.721'

        if config_end_user.VERSION_MOSES == 2009:
            lst_lm = str_lm.split(":")
        else:
            lst_lm = str_lm.split("=")

        str_score_lm = lst_lm[1].strip() #trim string

        #hypothesis sentence
        hyp_sentence = list_items[1].strip() # trim string

        #pre-processing voi nhung cau co dau cau o dau
        #muc dich: khong lam cho ngram hieu nham la ket thuc cau
        default_begin_of_sentence = "-"
        #list_char_end_of_sentence = [".", "!","?", "..."]
        list_char_end_of_sentence = [".", "!","?"]

        if hyp_sentence[0] in list_char_end_of_sentence:
            #hyp_sentence[0] = default_begin_of_sentence
            #TypeError: 'str' object does not support item assignment

            #'J' + word[1:]
            hyp_sentence = default_begin_of_sentence + hyp_sentence[1:]

        #number of words in hypothesis sentence;
        num_of_words_in_hyp_sentence = len(hyp_sentence.split())

        #output string for PhraseN
        str_output = str_weighted_overall_score + " " + str_score_lm + " " + str(num_of_words_in_hyp_sentence) + " " + hyp_sentence
        #str_output = str_weighted_overall_score + " " + str_score_lm + " " + hyp_sentence

        #lay thu muc hien tai
        current_working_directory = os.getcwd()

        #chuyen den thu muc chua code script
        os.chdir(os.path.dirname(output_path))

        int_index = int(str_index)

        if int_index != current_index:
            #cau moi --> thay file de ghi vao
            current_index = int_index
            number_of_sentences += 1

            ##just for checking
            ##doi voi nhung PhraseN co du so luong N-best-list
            if int_number_of_sentences_in_PhraseN != max_number_of_sentences_in_PhraseN:
                print("%s co %d cau trong n-best-list." %(current_file_name, int_number_of_sentences_in_PhraseN))

            #update current_file_name = "PhraseN"
            #append information to file with new id
            current_file_name = "Phrase" + str_index
            int_number_of_sentences_in_PhraseN = 0
        #end if

        #for appending: file_output_path
        file_writer = open(current_file_name, mode = 'a', encoding = 'utf-8')
        int_number_of_sentences_in_PhraseN += 1

        file_writer.write(str_output)
        file_writer.write("\n")

        file_writer.close()

        #chuyen lai thu muc hien tai
        os.chdir(current_working_directory)

    #end for

    return number_of_sentences
"""
Phrase253 co 480 cau trong n-best-list.
Phrase273 co 120 cau trong n-best-list.
Phrase342 co 120 cau trong n-best-list.
Phrase379 co 480 cau trong n-best-list.
Phrase499 co 480 cau trong n-best-list.
Phrase648 co 40 cau trong n-best-list.
Phrase671 co 120 cau trong n-best-list.
Phrase685 co 120 cau trong n-best-list.
Phrase688 co 480 cau trong n-best-list.
Phrase744 co 40 cau trong n-best-list.
So cau trong file hypothesis la: 881
"""

"""Doi voi du lieu 10881

Phrase3474 co 37 cau trong n-best-list.
Phrase4178 co 224 cau trong n-best-list.
Phrase4660 co 370 cau trong n-best-list.
Phrase4661 co 370 cau trong n-best-list.
Phrase5755 co 224 cau trong n-best-list.
Phrase5944 co 464 cau trong n-best-list.
Phrase7483 co 236 cau trong n-best-list.
Phrase9075 co 328 cau trong n-best-list.
Phrase10273 co 633 cau trong n-best-list.
Phrase10648 co 39 cau trong n-best-list.
Phrase10744 co 322 cau trong n-best-list.
"""
"""
Phrase4660 co 12 cau trong n-best-list.
Phrase4661 co 12 cau trong n-best-list.
"""
#**************************************************************************#
def split_sentences_with_id_threads(file_input_path, output_path, n_thread, config_end_user):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type output_path: string
    :param output_path: contains path to script "nbestToLattice.sh"

    :rtype: the number of sentences in n-best-list. Default = 1000

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file output from TreeTagger')
    """
    tmp_dir = "/tmp/WCE_wpp_min_max_feature"+ "_" + str(n_thread) + "/"
    try:
      os.stat(tmp_dir)
    except:
      os.mkdir(tmp_dir)
    #tmp_dir = current_config.SCRIPT_TEMP + "_" + str(n_thread)
    print (file_input_path)
    print (tmp_dir)
    str_message_if_not_existed = "Not Existed file corpus input that is output from TreeTagger"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode='r', encoding='utf-8')

    delimiter = "|||"
    number_of_sentences = 0

    """MOSES >= 2013
0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , said m camus .  ||| LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15

0 ||| the chirurgiens of los angeles ont said qu' ils étaient outrés , declared m camus .  ||| LexicalReordering0= -2.31489 0 0 -1.80126 0 0 Distortion0= 0 LM0= -147.721 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -6.58588 -6.62274 -4.26 -5.77525 ||| -1014.93 ||| 0=0 1=1 2=2 3=3 4=4 5=5 6=6 7=7 8=8 9=9 10=10 11-13=11-12 14=13 15=14 16=15 ||| 0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9 10-10 11-11 12-12 13-12 14-13 15-14 16-15
    """

    """MOSES = 2009
    0 ||| yet a crucial step for the Balkans .  ||| d: 0 -1.39532 0 0 -1.10053 0 0 lm: -135.242 tm: -3.65122 -9.83896 -3.59304 -6.25423 3.99959 w: -8 ||| -164.237 ||| 0=0 1-4=1-4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7 ||| 0=0 1=1 2=3 3=2 4=4 5=5 6=6 7=7
    """
    current_index = -1 # gia su chua doc cau nao
    current_file_name = "PhraseN"
    int_number_of_sentences_in_PhraseN = 0
    max_number_of_sentences_in_PhraseN = 1000
    first_index = -1

    for line in file_reader:
        list_items = [] # set empty list

        line = line.strip() #trim line

        if len(line) == 0: #xuong dong hay het file
            break

        list_items = line.split(delimiter) # Split with delimiter "|||"

        if len(list_items) ==0:
            break
        #output: -23.1953 -52.1298 7 yet a crucial step for the balkans
        #weighted overall score ~ index_3; LM0= -147.721; number of words in hypothesis sentence; hypothesis sentence
        str_index = list_items[0].strip() # trim string
        if first_index == -1:
            first_index = int(str_index)

        #weighted overall score
        str_weighted_overall_score = list_items[3].strip() # trim string

        #LM0= -147.721
        str_scores = list_items[2].strip().lower() # trim string
        #lexicalreordering0= -2.31489 0 0 -1.80126 0 0 distortion0= 0 lm0= -147.721 wordpenalty0= -16 phrasepenalty0= 15 translationmodel0= -6.58588 -6.62274 -4.26 -5.77525
        start = str_scores.find('lm')

        #config_end_user = load_config_end_user()

        if config_end_user.VERSION_MOSES == 2009:
            """d: 0 -1.39532 0 0 -1.10053 0 0 lm: -135.242 tm: -3.65122 -9.83896 -3.59304 -6.25423 3.99959 w: -8
            """
            end = str_scores.find('tm')
        else:
            """LexicalReordering0= -1.81744 0 0 -1.64139 0 0 Distortion0= 0 LM0= -146.242 WordPenalty0= -16 PhrasePenalty0= 15 TranslationModel0= -7.20993 -7.62317 -2.93815 -4.42405
            """
            end = str_scores.find('wordpenalty')

        str_lm = str_scores[start:end].strip() #'lm0= -147.721'

        if config_end_user.VERSION_MOSES == 2009:
            lst_lm = str_lm.split(":")
        else:
            lst_lm = str_lm.split("=")

        str_score_lm = lst_lm[1].strip() #trim string

        #hypothesis sentence
        hyp_sentence = list_items[1].strip() # trim string

        #pre-processing voi nhung cau co dau cau o dau
        #muc dich: khong lam cho ngram hieu nham la ket thuc cau
        default_begin_of_sentence = "-"
        #list_char_end_of_sentence = [".", "!","?", "..."]
        list_char_end_of_sentence = [".", "!","?"]

        if hyp_sentence[0] in list_char_end_of_sentence:
            #hyp_sentence[0] = default_begin_of_sentence
            #TypeError: 'str' object does not support item assignment

            #'J' + word[1:]
            hyp_sentence = default_begin_of_sentence + hyp_sentence[1:]

        #number of words in hypothesis sentence;
        num_of_words_in_hyp_sentence = len(hyp_sentence.split())

        #output string for PhraseN
        str_output = str_weighted_overall_score + " " + str_score_lm + " " + str(num_of_words_in_hyp_sentence) + " " + hyp_sentence
        #str_output = str_weighted_overall_score + " " + str_score_lm + " " + hyp_sentence

        #lay thu muc hien tai
        #current_working_directory = os.getcwd()

        #chuyen den thu muc chua code script
        #print (output_path)

        os.chdir(os.path.dirname(tmp_dir))

        #xu ly du lieu dua vao PhraseN
        #current_path = os.path.realpath(tmp_dir)

        int_index = int(str_index)

        if int_index != current_index:
            #cau moi --> thay file de ghi vao
            current_index = int_index
            number_of_sentences += 1

            ##just for checking
            ##doi voi nhung PhraseN co du so luong N-best-list
            if int_number_of_sentences_in_PhraseN != max_number_of_sentences_in_PhraseN:
                print("WARNING: file %s with nbest size %d instead of %d" %(current_file_name, int_number_of_sentences_in_PhraseN, max_number_of_sentences_in_PhraseN))

            #update current_file_name = "PhraseN"
            #append information to file with new id
            current_file_name = tmp_dir + "Phrase" + str_index
            int_number_of_sentences_in_PhraseN = 0
        #end if

        #for appending: file_output_path
        file_writer = open(current_file_name, mode = 'a', encoding = 'utf-8')
        int_number_of_sentences_in_PhraseN += 1

        file_writer.write(str_output)
        file_writer.write("\n")

        file_writer.close()

        #chuyen lai thu muc hien tai
        #os.chdir(current_working_directory)

    #end for
    
    last_index=first_index+number_of_sentences

    return first_index, last_index
#**************************************************************************#
def extracting_corresponding_features(file_input_path, file_output_path):
    """
    Extracting the corresponding features: word, WPP any, nodes, min, max

    :type file_input_path: string
    :param file_input_path: contains corpus with format output from FASTNC tool & SRILM

    :type file_output_path: string
    :param file_output_path: contains corpus with format "word, WPP any, nodes, min, max" in each line; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format ')
    """
    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    current_phrase = ""
    first_phrase = "Phrase0"
    string_phrase = "Phrase"
    #test_end_phrase = "Phrase7071"

    #TienNLe added 2015-02-09 BEGIN
    is_extracted_phrase = False
    #TienNLe added 2015-02-09 END

    #read data in openned file
    for line in file_reader:
        #print("line: %s" %line)

        list_item = line.split() # split with Default Delimiter

        number_of_items = len(list_item)

        #just for testing
        """
        if list_item[0].strip() == test_end_phrase:
            print("Da duyet den %s" %test_end_phrase)
            break
        """

        #xet truong hop co 2 items
        if number_of_items == 2:
            #word, WPP any, nodes, min, max
            #since	1.00000 ( time=0 nodes=1 min=1.00000 max=1.00000 mean=1.00000 var=0.00000 svar=0.00000 )
            #yet	1.0
            str_word = list_item[0].strip()
            str_wpp_any = list_item[1].strip()
            str_nodes = "1"
            str_min = "1.00000"
            str_max = "1.00000"
            str_output = str_word + "\t" + str_wpp_any + "\t" + str_nodes + "\t" + str_min + "\t" + str_max + "\n"

            file_writer.write(str_output)
            is_extracted_phrase = True
            continue

        if number_of_items < 9: #neu dong chi co 6 item hay nho hon 9 thi dong do la dong gioi thieu
            #kiem tra nhung dong cho chua tu "Phrase"
            item1 = list_item[0].strip()

            #neu khong chua thi continue
            #if not is_in_string(string_phrase, item1):
            #    continue
            if not item1.startswith(string_phrase): #Tien Ngoc LE updated 2014.Dec.26
                continue

            #Phrase0 1 0.00 1.00 yet 0.18901
            #xuong dong hop ly
            if current_phrase != item1:
                current_phrase = item1 # update current_phrase
                #print("number of items: %d " %number_of_items)
                #print ("current phrase : %s " %current_phrase)

                if item1 != first_phrase:
                    #Neu Phrase chua xu ly thi cho mac dinh vao
                    if is_extracted_phrase == False:
                        str_word = "default"
                        str_wpp_any = "1.00000"
                        str_nodes = "1"
                        str_min = "1.00000"
                        str_max = "1.00000"
                        str_output = str_word + "\t" + str_wpp_any + "\t" + str_nodes + "\t" + str_min + "\t" + str_max + "\n"

                        file_writer.write(str_output)
                    #end if

                    file_writer.write("\n") # if not the first Phrase0 then add empty line
            #end if

                is_extracted_phrase = False #Gia su chua xu ly Phrase nay

        else: #nguoc lai la dong thong tin can lay
            #a	0.51267 ( time=0 nodes=5 min=0.03497 max=0.51267 mean=0.20000 var=0.13312 svar=0.36486 )
            str_word = list_item[0].strip()
            str_wpp_any = list_item[1].strip()

            key_nodes = "nodes"
            str_nodes = ""

            key_min = "min"
            str_min = ""

            key_max = "max"
            str_max = ""

            #get_str_value_given_key(str_key_value)
            for item in list_item:
                item = item.strip()

                #nodes
                if is_in_string(key_nodes, item):
                    str_nodes = get_str_value_given_key(item)

                #min
                if is_in_string(key_min, item):
                    str_min = get_str_value_given_key(item)

                #max
                if is_in_string(key_max, item):
                    str_max = get_str_value_given_key(item)

            #end for

            str_output = str_word + "\t" + str_wpp_any + "\t" + str_nodes + "\t" + str_min + "\t" + str_max + "\n"

            file_writer.write(str_output)
            is_extracted_phrase = True
        #end if

        #raise Exception("Just for test")
    #end for

    file_writer.write("\n") # if not the first Phrase0 then add empty line

    #close 2 files
    file_reader.close()
    file_writer.close()
#**************************************************************************#
#Chinh trong code 'nbestToLattice.sh': voi so dong se xu ly (Chu y: khong lay phan nhan voi he so 1000BestList, ma chi lay so cau N khac nhau trong PhraseN); Ngoai ra, PHAI cap nhat PATH den SRILM va FASTNC trong file nBestToLattice.sh --> nen viet ham xu ly replace trong giai doan pre-processing

#**************************************************************************#
def extracting_corresponding_features_threads(file_input_path, file_output_path):
    """
    Extracting the corresponding features: word, WPP any, nodes, min, max

    :type file_input_path: string
    :param file_input_path: contains corpus with format output from FASTNC tool & SRILM

    :type file_output_path: string
    :param file_output_path: contains corpus with format "word, WPP any, nodes, min, max" in each line; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """
    #check existed paths
    """
    if not os.path.exists(file_input_path):
        raise TypeError('Not Existed file corpus input with format ')
    """
    str_message_if_not_existed = "Not Existed file corpus input"
    is_existed_file(file_input_path, str_message_if_not_existed)

    #open 2 files:
    #for reading: file_input_path
    file_reader = open(file_input_path, mode = 'r', encoding = 'utf-8')#, 'r')

    #for writing: file_output_path
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')#, 'w')

    current_phrase = ""
    first_phrase = "Phrase0"
    string_phrase = "Phrase"
    #test_end_phrase = "Phrase7071"

    #TienNLe added 2015-02-09 BEGIN
    is_extracted_phrase = False
    #TienNLe added 2015-02-09 END

    #read data in openned file
    for line in file_reader:
        #print("line: %s" %line)

        list_item = line.split() # split with Default Delimiter

        number_of_items = len(list_item)

        #just for testing
        """
        if list_item[0].strip() == test_end_phrase:
            print("Da duyet den %s" %test_end_phrase)
            break
        """

        #xet truong hop co 2 items
        #file_writer.write(str(number_of_items)+" ")
        if (is_extracted_phrase == True and number_of_items == 6):
            file_writer.write("\n");
            is_extracted_phrase = False 
        if number_of_items == 2:
            #word, WPP any, nodes, min, max
            #since      1.00000 ( time=0 nodes=1 min=1.00000 max=1.00000 mean=1.00000 var=0.00000 svar=0.00000 )
            #yet        1.0
            str_word = list_item[0].strip()
            str_wpp_any = list_item[1].strip()
            str_nodes = "1"
            str_min = "1.00000"
            str_max = "1.00000"
            str_output = str_word + "\t" + str_wpp_any + "\t" + str_nodes + "\t" + str_min + "\t" + str_max + "\n"

            file_writer.write(str_output)
            is_extracted_phrase = True
            continue

        if number_of_items < 9: #neu dong chi co 6 item hay nho hon 9 thi dong do la dong gioi thieu
            #kiem tra nhung dong cho chua tu "Phrase"
            item1 = list_item[0].strip()

            #neu khong chua thi continue
            #if not is_in_string(string_phrase, item1):
            #    continue
            if not item1.startswith(string_phrase): #Tien Ngoc LE updated 2014.Dec.26
                is_extracted_phrase = False 
                continue

            #Phrase0 1 0.00 1.00 yet 0.18901
            #xuong dong hop ly
            #if current_phrase != item1:
                #current_phrase = item1 # update current_phrase
                ##print("number of items: %d " %number_of_items)
                ##print ("current phrase : %s " %current_phrase)

                #if item1 != first_phrase:
                    ##Neu Phrase chua xu ly thi cho mac dinh vao
                    #if is_extracted_phrase == False:
                        #str_word = "default"
                        #str_wpp_any = "1.00000"
                        #str_nodes = "1"
                        #str_min = "1.00000"
                        #str_max = "1.00000"
                        #str_output = str_word + "\t" + str_wpp_any + "\t" + str_nodes + "\t" + str_min + "\t" + str_max + "\n"

                        #file_writer.write(str_output)
                    ##end if

                    #file_writer.write("\n") # if not the first Phrase0 then add empty line
            #end if
                is_extracted_phrase = False #Gia su chua xu ly Phrase nay

        else: #nguoc lai la dong thong tin can lay
            #a  0.51267 ( time=0 nodes=5 min=0.03497 max=0.51267 mean=0.20000 var=0.13312 svar=0.36486 )
            str_word = list_item[0].strip()
            str_wpp_any = list_item[1].strip()

            key_nodes = "nodes"
            str_nodes = ""

            key_min = "min"
            str_min = ""

            key_max = "max"
            str_max = ""

            #get_str_value_given_key(str_key_value)
            for item in list_item:
                item = item.strip()

                #nodes
                if is_in_string(key_nodes, item):
                    str_nodes = get_str_value_given_key(item)

                #min
                if is_in_string(key_min, item):
                    str_min = get_str_value_given_key(item)

                #max
                if is_in_string(key_max, item):
                    str_max = get_str_value_given_key(item)

            #end for

            str_output = str_word + "\t" + str_wpp_any + "\t" + str_nodes + "\t" + str_min + "\t" + str_max + "\n"

            file_writer.write(str_output)
            is_extracted_phrase = True
        #end if

        #raise Exception("Just for test")
    #end for

    file_writer.write("\n") # if not the first Phrase0 then add empty line

    #close 2 files
    file_reader.close()
    file_writer.close()
#**************************************************************************#

def generate_wpp_nodes_min_max(file_input_path, output_path):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type output_path: string
    :param output_path: contains path to script "nbestToLattice.sh"

    :raise ValueError: if any path is not existed
    """
    """
    + Deleting all files Phrase* in directory that contains code "nbestToLattice.sh"
    + Change mode execute for 2 files for fastnc & "nbestToLattice.sh"
    """
    #just for testing --> should disable
    preprocessing_for_extracting()

    current_config = load_configuration()

    config_end_user = load_config_end_user()

    number_of_sentences = split_sentences_with_id(file_input_path, output_path)
    #number_of_sentences = 10881
    #number_of_sentences = 2643
    #print("number_of_sentences:BEGIN")
    #print(number_of_sentences)
    #print("number_of_sentences:END")

    #$1: number of Phrases
    #$2: path to directory "SRILM_bin"
    #NOT USED - > Removed - $3: path to language model (target language)
    #$3: path to file "fastnc"
    #$4: path to file "RefToCtm.pl" in fastnc
    #$5: path to file output

    command_line = output_path + " " + str(number_of_sentences) + " " + config_end_user.SRILM_BIN_DIRECTORY + " " + config_end_user.TOOL_FASTNC + " " + config_end_user.TOOL_REFTOCTM + " " + current_config.WPP_NODES_MIN_MAX_TEMP

    print(command_line)

    """
/home/lent/Develops/Solution/ce_agent/ce_agent/config/../lib/shell_script/nbestToLattice.sh 2643 /home/lent/Develops/DevTools/srilm-1.7.1/bin/i686-m64 /home/lent/Develops/Solution/ce_agent/input_data/../../tool/fastnc/bin/fastnc /home/lent/Develops/Solution/ce_agent/input_data/../../tool/fastnc/scripts/RefToCtm.pl /home/lent/Develops/Solution/ce_agent/ce_agent/config/../extracted_features/en.column.feature_wpp_nodes_min_max_temp.txt
    """

    #generate the result with FAST tool and SRILM 1.7.1
    call_script(command_line, output_path)
#**************************************************************************#
def generate_wpp_nodes_min_max_threads(file_input_path, output_path , n_thread, current_config, config_end_user):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type output_path: string
    :param output_path: contains path to script "nbestToLattice.sh"

    :raise ValueError: if any path is not existed
    """
    """
    + Deleting all files Phrase* in directory that contains code "nbestToLattice.sh"
    + Change mode execute for 2 files for fastnc & "nbestToLattice.sh"
    """
    #just for testing --> should disable
    #preprocessing_for_extracting()

    #current_config = load_configuration()

    #config_end_user = load_config_end_user()
    tmp_dir = "/tmp/WCE_wpp_min_max_feature"+ "_" + str(n_thread) + "/"

    first_index, last_index = split_sentences_with_id_threads(file_input_path, output_path, n_thread, config_end_user)
    #number_of_sentences = 10881
    #number_of_sentences = 2643
    #print("number_of_sentences:BEGIN")
    #print(number_of_sentences)
    #print("number_of_sentences:END")

    #$1: number of Phrases
    #$2: path to directory "SRILM_bin"
    #NOT USED - > Removed - $3: path to language model (target language)
    #$3: path to file "fastnc"
    #$4: path to file "RefToCtm.pl" in fastnc
    #$5: path to file output
    #print ("Here I am : " + output_path)
    #number_of_sentences = 907
    command_line = output_path + " " + str(first_index) + " " + str(last_index) + " " + config_end_user.SRILM_BIN_DIRECTORY + " " + config_end_user.TOOL_FASTNC + " " + config_end_user.TOOL_REFTOCTM + " " + tmp_dir +" " + current_config.WPP_NODES_MIN_MAX_TEMP + "." + str(n_thread) + " " + current_config.LANGUAGE_MODEL_TGT
    
    #print("********************** generate_wpp_nodes_min_max_threads -> " + command_line)

    """
/home/lent/Develops/Solution/ce_agent/ce_agent/config/../lib/shell_script/nbestToLattice.sh 2643 /home/lent/Develops/DevTools/srilm-1.7.1/bin/i686-m64 /home/lent/Develops/Solution/ce_agent/input_data/../../tool/fastnc/bin/fastnc /home/lent/Develops/Solution/ce_agent/input_data/../../tool/fastnc/scripts/RefToCtm.pl /home/lent/Develops/Solution/ce_agent/ce_agent/config/../extracted_features/en.column.feature_wpp_nodes_min_max_temp.txt
    """

    #generate the result with FAST tool and SRILM 1.7.1
    call_script(command_line, output_path)
#**************************************************************************#
def feature_wpp_nodes_min_max(file_input_path, tool_path, file_output_temp_path, file_output_path):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type tool_path: string
    :param tool_path: contains path to script "nbestToLattice.sh"

    :type file_output_temp_path: string
    :param file_output_temp_path: contains result from script "nbestToLattice.sh"

    :type file_output_path: string
    :param file_output_path: contains corpus with format "word, WPP any, nodes, min, max" in each line; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """

    #step 1: generate result temp --> file_output_temp_path
    generate_wpp_nodes_min_max(file_input_path, tool_path)

    #step 2: filter corresponding features in result temp
    extracting_corresponding_features(file_output_temp_path, file_output_path)

    #Step 3: delete Phrase files
    #preprocessing_for_extracting()
#**************************************************************************#
def feature_wpp_nodes_min_max_threads(file_input_path, tool_path, file_output_temp_path, file_output_path, current_config, config_end_user):
    """
    :type file_input_path: string
    :param file_input_path: output of moses n-best-list

    :type tool_path: string
    :param tool_path: contains path to script "nbestToLattice.sh"

    :type file_output_temp_path: string
    :param file_output_temp_path: contains result from script "nbestToLattice.sh"

    :type file_output_path: string
    :param file_output_path: contains corpus with format "word, WPP any, nodes, min, max" in each line; there is a empty line among the sentences.

    :raise ValueError: if any path is not existed
    """

    #step 1: generate result temp --> file_output_temp_path
    #generate_wpp_nodes_min_max_threads(file_input_path, tool_path, current_config, config_end_user)
    print_time("Launching fastnc processes", current_config.RESULT_MESSAGE_OUTPUT)
    l_threads = []
    for l_inc in range(1,current_config.THREADS+1):
      ts = threading.Thread(target=generate_wpp_nodes_min_max_threads , args=(file_input_path+"."+str(l_inc), tool_path, l_inc, current_config, config_end_user))
      l_threads.append(ts)
      ts.start()
      time.sleep(1)
    for myT in l_threads:
      myT.join()
      
    print_time("fastnc processes finished", current_config.RESULT_MESSAGE_OUTPUT)
    print_time("Collecting data", current_config.RESULT_MESSAGE_OUTPUT)

    #step 2: filter corresponding features in result temp
    #extracting_corresponding_features(file_output_temp_path, file_output_path)
    l_threads = []
    for l_inc in range(1,current_config.THREADS+1):
      ts = threading.Thread(target=extracting_corresponding_features_threads , args=(file_output_temp_path+"."+str(l_inc), file_output_path+"."+str(l_inc)))
      l_threads.append(ts)
      ts.start()
      time.sleep(1)
    for myT in l_threads:
      myT.join()
    print_time("Collecting data finished", current_config.RESULT_MESSAGE_OUTPUT)


    #Step 3: delete Phrase files
    #preprocessing_for_extracting()
#**************************************************************************#
if __name__=="__main__":
    #split sentences with ID from n-best-list
    current_config = load_configuration()

    #chu y: cac buoc nay chua chuan hoa
    #chuan hoa cac thong so ve he so 10 hay 100 --> update code de phu hop voi yeu cau bai toan
    feature_wpp_nodes_min_max( current_config.MT_HYPOTHESIS_OUTPUT_NBESTLIST_INCLUDED_ALIGNMENT,  current_config.TOOL_N_BEST_TO_LATTICE, current_config.WPP_NODES_MIN_MAX_TEMP, current_config.WPP_NODES_MIN_MAX)

    print ('OK')

#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#
#**************************************************************************#