#!/bin/bash

## Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole Toolkit (eval_agent Toolkit) 
## Homepage: http://getalp.imag.fr
##
## Author: Tien LE (ngoc-tien.le@imag.fr)
## Advisors: Laurent Besacier & Benjamin Lecouteux
## URL: tienhuong.weebly.com

# $1: grammar for Berkeley Parser
# $2: input file
# $3: output file

#EN: java -jar BerkeleyParser-1.7.jar -gr $1 -binarize -inputFile $2 -outputFile $3
#./berkeley_parser.sh eng_sm6.gr input output

java -jar BerkeleyParser-1.7.jar -gr $1 -binarize -inputFile $2 -outputFile $3
