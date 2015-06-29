#! /bin/bash

#$1: path to plain2snt.out ; snt2cooc.out ; GIZA++
#$2: path to mkcls 
#$3: path to corpus that contain source & target
#$4: name of source_language_corpus
#$5: name of target_language_corpus

#concat: path+filename
path_to_corpus=$3
source_corpus_name=$4
target_corpus_name=$5
path_to_source_corpus="$path_to_corpus"/"$source_corpus_name"
path_to_target_corpus="$path_to_corpus"/"$target_corpus_name"

echo $path_to_source_corpus
echo $path_to_target_corpus

#step 1: Use plain2snt.out to convert your corpus into GIZA++ format: 
#./plain2snt.out [source_language_corpus] [target_language_corpus]
#Which will generate the files:
#[source_language_corpus].vcb
#[target_language_corpus].vcb
#[source_language_corpus]_[target_language_corpus].snt
#[target_language_corpus]_[source_language_corpus].snt
#--> ./GIZA++-v2/plain2snt.out corpus/output_preprocessing.src corpus/output_preprocessing.tgt
$1/./plain2snt.out $path_to_source_corpus $path_to_target_corpus

#step 2: to generate word classes, using mkcls
#./mkcls -p[source_language_corpus] -V[source_language_corpus].vcb.classes
#./mkcls -p[target_language_corpus] -V[target_language_corpus].vcb.classes
#Which will produce the files:
#[source_language_corpus].vcb.classes
#[source_language_corpus].vcb.classes.cats
#[target_language_corpus].vcb.classes
#[target_language_corpus].vcb.classes.cats
#--> ./mkcls-v2/mkcls -pcorpus/output_preprocessing.src -Vcorpus/output_preprocessing.src.vcb.classes
#--> ./mkcls-v2/mkcls -pcorpus/output_preprocessing.tgt -Vcorpus/output_preprocessing.tgt.vcb.classes
path_to_source_corpus_vcb="$path_to_source_corpus".vcb
path_to_target_corpus_vcb="$path_to_target_corpus".vcb
path_to_source_corpus_vcb_classes="$path_to_source_corpus".vcb.classes
path_to_target_corpus_vcb_classes="$path_to_target_corpus".vcb.classes

$2/./mkcls -p$path_to_source_corpus -V$path_to_source_corpus_vcb_classes
$2/./mkcls -p$path_to_target_corpus -V$path_to_target_corpus_vcb_classes

#mkcls - a program for making word classes: Usage: 
# mkcls [-nnum] [-ptrain] [-Vfile] opt
#-V output classes (Default: no file)
#-n number of optimization runs (Default: 1); larger number => better results
#-p filename of training corpus (Default: 'train')
#Example:
# mkcls -c80 -n10 -pin -Vout opt
#(generates 80 classes for the corpus 'in' and writes the classes in 'out')

#Create the cooccurence
#en_es
#./GIZA++-v2/snt2cooc.out corpus/output_preprocessing.src.vcb corpus/output_preprocessing.tgt.vcb corpus/output_preprocessing.src_output_preprocessing.tgt.snt > corpus/output_preprocessing.src_output_preprocessing.tgt.cooc 
source_target_name="$source_corpus_name"_"$target_corpus_name"
target_source_name="$target_corpus_name "_"$source_corpus_name"
path_to_source_target_snt="$path_to_corpus"/"$source_corpus_name"_"$target_corpus_name".snt
path_to_target_source_snt="$path_to_corpus"/"$target_corpus_name"_"$source_corpus_name".snt
path_to_source_target_cooc="$path_to_corpus"/"$source_corpus_name"_"$target_corpus_name".cooc
path_to_target_source_cooc="$path_to_corpus"/"$target_corpus_name"_"$source_corpus_name".cooc

#source-target
$1/./snt2cooc.out $path_to_source_corpus_vcb $path_to_target_corpus_vcb $path_to_source_target_snt > $path_to_source_target_cooc

#target-source
$1/./snt2cooc.out $path_to_target_corpus_vcb $path_to_source_corpus_vcb $path_to_target_source_snt > $path_to_target_source_cooc

#es_en
#./GIZA++-v2/snt2cooc.out corpus/output_preprocessing.tgt.vcb corpus/output_preprocessing.src.vcb corpus/output_preprocessing.tgt_output_preprocessing.src.snt > corpus/output_preprocessing.tgt_output_preprocessing.src.cooc 

#ket qua giong nhu tren
#./GIZA++-v2/snt2cooc.out corpus/output_preprocessing.src.vcb corpus/output_preprocessing.tgt.vcb corpus/output_preprocessing.tgt_output_preprocessing.src.snt > corpus/output_preprocessing.tgt_output_preprocessing.src.cooc

