#!/bin/bash
#Authors: Tien Ngoc LE & Tan Ngoc LE 

/data/servan/wce_xp/wce_system///tools/wapiti-1.5.0/./wapiti train -a sgd-l1 -i 200 -e 0.00005 -w 6 -p /data/servan/wce_xp/wce_system///wce_system/lib/templates/template.en1 /data/servan/wce_xp/wce_system///wce_system/var/data/CRF_tgt.column.train_file_System_WCE.txt /data/servan/wce_xp/wce_system///wce_system/var/data/CRF_model_with_template1_System_WCE.txt 2>&1 | tee /data/servan/wce_xp/wce_system///wce_system/var/data/CRF_model_training_log_file1_System_WCE.txt
