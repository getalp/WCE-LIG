#! /bin/bash

#Created by: Tien Ngoc LE (ngoc-tien.le@imag.fr)
#Date Created: 2014.Dec.14
#Date Updated: 2014.Dec.19

#Purpose: preprocessing for our solution 
#$1 --> en/fr
#$2 --> input name within path
#$3 --> output name within path

# Replace phrase "verbe-t-pronom" by "pronom verbe"
# Example: "a-t-il" --> "il a"
if [ $1 == "fr" ]
then
	sed -e "s/\([[:alpha:]]*\)\-t\-\([[:alpha:]]*\)/ \2 \1/g" $2 > temp1
else
	cp $2 temp1
fi

#note: just only using for EN & FR
#pre-tokenizer
#perl pre-tokenizer.perl -b -q -l $1 < temp3 > temp3.1
#perl pre-tokenizer.perl -l $1 < temp1 > temp2

#normalize punctuation
perl normalize-punctuation.perl $1 < temp1 > temp2
#if [ $1 == "fr" ]
#then
	#lenh nay lam lowercase ap dung cho tieng Phap 
	#sed 's/.*/\L&/g' temp2 > temp2.1
	#ref: http://stackoverflow.com/questions/4569825/sed-one-liner-to-convert-all-uppercase-to-lowercase
	#http://timmurphy.org/2013/02/24/converting-to-uppercase-lowercase-in-sed/
	#lowercase the first letter --> neu khong lam buoc nay thi TreeTagger doi voi tieng Phap khong tot lam, se nhan dien da so cac tu hoa la NAM :) , updated 2014.Dec.29
	#sed 's/^./\L&\E/g' temp2 > temp2.1
	#sed 's/.*/\L&/g' temp3 > temp4
	
	#uppercase ky tu dau tien cua cau
	#sed 's/^./\U&\E/g' output_preprocessing.src.all > output_preprocessing_uppercase_first_letters.src.all
	
	#perl normalize-punctuation.perl fr < temp4 > temp5
#else
	#cp temp3 temp4
	#perl normalize-punctuation.perl en < temp4 > temp5.1
#fi

#tokenizer
#perl tokenizer.perl -b -q -a -l $1 < temp4  > temp5
perl tokenizer.perl -l $1 < temp2 > temp3

#remove-non-printing-char.perl
#perl remove-non-printing-char.perl < $2.temp > temp2
#cp $2.temp temp2

#lowercase
#da chuyen thanh file sh
#Khong nen dung lowercase vi trong MOSES can phai co TrueCaser de hoc chinh xac hon
#perl lowercase.perl < $2.temp > temp2
perl lowercase.perl < temp3 > temp4

#Thay the cac chuoi dac biet de lam nhieu du lieu; nhu: dr. thanh dr ...
#phan nay can thiet de dua vao xu ly tieng noi
#lam mat dau ) o cau 406, 743, 878
#vi du: (GEW); (RVM); (Zaragoza)
#perl de-special-phrase.perl < input.rm_non_prt_chr > input.rm_non_prt_chr.rep_special_phrase

#replace special character in twice. Chu y: Nen chay 1 lan nua de vet can nhung truong hop sau: Vi du: "&amp; # 45" ; --lan 1--> "& # 45 ;" --lan 2--> "-"
perl deescape-special-chars.perl < temp4 > temp5
perl deescape-special-chars.perl < temp5 > temp6

#add_character_end_of_sentence
#python3 add_char_end_of_sentence.py temp7 temp8
#vi khi them dau cau thi phan alignment se bi lech 
#cp temp7 temp8

#convert corresponding name :)
#mv temp8 $3
mv temp6 $3

##############################################################################################################################
#replace unicode punctuation
#khong dung ham nay vi sh hay python co the doc file utf8
#replace-unicode-punctuation.perl < $1.ttt > input.uni_punct

#lowercase
#da chuyen thanh file sh
#Khong nen dung lowercase vi trong MOSES can phai co TrueCaser de hoc chinh xac hon
#lowercase.perl < input.uni_punct.rep_special_phrase > input.uni_punct.lc

#filter out long sentence (Khong can buoc nay vi da duoc clean bang moses)
#clean-corpus-n.perl common_name fr en  common_name.clean 1 100
##############################################################################################################################

#cleaning ~ remove all of the template files
#if [ $1 == "fr" ]
#then
#	rm -rf temp2.1
#fi

#rm -rf temp1 temp2 temp3 temp4 temp5 temp6



