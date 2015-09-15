#! /bin/bash

#Demo on lent@hestia.imag.fr
#Created by: Tien Ngoc LE
#Date Created: 2014.Dec.14
#Date Updated: .... by ....s

#note: file nay chi copy vao "/home/lent/Develops/Experiments/EMS_FREN_v2"

#path Demo: /home/lent/Develops/Solution/eval_agent/eval_agent/preprocessing
#command line: 
#command demo: 

#Purpose: Preprocessing for MOSES EMS, contains the following functions: 

#Lay phan du lieu de test (EVALUATE)
#Lay so luong train + dev tu dau -> train (dau) + dev (cuoi)
#Buoc: copy & paste -> enter
#Buoc 1

tail -${num_line_test} ${corpus_path}/$file_name_input > ${corpus_path}/${corpus_name_common}-test-${pair_extension}.${input_extension};

head -${num_line_train_dev} ${corpus_path}/$file_name_input > ${corpus_path}/${corpus_name_common}-train-dev-${pair_extension}.${input_extension};

head -${num_line_train} ${corpus_path}/${corpus_name_common}-train-dev-${pair_extension}.${input_extension} > ${corpus_path}/${corpus_name_common}-train-${pair_extension}.${input_extension};

tail -${num_line_dev} ${corpus_path}/${corpus_name_common}-train-dev-${pair_extension}.${input_extension} > ${corpus_path}/${corpus_name_common}-dev-${pair_extension}.${input_extension};

tail -${num_line_test} ${corpus_path}/$file_name_output > ${corpus_path}/${corpus_name_common}-test-${pair_extension}.${output_extension};

head -${num_line_train_dev} ${corpus_path}/$file_name_output > ${corpus_path}/${corpus_name_common}-train-dev-${pair_extension}.${output_extension};

head -${num_line_train} ${corpus_path}/${corpus_name_common}-train-dev-${pair_extension}.${output_extension} > ${corpus_path}/${corpus_name_common}-train-${pair_extension}.${output_extension};

tail -${num_line_dev} ${corpus_path}/${corpus_name_common}-train-dev-${pair_extension}.${output_extension} > ${corpus_path}/${corpus_name_common}-dev-${pair_extension}.${output_extension};

### wrap raw text (not tokenized) To XML (sgm format)
### wrap to sgm for training + tuning + testing
perl ${tienle_tools_path}/wrap_text_to_sgm.perl srcset ${input_extension} ${output_extension} ${corpus_path}/${corpus_name_common}-train-${pair_extension}.${input_extension} ${corpus_path}/${corpus_name_common}-train-${pair_extension}-src.${input_extension}.sgm;

perl ${tienle_tools_path}/wrap_text_to_sgm.perl refset ${input_extension} ${output_extension} ${corpus_path}/${corpus_name_common}-train-${pair_extension}.${output_extension} ${corpus_path}/${corpus_name_common}-train-${pair_extension}-ref.${output_extension}.sgm;

perl ${tienle_tools_path}/wrap_text_to_sgm.perl srcset ${input_extension} ${output_extension} ${corpus_path}/${corpus_name_common}-dev-${pair_extension}.${input_extension} ${corpus_path}/${corpus_name_common}-dev-${pair_extension}-src.${input_extension}.sgm;

perl ${tienle_tools_path}/wrap_text_to_sgm.perl refset ${input_extension} ${output_extension} ${corpus_path}/${corpus_name_common}-dev-${pair_extension}.${output_extension} ${corpus_path}/${corpus_name_common}-dev-${pair_extension}-ref.${output_extension}.sgm;

perl ${tienle_tools_path}/wrap_text_to_sgm.perl srcset ${input_extension} ${output_extension} ${corpus_path}/${corpus_name_common}-test-${pair_extension}.${input_extension} ${corpus_path}/${corpus_name_common}-test-${pair_extension}-src.${input_extension}.sgm;

perl ${tienle_tools_path}/wrap_text_to_sgm.perl refset ${input_extension} ${output_extension} ${corpus_path}/${corpus_name_common}-test-${pair_extension}.${output_extension} ${corpus_path}/${corpus_name_common}-test-${pair_extension}-ref.${output_extension}.sgm;

echo "Done. Have a happy day!!! :)"
