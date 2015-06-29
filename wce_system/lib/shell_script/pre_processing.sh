#! /bin/bash

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

#Purpose: preprocessing for our solution 
#$1 --> en/fr
#$2 --> input name within path
#$3 --> output name within path

# Replace phrase "verbe-t-pronom" by "pronom verbe"
# Example: "a-t-il" --> "il a"
if [ $1 = "fr" ];
then
	sed -e "s/\([[:alpha:]]*\)\-t\-\([[:alpha:]]*\)/ \2 \1/g" $2 > temp1
else
	cp $2 temp1
fi

#normalize punctuation
perl normalize-punctuation.perl $1 < temp1 > temp2

#tokenizer
perl tokenizer.perl -l $1 < temp2 > temp3

#lowercase
perl lowercase.perl < temp3 > temp4

#replace special character
perl deescape-special-chars.perl < temp4 > temp5

#convert corresponding name :)
mv temp5 $3

#rm -rf temp1 temp2 temp3 temp4



