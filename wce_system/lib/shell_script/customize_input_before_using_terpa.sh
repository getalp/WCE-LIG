#! /bin/bash

#Created by: Tien Ngoc LE (ngoc-tien.le@imag.fr)
#Date Created: 2015.Feb.22
#Date Updated: 

#Purpose: Replace for each word in each line --> output format ROW
#$1 --> input name within path
#$2 --> output name within path

#replace "<UNK>||||||" --> "<unk>|||<unk>|||<unk>" in format row
sed 's-<UNK>-unk-g' < $1 > temp2
sed 's-<unk>-unk-g' < temp2 > tempK

mv tempK $2

rm -rf temp2
