#! /bin/bash

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

#Created on Fri Dec  5 13:51:55 2014
#$1: /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MThypothesis_2643_tokenized.txt 
#$2: /home/tienle/Documents/Develops/DevTools/srilm/bin/i686-m64/ngram  
#$3: -order 5 
#$4: -lm /home/tienle/Documents/Develops/GeTools/Target_ngram-BackOffBehavior/MT08.en.lm  
#$5: > result

cat $1 | $2  -order $3 -lm $4  -ppl - -debug 2 -no-eos -no-sos > $5
