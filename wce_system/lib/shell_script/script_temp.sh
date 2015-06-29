#!/bin/bash
#Authors: Tien Ngoc LE & Tan Ngoc LE 

/local/wce_system//tools/wapiti-1.5.0/./wapiti label -c -s -p /local/wce_system//wce_system/var/data/CRF_tgt.column.test_file_System_WCE.txt -m /local/wce_system//wce_system/var/data/CRF_model_with_template6_System_WCE.txt /local/wce_system//wce_system/var/data/CRF_model_result_testing6_System_WCE.txt 2>&1 | tee /local/wce_system//wce_system/var/data/CRF_model_testing_log_file6_System_WCE.txt