#step 3: use GIZA++ to build your dictionary (-S is the source language, -T is the target language, -C is the generated aligned text file, and -o is the output file prefix)
#./GIZA++ -S [target_language_corpus].vcb -T [source_language_corpus].vcb -C [target_language_corpus]_[source_language_corpus].snt -o [prefix] -outputpath [output_folder]
#If you followed the steps correctly, you should find a file named: "[prefix].actual.ti.final" located at [output_folder]. 

#source to target alignment
#./GIZA++-v2/GIZA++ -S corpus/output_preprocessing.src.vcb -T corpus/output_preprocessing.tgt.vcb -C corpus/output_preprocessing.src_output_preprocessing.tgt.snt -o en_es -outputpath corpus/ -CoocurrenceFile  corpus/output_preprocessing.src_output_preprocessing.tgt.cooc >& corpus/dictionary.log
$1/./GIZA++ -S $path_to_source_corpus_vcb -T $path_to_target_corpus_vcb -C $path_to_source_target_snt -o src_tgt -outputpath $path_to_corpus -CoocurrenceFile  $path_to_source_target_cooc

#target to source alignment
#./GIZA++-v2/GIZA++ -S corpus/output_preprocessing.tgt.vcb -T corpus/output_preprocessing.src.vcb -C corpus/output_preprocessing.tgt_output_preprocessing.src.snt -o es_en -outputpath corpus/ -CoocurrenceFile  corpus/output_preprocessing.tgt_output_preprocessing.src.cooc >& corpus/dictionary.log2
$1/./GIZA++ -S $path_to_target_corpus_vcb -T $path_to_source_corpus_vcb -C $path_to_target_source_snt -o tgt_src -outputpath $path_to_corpus -CoocurrenceFile  $path_to_target_source_cooc


#other idea
#//Suppose source language is French and target language is English
#plain2snt.out  FrenchCorpus.f  EnglishCorpus.e
#mkcls  -c30  -n20  -pFrenchCorpus.f  -VFrenchCorpus.f.vcb.classes  opt
#mkcls  -c30  -n20  -pEnglishCorpus.e  -VEnglishCorpus.e.vcb.classes  opt
#snt2cooc.out  FrenchCorpus.f.vcb  EnglishCorpus.e.vcb  FrenchCorpus.f_EnglishCorpus.e.snt >courpuscooc.cooc
#GIZA++  -S  FrenchCorpus.f.vcb  -T EnglishCorpus.e.vcb -C FrenchCorpus.f_EnglishCorpus.e.snt  -m1 100  -m2 30  -mh 30  -m3 30  -m4 30  -m5 30  -p1 o.95  -CoocurrenceFile  courpuscooc.cooc -o     dictionary

 
# In this script we assume that the target language is always english, and the source languages those in the "for" cycle
 
#./tokenizer.perl -l en < raw_corp.en > corp.tok.en
 
#tr '[:upper:]' '[:lower:]' < corp.tok.en > corp.tok.low.en
 
#mkcls -n10 -pcorp.tok.low.en -Vcorp.tok.low.en.vcb.classes
 
#for l in "it" "es" "de" "fr" "nl"
#do
#        echo "Pre-processing: tokenizing and lowering..."
 
        #./tokenizer.perl -l $l < raw_corp.$l > corp.tok.$l
 
        #tr '[:upper:]' '[:lower:]' < corp.tok.$l > corp.tok.low.$l
 
        #echo "Finished pre-processing, starting creation of vocabulary, cooccurrence and classes..."
 
        #mkcls -n10 -pcorp.tok.low.$l -Vcorp.tok.low.$l.vcb.classes
 
        #plain2snt corp.tok.low.$l corp.tok.low.en
 
        #snt2cooc corp.tok.low.$l_corp.tok.low.en.cooc corp.tok.low.$l.vcb corp.tok.low.en.vcb corp.tok.low.$l_corp.tok.low.en.snt
 
        #echo "Finished creation! Now we start, really :)"
 
        #echo "Starting alignment: $l -> en" > $l.timelog
        #date >> $l.timelog
 
        #mgiza $l_en.dict.gizacfg
 
        #echo "Finished alignment, starting merge of parts" >> $l.timelog
 
        #date >> $l.timelog
 
        #for i in 0 1 2 3 4 5 6 7
        #do
        #        cat $l_en.dict.A3.final.part$i >> corpus_word_aligned_$l_en
        #done
 
        #rm $l_en.dict.A3.final.part*
 
        #date >> $l.timelog
        #echo "End of process." >> $l.timelog
#done
