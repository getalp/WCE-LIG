#! /bin/bash

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

sed 's/0 sentences,.*//g' < $1 | sed 's/0 zeroprobs,.*//g' > tmpfile1

sed '/^$/d' tmpfile1  > tmpfile2

#TienLe added 2014-10-28
#sed 's/p( .*= \[//g' < tmpfile2  | sed 's/\] .*\[ .*\]//g' | sed 's/.* .*//g' | sed 's/^[^	].*//g' |  sed '1d' | sed '$d' > $2

#tmpfile3: chi luu thong tin co dang (cac dong cach nhau bang khoang trang)
#	1gram
#	2gram
sed 's/p( .*= \[//g' < tmpfile2  | sed 's/\] .*\[ .*\]//g' | sed 's/.* .*//g' | sed 's/^[^	].*//g' |  sed '1d' | sed '$d' > tmpfile3

#Buoc - Bo dau tab trong file tmpfile3 
awk {'print $1'} < tmpfile3 > tmpfile4

#Buoc - Xoa 'gram' trong dong (co nghia la: thay the bang ky tu rong)
sed s/gram//g  < tmpfile4 > tmpfile5

#Buoc - Thay the 'OOV' bang so 0
sed s/OOV/0/g < tmpfile5 > $2

rm tmpfile1 tmpfile2 tmpfile3 tmpfile4 tmpfile5

#sed '/0 sentences/d'< tmpfile-order5 > tmp1
#sed '/0 zeroprobs,/d'< tmp1 > tmp2
#sed '/^[A-Z"¿(].*$/d'< tmp2 > tmp3
#sed 's/.*= //g' < tmp3 > tmp4 
#sed 's/].*//g' < tmp4 > tmp5
#sed 's/\[//g' < tmp5 > tmp6
# mv tmp6  target-ngram

