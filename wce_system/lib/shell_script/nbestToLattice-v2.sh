#!/bin/bash

#Updated by Tien Ngoc LE updated 2014.Dec.23

export LC_ALL=C

dem=0
SRILM_BIN=/home/lent/Develops/DevTools/srilm-1.7.1/bin/i686-m64
ML=../../corpus/language_model/lm_5gram.en
ORDER=5

while [ "$dem" -lt $1 ] ;
do
	i=Phrase$dem

    
    LM_ACCESS="-lm $ML"
        
	$SRILM_BIN/nbest-lattice -nbest $i -write ${i}.wlat
	$SRILM_BIN/wlat-to-pfsg ${i}.wlat > ${i}.wlat.pfsg
	$SRILM_BIN/lattice-tool  -in-lattice ${i}.wlat.pfsg -write-htk -out-lattice ${i}.wlat.pfsg.htk
	#$SRILM_BIN/lattice-tool -read-htk -in-lattice ${i}.wlat.pfsg $LM_ACCESS -order $ORDER -htk-logbase 10 -write-htk -out-lattice ${i}.wlat.pfsg.htk
	
	#$SRILM_BIN/lattice-tool -read-htk -in-lattice-list $CONF_DIR/Liste_treil_${NAME}.lst $LM_ACCESS -order $ORDER -htk-logbase 10 -htk-lmscale $FUDGE -htk-wdpenalty $PENALITE -write-htk -out-lattice-dir $HTK_LM
        
	head -n 1 $i | cut -f4- -d\ > ${i}b
	#RefToCtm.pl ${i}b
	#/home/tienle/Documents/Develops/GeTools/WPP-Nodes-Min-Max/fastnc/scripts/RefToCtm.pl ${i}b
	../../../tool/fastnc/scripts/RefToCtm.pl ${i}b

	for j in *.ctm;
	do
		#./fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ./Results.txt
		#/home/tienle/Documents/Develops/GeTools/WPP-Nodes-Min-Max/fastnc/bin/fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ./Results.txt
		../../../tool/fastnc/bin/fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ../../extracted_features/en.column.feature_wpp_nodes_min_max_temp.txt
	done
	#rm -f *.ctm
	#Tien Ngoc LE added 2014.Dec.24	
	find . -type f -iname \*.ctm -delete	
	rm ${i}.wlat ${i}.wlat.pfsg ${i}.wlat.pfsg.htk ${i}b
        
	dem=$(($dem+1))
done

#for i in *.htk;
#do
#       ./fastnc --read-lattice $i --compute-mesh --write-mesh ${i}.mesh;
#       ./fastnc --read-ctm Ctm0.ctm  --read-lattice $i --compute-posteriors --compute-mesh  --align-ctm-dtw
#done

