# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 11:31:37 2015
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

###############################################################
#  PyNLPl - WordAlignment Library for reading GIZA++ A3 files
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       In part using code by Sander Canisius
#
#       Licensed under GPLv3
#
#
# This library reads GIZA++ A3 files. It contains three classes over which
# you can iterate to obtain (sourcewords,targetwords,alignment) pairs.
#
#   - WordAlignment  - Reads target-source.A3.final files, in which each source word is aligned to one target word
#   - MultiWordAlignment  - Reads source-target.A3.final files, in which each source word may be aligned to multiple target target words
#   - IntersectionAlignment  - Computes the intersection between the above two alignments
#
#
###############################################################
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from pynlpl.common import u
"""
import bz2
import gzip
import copy
import io
#from sys import stderr
import os
import sys

#**************************************************************************#
#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#in order to test with line by line on the server

#from feature.common_functions import *
#from config.configuration import *
from common_module.cm_config import load_configuration, load_config_end_user
#**************************************************************************#
class GizaSentenceAlignment(object):
    def __init__(self, sourceline, targetline, index):
        self.index = index
        self.alignment = []
        if sourceline:
            self.source = self._parsesource(sourceline.strip())
        else:
            self.source = []
        self.target = targetline.strip().split(' ')

    def _parsesource(self, line):
        cleanline = ""

        inalignment = False
        begin = 0
        sourceindex = 0

        for i in range(0,len(line)):
            if line[i] == ' ' or i == len(line) - 1:
                if i == len(line) - 1:
                    offset = 1
                else:
                    offset = 0

                word = line[begin:i+offset]
                if word == '})':
                    inalignment = False
                    begin = i + 1
                    continue
                elif word == "({":
                    inalignment = True
                    begin = i + 1
                    continue
                if word.strip() and word != 'NULL':
                    if not inalignment:
                        sourceindex += 1
                        if cleanline: cleanline += " "
                        cleanline += word
                    else:
                        targetindex = int(word)
                        self.alignment.append( (sourceindex-1, targetindex-1) )
                begin = i + 1

        return cleanline.split(' ')


    def intersect(self,other):
        if other.target != self.source:
            print("GizaSentenceAlignment.intersect(): Mismatch between self.source and other.target: " + repr(self.source) + " -- vs -- " + repr(other.target),file=stderr)
            return None

        intersection = copy.copy(self)
        intersection.alignment = []

        for sourceindex, targetindex in self.alignment:
            for targetindex2, sourceindex2 in other.alignment:
                if targetindex2 == targetindex and sourceindex2 == sourceindex:
                    intersection.alignment.append( (sourceindex, targetindex) )

        return intersection

    def __repr__(self):
        s = " ".join(self.source)+ " ||| "
        s += " ".join(self.target) + " ||| "
        for S,T in sorted(self.alignment):
            s += self.source[S] + "->" + self.target[T] + " ; "
        return s


    def getalignedtarget(self, index):
        """Returns target range only if source index aligns to a single consecutive range of target tokens."""
        targetindices = []
        target = None
        foundindex = -1
        for sourceindex, targetindex in self.alignment:
            if sourceindex == index:
                targetindices.append(targetindex)
        if len(targetindices) > 1:
            for i in range(1,len(targetindices)):
                if abs(targetindices[i] - targetindices[i-1]) != 1:
                    break  # not consecutive
            foundindex = (min(targetindices), max(targetindices))
            target = ' '.join(self.target[min(targetindices):max(targetindices)+1])
        elif targetindices:
            foundindex = targetindices[0]
            target = self.target[foundindex]

        return target, foundindex
#**************************************************************************#
class GizaModel(object):
    def __init__(self, filename, encoding= 'utf-8'):
        if filename.split(".")[-1] == "bz2":
            self.f = bz2.BZ2File(filename,'r')
        elif filename.split(".")[-1] == "gz":
            self.f = gzip.GzipFile(filename,'r')
        else:
            self.f = io.open(filename,'r',encoding=encoding)
        self.nextlinebuffer = None


    def __iter__(self):
        self.f.seek(0)
        nextlinebuffer = u(next(self.f))
        sentenceindex = 0

        done = False
        while not done:
            sentenceindex += 1
            line = nextlinebuffer
            if line[0] != '#':
                raise Exception("Error parsing GIZA++ Alignment at sentence " +  str(sentenceindex) + ", expected new fragment, found: " + repr(line))

            targetline = u(next(self.f))
            sourceline = u(next(self.f))

            yield GizaSentenceAlignment(sourceline, targetline, sentenceindex)

            try:
                nextlinebuffer = u(next(self.f))
            except StopIteration:
                done = True


    def __del__(self):
        if self.f: self.f.close()


#------------------ OLD -------------------

def parseAlignment(tokens): #by Sander Canisius
    assert tokens.pop(0) == "NULL"
    while tokens.pop(0) != "})":
        pass

    while tokens:
        word = tokens.pop(0)
        assert tokens.pop(0) == "({"
        positions = []
        token = tokens.pop(0)
        while token != "})":
            positions.append(int(token))
            token = tokens.pop(0)

        yield word, positions

#**************************************************************************#
class WordAlignment(object):
    """Target to Source alignment: reads target-source.A3.final files, in which each source word is aligned to one target word"""

    def __init__(self,filename, encoding=False): #encoding = 'utf-8'
        """Open a target-source GIZA++ A3 file. The file may be bzip2 compressed. If an encoding is specified, proper unicode strings will be returned"""

        if filename.split(".")[-1] == "bz2":
            self.stream = bz2.BZ2File(filename,'r')
        else:
            self.stream = open(filename)
        self.encoding = encoding


    def __del__(self):
        self.stream.close()

    def __iter__(self): #by Sander Canisius
        line = self.stream.readline()
        while line:
            assert line.startswith("#")
            src = self.stream.readline().split()
            trg = []
            alignment = [None for i in xrange(len(src))]

            for i, (targetWord, positions) in enumerate(parseAlignment(self.stream.readline().split())):

                trg.append(targetWord)

                for pos in positions:
                    assert alignment[pos - 1] is None
                    alignment[pos - 1] = i

            if self.encoding:
                yield [ u(w,self.encoding) for w in src ], [ u(w,self.encoding) for w in trg ], alignment
            else:
                yield src, trg, alignment

            line = self.stream.readline()


    def targetword(self, index, targetwords, alignment):
        """Return the aligned targetword for a specified index in the source words"""
        if alignment[index]:
            return targetwords[alignment[index]]
        else:
            return None

    def reset(self):
        self.stream.seek(0)
#**************************************************************************#
class MultiWordAlignment(object):
    """Source to Target alignment: reads source-target.A3.final files, in which each source word may be aligned to multiple target words (adapted from code by Sander Canisius)"""

    def __init__(self,filename, encoding = False):
        """Load a target-source GIZA++ A3 file. The file may be bzip2 compressed. If an encoding is specified, proper unicode strings will be returned"""

        if filename.split(".")[-1] == "bz2":
            self.stream = bz2.BZ2File(filename,'r')
        else:
            self.stream = open(filename)

        #end if

        self.encoding = encoding

    def __del__(self):
        self.stream.close()

    def __iter__(self):
        line = self.stream.readline()
        while line:
            assert line.startswith("#")
            trg = self.stream.readline().split()
            src = []
            alignment = []

            for i, (word, positions) in enumerate(parseAlignment(self.stream.readline().split())):
                src.append(word)
                alignment.append( [ p - 1 for p in positions ] )


            if self.encoding:
                yield [ unicode(w,self.encoding) for w in src ], [ unicode(w,self.encoding) for w in trg ], alignment
            else:
                yield src, trg, alignment

            line = self.stream.readline()

    def targetword(self, index, targetwords, alignment):
        """Return the aligned targeword for a specified index in the source words. Multiple words are concatenated together with a space in between"""
        return " ".join(targetwords[alignment[index]])

    def targetwords(self, index, targetwords, alignment):
        """Return the aligned targetwords for a specified index in the source words"""
        return [ targetwords[x] for x in alignment[index] ]

    def reset(self):
        self.stream.seek(0)
#**************************************************************************#
class IntersectionAlignment:
    def __init__(self,source2target,target2source,encoding=False):
        self.s2t = MultiWordAlignment(source2target, encoding)
        self.t2s = WordAlignment(target2source, encoding)
        self.encoding = encoding

    def __iter__(self):
        for (src, trg, alignment), (revsrc, revtrg, revalignment) in zip(self.s2t,self.t2s): #will take unnecessary memory in Python 2.x, optimal in Python 3
            if src != revsrc or trg != revtrg:
                raise Exception("Files are not identical!")
            else:
                #keep only those alignments that are present in both
                intersection = []
                for i, x in enumerate(alignment):
                    if revalignment[i] in x:
                        intersection.append(revalignment[i])
                    else:
                        intersection.append(None)

                yield src, trg, intersection

    def reset(self):
        self.s2t.reset()
        self.t2s.reset()
#**************************************************************************#
def get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE(file_giza_path):
    """
    Creating list of alignment word to word from TARGET to SOURCE
    =============================================================
    :type file_giza_path: string
    :param file_giza_path: output from GIZA++

    :rtype: list of alignment word to word from target to source, Note: if value = '' then value=-1 that means there is no word in Source language associated.
    """

    #ref: get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE

    result = [] # empty list
    comma_char = ","
    # split string --> {'0=0', '1=1',..., '23=25,26'}

    #for writing: file_output_path
    current_config = load_configuration()
    file_output_path = current_config.WORD_ALIGNMENT_USING_GIZA
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    aligned = WordAlignment(file_giza_path)#current_config.TARGET_SOURCE_A3_FINAL)#Target to Source alignment; en_es.A3.final
    #(['ambos', 'tienen', 'cámaras', 'y', 'pantallas', 'líderes', 'en', 'su', 'clase', '.'], ['they', 'both', 'have', 'class-leading', 'cameras', 'and', 'displays', '.'], [1, 3, 4, 5, 6, 6, None, 6, 6, 7])
    for items in aligned:
        #print(items[2]) #hien thi du lieu o cot 3
        #print(items) #es_en.A3.final
        list_temp = []
        for item in items[2]:
            if item is None:
                list_temp.append(-1)
            else:
                list_temp.append(item)
            #end if
        #end for
        #print(list_temp)
        result.append(list_temp)

        #Ghi ra loggile
        str_output = " ".join(str(v) for v in list_temp)
        file_writer.write(str_output)
        file_writer.write("\n")
    #end for

    #close file
    file_writer.close()

    return result
#**************************************************************************#
### It means: we get the number of words from output-target
def get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE_after_optimising(file_giza_path, file_target_ref_test_format_row):
    """
    Creating list of alignment word to word from TARGET to SOURCE
    =============================================================
    :type file_giza_path: string
    :param file_giza_path: output from GIZA++

    :type file_target_ref_test_format_row: string
    :param file_target_ref_test_format_row: corpus target after preprocessing

    :rtype: list of alignment word to word from target to source, Note: if value = '' then value=-1 that means there is no word in Source language associated.
    """

    #ref: get_list_alignment_target_to_source_from_line_output_moses_TARGET_To_SOURCE
    word_alignment_temp = get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE(file_giza_path)
    """
    print("word_alignment_temp: BEGIN")
    print(len(word_alignment_temp))
    print("word_alignment_temp: END")
    """

    num_of_words_in_sentences =  count_number_of_words_in_sentences_format_row_to_result_list(file_target_ref_test_format_row)
    """
    print("num_of_words_in_sentences: BEGIN")
    print(len(num_of_words_in_sentences))
    print("num_of_words_in_sentences: END")
    """

    result = [] # empty list

    #for writing: file_output_path
    current_config = load_configuration()
    file_output_path = current_config.WORD_ALIGNMENT_USING_GIZA_AFTER_OPTIMISING
    file_writer = open(file_output_path, mode = 'w', encoding = 'utf-8')

    range_corpus = range(len(num_of_words_in_sentences))

    """
    print("range_corpus: BEGIN")
    print(range_corpus)
    print("range_corpus: END")
    """

    num_of_diff = 0

    for id_sent in range_corpus:
        list_temp = []
        num_of_words = num_of_words_in_sentences[id_sent]
        """
        print("num_of_words: BEGIN")
        print(num_of_words)
        print("num_of_words: END")
        """

        range_sentence = range(num_of_words)
        num_of_word_aligned = len(word_alignment_temp[id_sent])
        """
        print("num_of_word_aligned: BEGIN")
        print(num_of_word_aligned)
        print("num_of_word_aligned: END")
        """

        #just for testing
        if num_of_words != num_of_word_aligned:
            num_of_diff += 1

        for i in range_sentence:
            if i < num_of_word_aligned:
                list_temp.append(word_alignment_temp[id_sent][i])
            else:
                list_temp.append(-1)
            #end if
        #end for

        result.append(list_temp)

        #Ghi ra loggile
        str_output = " ".join(str(v) for v in list_temp)
        file_writer.write(str_output)
        file_writer.write("\n")
    #end for

    #close file
    file_writer.close()

    print("num_of_diff: BEGIN - So luong cau co alignment lech nhau")
    print(num_of_diff)
    print("num_of_diff: END")

    return result
#**************************************************************************#
def get_alignment_by_giza(path_to_tool_giza, path_to_tool_mkcls, path_to_corpus, source_corpus_name, target_corpus_name):
    current_config = load_configuration()

    command_line = "bash " #Path to the shell script TreeeTagger
    script_path = current_config.TOOL_GIZA

    #chmod execute for script
    run_chmod(script_path)

    command_line = command_line + " " + script_path + " " + path_to_tool_giza + " " + path_to_tool_mkcls + " " + path_to_corpus + " " + source_corpus_name + " " + target_corpus_name

    print(command_line)

    #Run Script
    #call_script(command_line, script_path)

    list_of_commands = []

    ##Generate Shell Script
    list_of_commands.append(command_line)
    create_script_temp(list_of_commands)

    #Run Script
    call_script(current_config.SCRIPT_TEMP, current_config.SCRIPT_TEMP)
#**************************************************************************#
if __name__=="__main__":
    #Test case:
    current_config = load_configuration()

    path_to_tool_giza = current_config.PATH_TO_TOOL_GIZA
    path_to_tool_mkcls = current_config.PATH_TO_TOOL_MKCLS
    path_to_corpus = current_config.PATH_TO_CORPUS
    source_corpus_name = current_config.SOURCE_CORPUS_NAME
    target_corpus_name = current_config.TARGET_CORPUS_NAME

    get_alignment_by_giza(path_to_tool_giza, path_to_tool_mkcls, path_to_corpus, source_corpus_name, target_corpus_name)

    #current_config.TARGET_SOURCE_A3_FINAL
    #WordAlignment(object) : Target to Source alignment: reads target-source.A3.final files, in which each source word is aligned to one target word
    #en_es.A3.final
    ## Sentence pair (12272) source length 8 target length 10 alignment score : 6.1057e-13
    #ambos tienen cámaras y pantallas líderes en su clase .
    #NULL ({ 7 }) they ({ }) both ({ 1 }) have ({ }) class-leading ({ 2 }) cameras ({ 3 }) and ({ 4 }) displays ({ 5 6 8 9 }) . ({ 10 })

    #aligned = WordAlignment(current_config.TARGET_SOURCE_A3_FINAL)#Target to Source alignment; en_es.A3.final
    #(['ambos', 'tienen', 'cámaras', 'y', 'pantallas', 'líderes', 'en', 'su', 'clase', '.'], ['they', 'both', 'have', 'class-leading', 'cameras', 'and', 'displays', '.'], [1, 3, 4, 5, 6, 6, None, 6, 6, 7])

    #aligned = MultiWordAlignment(current_config.TARGET_SOURCE_A3_FINAL)#Source to Target alignment
    #(['they', 'both', 'have', 'class-leading', 'cameras', 'and', 'displays', '.'], ['ambos', 'tienen', 'cámaras', 'y', 'pantallas', 'líderes', 'en', 'su', 'clase', '.'], [[], [0], [], [1], [2], [3], [4, 5, 7, 8], [9]])

    #aligned = GizaModel(current_config.TARGET_SOURCE_A3_FINAL)
    #they both have class-leading cameras and displays . ||| ambos tienen cámaras y pantallas líderes en su clase . ||| .->en ; both->ambos ; class-leading->tienen ; cameras->cámaras ; and->y ; displays->pantallas ; displays->líderes ; displays->su ; displays->clase ; .->. ;


    #targetword(self, index, targetwords, alignment)
    #target_word = aligned.targetword(0, targetwords, alignment)
    """
    num_of_sent = 0

    for items in aligned:
        #print(items[2]) #hien thi du lieu o cot 3
        print(items) #es_en.A3.final
        num_of_sent += 1

    print("num of items in aligned is: %d" %num_of_sent)
    """

    #get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE
    #target_source_A3_final: ../extracted_features/en_es.A3.final
    temp = get_list_alignments_target_to_source_from_output_giza_TARGET_To_SOURCE(current_config.TARGET_SOURCE_A3_FINAL)

    print(temp)

    print("len = %d" %len(temp))

    print("OK")