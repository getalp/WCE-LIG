## YAML Template.
---

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

language_support:
    source_language: en, fr, es
    target_language: en, fr, es

language_pair:    
    ##input corpus            
    input_raw_corpus_source_language: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/raw_corpus.src
    input_raw_corpus_target_language: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/raw_corpus.tgt
    post_edition_of_machine_translation_sentences_target_language: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/post_edition.tgt   
    post_edition_after_tokenizing_lowercasing:  <%= ENV['WCE_ROOT'] %>/wce_system/var/data/post_edition_after_tokenizing_lowercasing.tgt    
    post_edition_after_tokenizing_lowercasing_after_adding_sentence_id:  <%= ENV['WCE_ROOT'] %>/wce_system/var/data/post_edition_after_tokenizing_lowercasing.tgt_after_adding_sentence_id
    list_of_id_sentences_asr:  <%= ENV['WCE_ROOT'] %>/wce_system/var/data/list_of_id_sentences_asr.txt
    hypothesis_asr_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/hypothesis_asr_10_tramots.txt
    reference_asr_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/reference_asr_test_refASR.txt
    
    ###for verifying the result     
    target_mt_all_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt-mt-all.en
    post_edition_of_machine_translation_sentences_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.post_edition.tgt
    
    ##output from Google & Bing Translator
    google_translate_corpus: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_Google_Translator.tgt
    bing_translate_corpus: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_Bing_Translator.tgt
    
    ##language model           
    language_model_tgt: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/lm_5gram.tgt
    language_model_src: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/lm_5gram.src
    
    ##Tam thoi dung duong dan tuyet doi cho file moses.ini - version 2014
    #moses_ini: /home/lent/Develops/Experiments/EMS_FREN_v1/tuning/moses.ini.1
    
    mt_hypothesis_output_1_bestlist_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/mt_hypothesis_output_1_bestlist_included_alignment.tgt
    mt_hypothesis_output_1_bestlist: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/mt_hypothesis_output_1_bestlist.tgt
    mt_hypothesis_output_1_bestlist_included_alignment_ape: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/mt_hypothesis_output_1_bestlist_included_alignment_ape.tgt
    
    mt_hypothesis_output_nbestlist_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/mt_hypothesis_output_nbestlist_included_alignment.tgt
    mt_hypothesis_output_nbestlist: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/mt_hypothesis_output_nbestlist.tgt
    
    src_ref_test_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.src        
    pattern_ref_test_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing
    target_ref_test_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.tgt
    src_target_ref_test_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.src_tgt    
    pattern_ref_test_format_row_ape: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing_ape
    
    target_ref_test_format_row_after_adding_sentence_id: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.tgt_after_adding_sentence_id
    
    ##corpus format column
    src_ref_test_format_col: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.col.src    
    target_ref_test_format_col: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.col.tgt
        
    # Output from TOOLs
    ##alignment output of Giza
    word_alignment_using_giza: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/word_alignment_using_giza.txt
    word_alignment_using_giza_after_optimising: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/word_alignment_using_giza_after_optimizing.txt
        
    #TreeTagger output
    src_ref_test_output_treetagger_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.treetagger.format.row.src
    target_ref_test_output_treetagger_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.treetagger.format.row.tgt
            
    ##cach 2: dung "make-factor-pos" de lay ket qua theo dong, roi chuyen sang dinh dang cot
    ##surgeons	NNS	surgeon
    src_ref_test_output_treetagger_format_col: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.treetagger.format.col.src
    target_ref_test_output_treetagger_format_col: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.treetagger.format.col.tgt    
    
    ##lib
    list_punctuations: <%= ENV['WCE_ROOT'] %>/wce_system/lib/list_punctuations.txt
    list_stop_words_en: <%= ENV['WCE_ROOT'] %>/wce_system/lib/stopwords/a_full_stopwords_en.txt
    list_stop_words_fr: <%= ENV['WCE_ROOT'] %>/wce_system/lib/stopwords/stopwords_fr.txt
    list_stop_words_es: <%= ENV['WCE_ROOT'] %>/wce_system/lib/stopwords/a_full_stopwords_es.txt

    ##Extracting Phase    
    probability_hypothesis_row_corpus: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/mt_hypothesis_output.probability.txt
    probability_row_corpus_source_language: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.probability.src    
    number_of_occurrences_stem: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_number_of_occurrences_stem.txt
    number_of_occurrences_word: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_number_of_occurrences_word.txt
    numeric: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_numeric.txt
    occur_in_google_translate: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_occur_in_google_translate.txt
    occur_in_bing_translate: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_occur_in_bing_translate.txt    
    polysemy_count_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_count_target.txt
    polysemy_count_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_count_source.txt
    proper_name: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_proper_name.txt
    punctuation: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_punctuation.txt
    stop_word: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_stop_word.txt
    longest_target_gram_length: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_longest_target_gram_length.txt
    backoff_behaviour: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_backoff_behaviour.txt    
    temp_longest_source_gram_length_not_aligned_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_temp_longest_source_gram_length_not_aligned_target.txt
    temp_longest_source_gram_length_not_aligned_target_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.row.feature_temp_longest_source_gram_length_not_aligned_target.txt
    longest_source_gram_length_aligned_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_longest_source_gram_length_aligned_target.txt
    alignment_features: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_alignment_features.txt
    unknown_lemma: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_unknown_lemma.txt
    features_asr_not_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/column.features_asr_not_alignment.txt
    features_asr_aligned: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/column.features_asr_aligned.txt
    features_asr_aligned_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/column.features_asr_aligned_last.txt
    alignment_src_tgt_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/alignment_src_tgt_format_row.txt
    alignment_tgt_src_format_row: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/alignment_tgt_src_format_row.txt
    babel_net_output_corpus_tgt_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_last.txt
    babel_net_output_corpus_tgt_last_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_pattern
    backoff_behaviour_after_converting_to_int: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_backoff_behaviour_after_converting_to_int.txt    
    alignment_features_after_converting_to_int: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_alignment_features_after_converting_to_int.txt
    
    directory_with_extracted_features_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/ape_wmt15_testData/
    
    ##neu muon cap nhat duong dan "wpp_nodes_min_max_temp" thi phai cap nhat trong file "nbestToLattice.sh" in folder "lib/shell_script"
    #wpp_nodes_min_max_temp: tgt.column.feature_wpp_nodes_min_max.txt --> update in file "nbestToLattice.sh" in folder "lib/shell_script"
    wpp_nodes_min_max_temp: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_wpp_nodes_min_max_temp.txt
    wpp_nodes_min_max: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_wpp_nodes_min_max.txt
    wpp_exact:  <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_wpp_exact.txt
            
    ## Berkely Parser --> Constituent Label & Distance to Root, NULL link (EN)        
    ##constituent_first_en_temp: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_first_en_temp.txt
    ##constituent_last_en_temp: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_last_en_temp.txt    
    ##constituent_first_en: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_first_tgt.txt
    ##constituent_last_en: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_last_tgt.txt
    #constituent_tree: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_tree.txt
    constituent_tree_temp: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_tree_temp.txt    
    distance_to_root: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_distance_to_root.txt
    constituent_label: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_label.txt
    constituent_label_after_converting_to_int: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_constituent_label_after_converting_to_int.txt
    
    ##for independent target language
    babel_net_corpus: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_pos.babelnet
    babel_net_output_corpus: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_babelnet
    babel_net_output_corpus_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_filtering
    babel_net_output_corpus_target_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_filtering_last
    
    ##for OAR
    babel_net_corpus_oar: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_pos.babelnet_oar
    babel_net_output_corpus_oar: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_babelnet_oar
    babel_net_output_corpus_oar_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_filtering_oar
    babel_net_output_corpus_tgt_oar_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_filtering_oar_last
    
    ##for spanish (es)        
    babel_net_corpus_es: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_pos.babelnet_es
    babel_net_output_corpus_es: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_babelnet_es
    babel_net_output_corpus_es_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_filtering_es

    ##for english (en)              
    babel_net_corpus_en: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_pos.babelnet_en
    babel_net_output_corpus_en: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_babelnet_en
    babel_net_output_corpus_en_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_filtering_en

    ##for french (fr)    
    babel_net_corpus_fr: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/tgt.column.feature_pos.babelnet_fr
    babel_net_output_corpus_fr: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_babelnet_fr
    babel_net_output_corpus_fr_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_polysemy_after_filtering_fr
    
    ##TARGET_REF_TEST_FORMAT_ROW
    berkeley_parser_input: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/target_ref_test_format_row.replace_parenthesis.txt
    
    ##for tool Terpa
    hypothesis_set_sgm: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt-mt-output.sgm
    post_edition_sgm: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt-pe-output.sgm
    label_output: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_label.txt
    label_output_tercom_original: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_label_tercom_original.txt
    label_output_tercom_wce: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_label_tercom_wce.txt    
    label_output_tercom_wce_verify: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_label_tercom_wce_verify.txt
    terp_pra_from_wce_slt_lig: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/Labels-MT
    tercom_result: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tercom_result
    tercom_shifted_sentences: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tercom_shifted_sentences
    tercpp_result: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tercpp_result
    label_output_tercpp_original: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_label_tercpp_original.txt
    label_output_tercom_ape: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_label_tercom_ape.txt
    
    ##for tool wapiti
    output_merged_features: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features.txt
    output_merged_features_wmt15: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15.txt
    output_merged_features_for_testing_model: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_for_testing_model.txt
    output_merged_features_wmt15_after_converting_to_int: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_after_converting_to_int.txt
    output_merged_features_wmt15_after_converting_to_int_within_label:  <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_after_converting_to_int_within_label.txt
    output_merged_features_wmt15_after_converting_to_int_and_remove_empty_line: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_after_converting_to_int_and_remove_empty_line.txt
    output_merged_features_wmt15_for_pca: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_for_pca.txt
    output_merged_features_wmt15_for_pca_after_pca: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_for_pca_after_PCA.txt    
    output_merged_features_wmt15_after_pca_last: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_after_PCA_last.txt    
    output_merged_features_wmt15_after_pca_last_and_label: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_after_PCA_last_and_label.txt    
    output_merged_features_wmt15_after_pca_last_and_label_and_remove_empty_line: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt15_after_PCA_last_and_label_and_remove_empty_line.txt    
    
    output_merged_features_wmt14_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt14_wmt13.txt
    output_merged_features_wmt14_wmt13_after_converting_to_int: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.merged_features_wmt14_wmt13_after_converting_to_int.txt
    
    train_file_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.train_file
    dev_file_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.dev_file
    test_file_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_tgt.column.test_file
    log_file_training_wapiti: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_model_training_log_file
    result_testing_wapiti: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_model_result_testing
    result_labeling_wapiti: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_model_result_labeling
    log_file_testing_wapiti: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_model_testing_log_file    
    crf_message_output: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/logfile_phase_metrics_baselines_and_CRF.txt
    model_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_model_with_template
    template_path: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/template.en    
    result_labeling_threshold: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/result_labeling_with_given_threshold
    result_threshold_best: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/result_threshold_best.txt
    
    template_path_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_subset_template_subset
    result_word_label_using_threshold_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/CRF_subset_word_label_using_threshold_path    
    result_feature_selection: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/feature_selection.txt
    
    ##Boosting method
    training_cross_validation_path_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_train_data_cross_validation_subset
    developing_cross_validation_path_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_dev_data_cross_validation_subset
    testing_cross_validation_path_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_test_data_cross_validation_subset
    boost_template_path_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_subset_template_subset
    
    training_corpus_for_boosting_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_corpus.data
    training_names_for_boosting_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_corpus.names
    training_corpus_name: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_corpus
    
    boosting_training_log_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_training_log.txt
    boosting_testing_log_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_testing_log.txt
    result_testing_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/boosting_result_testing.txt
    
    ##ASR tasks
    features_values_asr_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/testNEW.csv
    after_sorting_features_values_asr_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/after_sorting_features_values_asr.csv
    output_sentences_not_encoding: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_sentences_not_encoding.txt
    output_sentences_within_encoding: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_sentences_within_encoding.txt
    output_format_row_within_encoding: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_format_row_within_encoding.txt
    output_format_column_within_encoding: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_format_column_within_encoding.txt
    output_format_column_result_diff: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_format_column_result_diff.txt
    sclite_files_directory_path: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/sclite_files/        
    error_words_output: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/asr_error_words_output.txt
    
    ##for Giza++
    target_source_A3_final: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/src_tgt.A3.final
    #target_source_A3_final: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt_src.A3.final        
    path_to_corpus: <%= ENV['WCE_ROOT'] %>/wce_system/var/data
    source_corpus_name: output_preprocessing.src
    target_corpus_name: output_preprocessing.tgt
    
    ##MOSES
    model_dir_path: <%= ENV['WCE_ROOT'] %>/wce_system/var/data
        
    ##for verifying the result of moses 2009
    input_raw_corpus_source_language_testing_moses2009: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/src-ref-all.fr
    src_ref_test_format_row_testing_moses2009: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/output_preprocessing_testing_moses2009.src
    tgt_mt_all_format_row_testing_moses2009: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/tgt-mt-all.en
    tgt_mt_all_after_lc_tok_format_row_testing_moses2009: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/tgt-mt-all.en_after_lc_tok
    translated_model_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/src-ref-all.fr.translated_model
    translated_output10881_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/src-ref-all.fr.translated_output10881
    translated_model_no_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/src-ref-all.fr.translated_model_no_included_alignment 
    translated_output10881_no_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/src-ref-all.fr.translated_output10881_no_included_alignment
    log_comparing_tgt_mt_all_after_lc_tok_and_translated_model_no_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/log_comparing_tgt_mt_all_after_lc_tok_and_translated_model_no_included_alignment
    log_comparing_tgt_mt_all_after_lc_tok_and_translated_output10881_no_included_alignment: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/log_comparing_tgt_mt_all_after_lc_tok_and_translated_output10881_no_included_alignment
    post_edition_for_checking_moses_2009: <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/tgt-pe-all.en
    post_edition_after_tokenizing_lowercasing_checking_moses_2009:  <%= ENV['WCE_ROOT'] %>/wce_system/corpus/checking_moses_2009/tgt-pe-all.en_after_lc_tok
    
    ##For wmt15
    features_test_wmt15: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_test_wmt15.txt
        
    ##Preprocessing for wmt14 & wmt13
    features_test_wmt14: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_test_wmt14.txt
    features_test_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_test_wmt13.txt
    features_train_wmt14: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt14.txt
    features_train_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt13.txt
    features_train_wmt14_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt14_wmt13.txt
    features_test_wmt14_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_test_wmt14_wmt13.txt
    features_train_wmt14_wmt13_test_wmt14: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt14_wmt13_test_wmt14.txt
    features_train_wmt14_wmt13_test_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt14_wmt13_test_wmt13.txt
    features_train_wmt14_test_wmt14: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt14_test_wmt14.txt
    features_train_wmt13_test_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt13_test_wmt13.txt
    features_train_wmt15_14_13_test_wmt: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/features_train_wmt15_14_13_test_wmt.txt
    
    wmt14_train_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_train_source.txt
    wmt14_train_source_temp: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_train_source_temp.txt
    wmt14_train_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_train_target.txt
    wmt14_train_tag: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_train_tag.txt
    wmt14_test_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_test_source.txt
    wmt14_test_source_temp: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_test_source_temp.txt
    wmt14_test_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_test_target.txt
    wmt14_test_tag: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_test_tag.txt
    
    wmt13_train_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt13_train_source.txt    
    wmt13_train_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt13_train_target.txt
    wmt13_train_tag: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt13_train_tag.txt
    wmt13_test_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt13_test_source.txt    
    wmt13_test_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt13_test_target.txt
    wmt13_test_tag: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt13_test_tag.txt
    
    wmt14_wmt13_train_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_train_source.txt
    wmt14_wmt13_train_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_train_target.txt
    wmt14_wmt13_train_tag: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_train_tag.txt
    wmt14_wmt13_test_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_test_source.txt
    wmt14_wmt13_test_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_test_target.txt
    wmt14_wmt13_test_tag: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_test_tag.txt
    wmt14_wmt13_train_test_source: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_train_test_source.txt
    wmt14_wmt13_train_test_target: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_train_test_target.txt
    wmt14_wmt13_train_test_tag: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/wmt14_wmt13_train_test_tag.txt
    
    label_output_from_extracted_features: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/tgt.column.feature_label_output_from_extracted_features.txt
    
    ## Log paths
    solution_message_output: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/logfile_phase_all.txt
    preprocessing_message_output: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/logfile_phase_preprocessing.txt
    result_message_output: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/logfile_phase_extracting_features.txt
    verify_result_old_and_new: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/result_verify_result_old_and_new.txt    
    f_measure_result_baseline: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/f_measure_result_baseline.txt
    baseline_wmt15: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/baseline_wmt15.txt
    baseline_wmt14_wmt13: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/baseline_wmt14_wmt13.txt
    baseline_test_model_crf: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/baseline_test_model_crf.txt
    result_message_output_ape: <%= ENV['WCE_ROOT'] %>/wce_system/var/log/logfile_phase_extracting_features.txt.ape
    
    ## For OAR
    target_ref_test_output_treetagger_format_col_pattern:  <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_preprocessing.treetagger.format.col.tgt_pattern
    merged_files:  <%= ENV['WCE_ROOT'] %>/wce_system/var/data/merged_files.txt
    
    ## For APE 2015
    file_output_pattern: <%= ENV['WCE_ROOT'] %>/wce_system/var/data/output_pattern
    
    
