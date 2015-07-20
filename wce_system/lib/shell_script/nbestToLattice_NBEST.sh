#!/bin/bash

#Updated by Tien Ngoc LE updated 2014.Dec.24

export LC_ALL=C

dem=0
SRILM_BIN=/home/lent/Develops/DevTools/srilm-1.7.1/bin/i686-m64
ML=../../corpus/language_model/lm_5gram.en

while [ "$dem" -lt $1 ] ;
do
	i=Phrase$dem
	count=`wc Phrase$dem | awk '{ print $1 }'`
	k=1 #Tu dau den cuoi
	
	LM_ACCESS="-lm $ML"
	
	while [ "$k" -le "$count" ] ;
	do
		awk "NR==$k" Phrase$dem >> tmp
		m=$(($k-1))
		n=$(($count-$k))
		head -$m Phrase$dem >> tmp
		tail -$n Phrase$dem >> tmp
		
		#/home/Toolkits/Srilm/bin/i686-m64
		
		$SRILM_BIN/nbest-lattice -nbest tmp  -write ${i}.wlat
		$SRILM_BIN/wlat-to-pfsg ${i}.wlat > ${i}.wlat.pfsg
		#$SRILM_BIN/lattice-tool  -in-lattice ${i}.wlat.pfsg $LM_ACCESS -write-htk -out-lattice ${i}.wlat.pfsg.htk
		$SRILM_BIN/lattice-tool  -in-lattice ${i}.wlat.pfsg -write-htk -out-lattice ${i}.wlat.pfsg.htk
		
		head -n1 tmp  | cut -f4- -d\ > ${i}b
		#RefToCtm.pl ${i}b
		../../../tool/fastnc/scripts/RefToCtm.pl ${i}b

		for j in *.ctm
		do
			#./fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ./Results.txt
			../../../tool/fastnc/bin/fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ../../extracted_features/en.column.feature_wpp_nodes_min_max_temp.txt
		done
		
		#echo >> ./Results.txt
		echo >> ../../extracted_features/en.column.feature_wpp_nodes_min_max_temp.txt
		
		#rm -f *.ctm
		find . -type f -iname \*.ctm -delete
		rm tmp
		rm ${i}.wlat ${i}.wlat.pfsg ${i}.wlat.pfsg.htk ${i}b
		
		k=$(($k+1))
	done
	
	dem=$(($dem+1))
	echo "FINISH:      "$dem
done

#for i in *.htk;
#do
#       ./fastnc --read-lattice $i --compute-mesh --write-mesh ${i}.mesh;
#       ./fastnc --read-ctm Ctm0.ctm  --read-lattice $i --compute-posteriors --compute-mesh  --align-ctm-dtw
#done

