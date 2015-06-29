#! /bin/bash

#Created by: Tien Ngoc LE (ngoc-tien.le@imag.fr)
#Date Created: 2015.Feb.17
#Date Updated: 

#Purpose: Replace for each word in each line --> output format ROW
#$1 --> input name within path
#$2 --> output name within path

#replace "<UNK>||||||" --> "<unk>|||<unk>|||<unk>" in format row
sed 's-<UNK>||||||-<unk>|||<unk>|||<unk>-g' < $1 > temp2

mv temp2 $2