tools:                  
    ##Shell script in directory "lib"    
    tool_create_probability_each_word_from_language_model: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/create_probability_each_word_from_language_model.sh
    tool_create_longest_target_gram_length: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/create_longest_target_gram_length.sh
    
    tool_n_best_to_lattice: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/nbestToLattice.sh
        
    ##script_temp
    script_temp: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/script_temp.sh
        
    ##tool lingua nay khong huu dung
    ##tool Lingua-LinkParser-1.17 + link-grammar-4.8.6 --> Constituent Label & Distance to Root, NULL link (EN)
    ##/home/lent/Develops/Solution/eval_agent/tool/Lingua-LinkParser-1.17/scripts
    ##tool_get_constituent_first: <%= ENV['WCE_ROOT'] %>/wce_system/<%= ENV['WCE_ROOT'] %>/wce_system/tool/Lingua-LinkParser-1.17/scripts/getConstituentTree_head.sh
    ##tool_get_constituent_last: <%= ENV['WCE_ROOT'] %>/wce_system/<%= ENV['WCE_ROOT'] %>/wce_system/tool/Lingua-LinkParser-1.17/scripts/getConstituentTree_tail.sh
    
    ## Berkeley Parser    
    ## for preprocessing for EN before using Berkeley Parser
    replace_parenthesis: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/replace_parenthesis.sh
        
    ## pre processing:
    tool_pre_processing: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/pre_processing.sh
    tool_pre_processing_lowercasing: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/pre_processing_lowercasing.sh
    
    ##TreeTagger
    tool_tree_tagger: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/make-factor-pos.tree-tagger-TienLe-TanLe.perl    
    customize_output_treetagger: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/customize_result_after_using_treetagger.sh
    
    ## Terp-a    
    customize_input_before_using_terpa: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/customize_input_before_using_terpa.sh    
    wrap_text_to_sgm: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/wrap_text_to_sgm.perl    
    terp_pra: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/terp.pra
    tool_tercom: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/tercom_wmt.sh
    
    ## Booting
    tool_boosting_path: <%= ENV['WCE_ROOT'] %>/wce_system/<%= ENV['WCE_ROOT'] %>/wce_system/tool/bonzaiboost/./bonzaiboost-i386-linux64-v1.6.9    
    
    ## ASR tasks    
    tool_diff: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/create_diff_asr_wce.sh
    tool_analyse_erreurs: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/AnalyserErreursAvecPRF_EtTaggerLesFichiersRES.pl
    
    ##Giza++
    tool_giza: <%= ENV['WCE_ROOT'] %>/wce_system/lib/shell_script/get_alignment_by_giza.sh
    
    ## Feature Selection  (yet updated)
    #alignment_features: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/alignment_features
    alignment_context_pos: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/alignment_context_pos
    alignment_context_stem: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/alignment_context_stem
    alignment_context_word: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/alignment_context_word
    source_pos: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/source_pos
    source_stem: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/source_stem
    source_word: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/source_word
    target_pos: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/target_pos
    target_stem: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/target_stem
    target_word: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/target_word

    backoff_behaviour: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/backoff_behaviour
    constituent_label: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/constituent_label
    distance_to_root: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/distance_to_root
    longest_source_gram_length: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/longest_source_gram_length
    longest_target_gram_length: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/longest_target_gram_length
    max_en: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/max_en
    min_en: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/min_en
    nodes: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/nodes
    number_of_occurrences_stem: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/number_of_occurrences_stem
    number_of_occurrences_word: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/number_of_occurrences_word
    numeric: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/numeric
    occur_in_bing_translator: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/occur_in_bing_translator
    occur_in_google_translator: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/occur_in_google_translator
    polysemycount_target: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/polysemycount_target
    proper_name: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/proper_name
    punctuation: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/punctuation
    stop_word: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/stop_word
    unknown_lemma: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/unknown_lemma
    wpp_any: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/wpp_any
    wpp_exact: <%= ENV['WCE_ROOT'] %>/wce_system/lib/templates/wpp_exact
    
    
