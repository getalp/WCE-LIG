#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE & Christophe Servan (ngoc-tien.le@imag.fr, christophe.servan@imag.fr)
# Supervisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

Our solution contains three main-steps:
Step 1: Preprocessing
Step 2: Extracting features
Step 3: Estimating confidences in Word-level

- input corpus (French-English)
    + source language
    + target language
    + post-edition
    + output from Google Translator
    + output from Bing Translator
    + output from tool MOSES: n-best-list & 1-best-list

- output: After using our WCE system, we have result file that contains label of each word in given input corpus target language. Note: B (Insert label), Other labels are G

- Tutorial:
+ Set the WCE_ROOT environment variable to the place where is this Readme file.

+ Running three Phases (Preprocessing, Extracting Features and Measuring Confidence):
$ python3  $WCE_ROOT/wce_system/solution/lauching_solution.py

+ Processing Phase:
$ python3 $WCE_ROOT/wce_system/preprocessing/pre_processing.py

+ Extracting Feature Phase:
$ python3 $WCE_ROOT/wce_system/feature/extract_all_features.py

+ Measuring Confidence Phase:
$ python3 $WCE_ROOT/wce_system/metrics/demo_metrics.py

*** For example:
- Input: Using FR-EN within 10881 sentences in source language, target language and post-edition.

- Output: file "$WCE_ROOT/wce_system/var/data/CRF_model_testing_log_file1_System_WCE_manual.txt"
*** Template_1_System_WCE classifier Good/Bad:
X-Bad = 1640 	 Y-Bad = 3395 	 Z-Bad = 4537
X-Good = 15409 	 Y-Good = 18306 	 Z-Good = 17164
B 	 Pr=0.4831 	 Rc=0.3615 	 F1=0.4135
G 	 Pr=0.8417 	 Rc=0.8978 	 F1=0.8688
