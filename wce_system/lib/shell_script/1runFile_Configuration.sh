######################################################################
### Authors: Tien Ngoc Le
### Homepage: tienhuong.weebly.com
### Email: letien.dhcn@gmail.com; letan.dhcn@gmail.com
### Created Date: 2014.05.12
### Updated Date: 2014.Dec.07
######################################################################

#Command for config the environment variables: source ./config_runFile.sh

#note: file nay chi copy vao "/home/lent/Develops/Experiments/EMS_FREN_v2"

#This folder-names should be updated when you would like to do with other experiment!!! :)
# Tuong ung voi file config co cac bien sau:
#working-dir=$experiments-path/EMS6
#corpus-name-dir="corpusFRVI_2" 
#corpus-name-common="corpusFRVI"
#Do do, cac bien phai co gia tri tuong ung voi cac bien phai GIONG NHAU !!!

export experiment_folder_name=EMS_FREN_v2;
export corpus_folder_name=corpusFREN_v2;
export corpus_name_common=corpusFREN;
export corpus_resource=${corpus_name_common};

export input_extension=fr;
export output_extension=en;
export pair_extension=fren;

### Paths
#export develops_path=/home/tienle/Documents/Develops;
export develops_path=/home/lent/Develops;

#TienNLe added 2014.05.17, updated 2014.Dec.07
export devtools_path=${develops_path}/DevTools;
export data_path=${develops_path}/Data;
export experiments_path=${develops_path}/Experiments;

export experiments_path=${experiments_path}/${experiment_folder_name};
export tienle_tools_path=${devtools_path}/tienle_tools;
export corpus_path=${data_path}/${corpus_folder_name};
export moses_scripts_path=${devtools_path}/moses/scripts;

#TreeTagger (FR)
#/home/tienle/Documents/Develops/DevTools/treetagger
export treetagger_path=${devtools_path}/treetagger;
#/home/tienle/Documents/Develops/DevTools/mosesdecoder/scripts/training/wrappers
#TreeTagger Just For MOSES
export make_pos_treetagger_path=${moses_scripts_path}/training/wrappers;

#/home/tienle/Documents/Develops/DevTools/treetagger
#export treetagger_path=${devtools_path}/treetagger
export treetagger_BIN_path=${treetagger_path}/bin
export treetagger_CMD_path=${treetagger_path}/cmd

# Preparing data for Demo 

# Organizing the corpus from raw-text file to files that are uses to train/dev/test with 90%, 5% and 5% respectively.
# num_line_train_dev=num_line_train + num_line_dev
#export num_line_all=5000;
#export num_line_train=1000;
#export num_line_dev=50;
#export num_line_train_dev=4900;
#export num_line_test=50;

export num_line_all=1661012;
#13467
export num_line_train=1577079;
export num_line_dev=83052;
export num_line_train_dev=1660131;
export num_line_test=881;

export file_name_input=${corpus_resource}.${input_extension};
export file_name_input_word=${corpus_resource}_word.${input_extension};
export file_name_output=${corpus_resource}.${output_extension};
