#! /bin/bash

## Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole Toolkit (eval_agent Toolkit) 
## Homepage: http://getalp.imag.fr
##
## Author: Tien LE (ngoc-tien.le@imag.fr)
## Advisors: Laurent Besacier & Benjamin Lecouteux
## URL: tienhuong.weebly.com

#for french
#xoa file ket qua neu no da ton tai truoc do
#Neu khong xoa thi xay ra hien tuong cong don
#rm -rf $2

#Chu y: Neu bo file $2 thi khong the co ket qua day du duoc. 
#Vi day la qua trinh cong don ket qua
num_sent=1
while read line 
do
	if [ "$line" != "" ] 
	then
		word=`echo $line | awk '{ print $1}' `
		pos=`echo $line | awk '{ print $2}' `
		
		#echo $pos

		#if this word is not Noun, verb, adj or adverb 
		
		if [ "$pos" == "OTHER" ]
		then
			echo "Number of senses:-1" >> $2
		else
			#chu y: khi xu ly voi ket qua tra ve tu file khac
			sh sense2.sh FR $word $pos >> $2
		fi
	else
		echo >> $2
		echo "Finished line: $num_sent"
		let num_sent=num_sent+1
	fi

done < $1
