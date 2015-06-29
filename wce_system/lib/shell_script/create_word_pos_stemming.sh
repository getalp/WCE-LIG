#! /bin/bash

#Created by: Tien Ngoc LE (ngoc-tien.le@imag.fr)
#Date Created: 2014.Dec.19
#Date Updated: 

#Purpose: Using TreeTagger for create (word, pos, stemming) for each word in each line --> output format ROW
#$1 --> Path to directory TreeTagger (that contains the following directories: bin, cmd, doc, lib)
#$2 --> en/fr
#$3 --> input name within path
#$4 --> output name within path

#Create TreeTagger files for fr/en/de/it/es
make-factor-pos.tree-tagger-TienLe-TanLe.perl -tree-tagger $1 -l $2 $3 temp -wordtaglemma

#replace "<UNK>||||||" --> "<unk>|||<unk>|||<unk>" trong format dong
sed 's-<UNK>||||||-<unk>|||<unk>|||<unk>-g' < temp > temp2

mv temp2 $4

rm -rf temp
