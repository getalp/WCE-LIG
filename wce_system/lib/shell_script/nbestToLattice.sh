#!/bin/bash

#Updated by Tien Ngoc LE updated 2014.Dec.23

#$1: number of Phrases
#$2: path to directory "SRILM_bin"
#NOT USED - > Removed - $3: path to language model (target language)
#$3: path to file "fastnc"
#$4: path to file "RefToCtm.pl" in fastnc
#$5: path to file output

export LC_ALL=C
#for i in Phrase*; do nbest-lattice -nbest $i -write ${i}.wlat; done
#for i in *.wlat;  do wlat-to-pfsg $i > ${i}.pfsg; done
#rename 's/\.wlat\.pfsg/\.pfsg/' *
#for i in *.pfsg; do lattice-tool  -in-lattice $i -write-htk -out-lattice ${i}.htk; done
#for i in *.htk; do lattice-tool -read-htk -in-lattice $i -use-server 6666@localhost -order 5 -write-htk -out-lattice ${i}.ext; done

dem=0
SRILM_BIN=$2
ORDER=5
TOOL_FASTNC=$3
TOOL_REF_TO_CTM=$4
OUTPUT_FILE=$5

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
	#../../../tool/fastnc/scripts/RefToCtm.pl ${i}b
	$TOOL_REF_TO_CTM ${i}b

	for j in *.ctm;
	do
		#./fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ./Results.txt
		#/home/tienle/Documents/Develops/GeTools/WPP-Nodes-Min-Max/fastnc/bin/fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ./Results.txt
		#../../../tool/fastnc/bin/fastnc --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ../../extracted_features/en.column.feature_wpp_nodes_min_max_temp.txt
		$TOOL_FASTNC --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a $OUTPUT_FILE
		#$TOOL_FASTNC --read-ctm $j  --read-lattice  ${i}.wlat.pfsg.htk --compute-posteriors --compute-mesh  --align-ctm-dtw | tee -a ../../extracted_features/en.column.feature_wpp_nodes_min_max_temp.txt
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

