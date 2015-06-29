# -*- coding: utf-8 -*-
"""
Created on Mon May  4 15:01:21 2015
"""

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

# **************************************************************************#
import os
import sys

#when import module/class in other directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  #in order to test with line by line on the server

from common_module.cm_config import load_configuration, load_config_end_user
from common_module.cm_file import get_file_hypothethis_from_output_moses

#Purpose: get content of output of MT system
# **************************************************************************#
if __name__=="__main__":
    #Test case:
    current_config = load_configuration()
    config_end_user = load_config_end_user()

    file_input_path = config_end_user.ONE_BEST_LIST_INCLUDED_ALIGNMENT
    file_output_path = config_end_user.RAW_CORPUS_TARGET_LANGUAGE
    get_file_hypothethis_from_output_moses(file_input_path, file_output_path)

    print('OK')