#! /bin/bash

#Created by: Tien Ngoc LE (ngoc-tien.le@imag.fr)
#Date Created: 2015.Feb.22
#Date Updated: 

#Purpose: Replace for each word in each line --> output format ROW
#$1 --> ASR format column
#$2 --> WCE format column
#$3 --> output name within path

#diff -y A_S_R W_C_E > filediff.txt
diff -y $1 $2 > $3
