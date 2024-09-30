# VELD registry

This is a living collection VELD repositories and containing velds.

The technical concept for the VELD design can be found here: https://zenodo.org/records/13318651

## setup and execution

The github and gitlab API crawlers need access tokens, these are persisted in a `.env` file at the
root directory of this repo and have contents like so: 
```
github_token=<INSERT_TOKEN_HERE>
gitlab_token=<INSERT_TOKEN_HERE>
```

Executed with docker compose: 
```
# newer docker versions:
docker compose up 
# older docker versions with compose being a separate command:
docker-compose up
```

# chain velds

- https://github.com/acdh-oeaw/veld_chain_5_apis_ner_evaluate_old_models
  - [veld.yaml](https://github.com/acdh-oeaw/veld_chain_5_apis_ner_evaluate_old_models/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_chain_6_apis_ner_transform_to_gold
  - [veld.yaml](https://github.com/acdh-oeaw/veld_chain_6_apis_ner_transform_to_gold/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_chain_7_train
  - [veld_convert.yaml](https://github.com/acdh-oeaw/veld_chain_7_train/blob/main/veld_convert.yaml)
  - [veld_publish.yaml](https://github.com/acdh-oeaw/veld_chain_7_train/blob/main/veld_publish.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_chain_7_train/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_chain_9_akp_ner
  - [veld.yaml](https://github.com/acdh-oeaw/veld_chain_9_akp_ner/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_chain_10_apis_ner_to_huggingface
  - [veld.yaml](https://github.com/acdh-oeaw/veld_chain_10_apis_ner_to_huggingface/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_chain_11_fasttext
  - [veld_eval.yaml](https://github.com/acdh-oeaw/veld_chain_11_fasttext/blob/main/veld_eval.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_chain_11_fasttext/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_chain_12_word2vec
  - [veld_eval.yaml](https://github.com/acdh-oeaw/veld_chain_12_word2vec/blob/main/veld_eval.yaml)
  - [veld_preprocess.yaml](https://github.com/acdh-oeaw/veld_chain_12_word2vec/blob/main/veld_preprocess.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_chain_12_word2vec/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_chain_13_udpipe
  - [veld_infer.yaml](https://github.com/acdh-oeaw/veld_chain_13_udpipe/blob/main/veld_infer.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_chain_13_udpipe/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_chain_14_eltec_udpipe_inference
  - [veld_analyse.yaml](https://github.com/acdh-oeaw/veld_chain_14_eltec_udpipe_inference/blob/main/veld_analyse.yaml)
  - [veld_infer.yaml](https://github.com/acdh-oeaw/veld_chain_14_eltec_udpipe_inference/blob/main/veld_infer.yaml)
  - [veld_preprocess.yaml](https://github.com/acdh-oeaw/veld_chain_14_eltec_udpipe_inference/blob/main/veld_preprocess.yaml)
- https://github.com/acdh-oeaw/veld_chain_15_glove
  - [veld_infer.yaml](https://github.com/acdh-oeaw/veld_chain_15_glove/blob/main/veld_infer.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_chain_15_glove/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_chain_16_clscorgi
  - [veld.yaml](https://github.com/acdh-oeaw/veld_chain_16_clscorgi/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki
  - [veld_analyse_evaluation.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_analyse_evaluation.yaml)
  - [veld_jupyter_notebook_fasttext.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_jupyter_notebook_fasttext.yaml)
  - [veld_jupyter_notebook_glove.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_jupyter_notebook_glove.yaml)
  - [veld_jupyter_notebook_word2vec.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_jupyter_notebook_word2vec.yaml)
  - [veld_multi_chain__preprocess.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_multi_chain__preprocess.yaml)
  - [veld_multi_chain__preprocess_train_eval.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_multi_chain__preprocess_train_eval.yaml)
  - [veld_preprocess_clean.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_preprocess_clean.yaml)
  - [veld_preprocess_download_and_extract.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_preprocess_download_and_extract.yaml)
  - [veld_preprocess_lowercase.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_preprocess_lowercase.yaml)
  - [veld_preprocess_remove_punctuation.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_preprocess_remove_punctuation.yaml)
  - [veld_preprocess_sample.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_preprocess_sample.yaml)
  - [veld_preprocess_transform_wiki_json_to_txt.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_preprocess_transform_wiki_json_to_txt.yaml)
  - [veld_train_eval_fasttext.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_train_eval_fasttext.yaml)
  - [veld_train_eval_glove.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_train_eval_glove.yaml)
  - [veld_train_eval_word2vec.yaml](https://github.com/acdh-oeaw/veld_chain_17_train_infer_wordembeddings_multiple_architectures__wiki/blob/main/veld_train_eval_word2vec.yaml)
- https://github.com/acdh-oeaw/veld_chain_18_MARA_load_and_publish_models
- https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc
  - [veld_eval_fasttext.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_eval_fasttext.yaml)
  - [veld_eval_glove.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_eval_glove.yaml)
  - [veld_eval_word2vec.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_eval_word2vec.yaml)
  - [veld_jupyter_notebook_fasttext.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_jupyter_notebook_fasttext.yaml)
  - [veld_jupyter_notebook_glove.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_jupyter_notebook_glove.yaml)
  - [veld_jupyter_notebook_word2vec.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_jupyter_notebook_word2vec.yaml)
  - [veld_preprocess_clean.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_preprocess_clean.yaml)
  - [veld_preprocess_lowercase.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_preprocess_lowercase.yaml)
  - [veld_preprocess_remove_punctuation.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_preprocess_remove_punctuation.yaml)
  - [veld_preprocess_sample.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_preprocess_sample.yaml)
  - [veld_preprocess_strip.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_preprocess_strip.yaml)
  - [veld_train_fasttext.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_train_fasttext.yaml)
  - [veld_train_glove.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_train_glove.yaml)
  - [veld_train_word2vec.yaml](https://github.com/acdh-oeaw/veld_chain_19_train_infer_wordembeddings_multiple_architectures__amc/blob/main/veld_train_word2vec.yaml)

# code velds

- https://github.com/acdh-oeaw/veld_code_3_apis_ner_evaluate_old_models
  - [veld.yaml](https://github.com/acdh-oeaw/veld_code_3_apis_ner_evaluate_old_models/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_code_4_apis_ner_transform_to_gold
  - [veld.yaml](https://github.com/acdh-oeaw/veld_code_4_apis_ner_transform_to_gold/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_code_5_simple_docker_test
  - [veld.yaml](https://github.com/acdh-oeaw/veld_code_5_simple_docker_test/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_code_7_train_spacy_ner
  - [veld_convert.yaml](https://github.com/acdh-oeaw/veld_code_7_train_spacy_ner/blob/main/veld_convert.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_code_7_train_spacy_ner/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_code_9_jupyter_notebook_base
  - [veld.yaml](https://github.com/acdh-oeaw/veld_code_9_jupyter_notebook_base/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_code_10_akp_ner
  - [veld.yaml](https://github.com/acdh-oeaw/veld_code_10_akp_ner/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_code_11_publish_to_hf
  - [veld.yaml](https://github.com/acdh-oeaw/veld_code_11_publish_to_hf/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_code_12_fasttext
  - [veld_jupyter_notebook.yaml](https://github.com/acdh-oeaw/veld_code_12_fasttext/blob/main/veld_jupyter_notebook.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_code_12_fasttext/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_code_13_word2vec
  - [veld_jupyter_notebook.yaml](https://github.com/acdh-oeaw/veld_code_13_word2vec/blob/main/veld_jupyter_notebook.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_code_13_word2vec/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_code_14_we_evaluation
  - [veld_analyse_evaluation.yaml](https://github.com/acdh-oeaw/veld_code_14_we_evaluation/blob/main/veld_analyse_evaluation.yaml)
  - [veld_eval_fasttext.yaml](https://github.com/acdh-oeaw/veld_code_14_we_evaluation/blob/main/veld_eval_fasttext.yaml)
  - [veld_eval_glove.yaml](https://github.com/acdh-oeaw/veld_code_14_we_evaluation/blob/main/veld_eval_glove.yaml)
  - [veld_eval_word2vec.yaml](https://github.com/acdh-oeaw/veld_code_14_we_evaluation/blob/main/veld_eval_word2vec.yaml)
- https://github.com/acdh-oeaw/veld_code_15_udpipe
  - [veld_infer.yaml](https://github.com/acdh-oeaw/veld_code_15_udpipe/blob/main/veld_infer.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_code_15_udpipe/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_code_16_xml_xslt_transformer
  - [veld.yaml](https://github.com/acdh-oeaw/veld_code_16_xml_xslt_transformer/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_code_17_glove
  - [veld_jupyter_notebook.yaml](https://github.com/acdh-oeaw/veld_code_17_glove/blob/main/veld_jupyter_notebook.yaml)
  - [veld_train.yaml](https://github.com/acdh-oeaw/veld_code_17_glove/blob/main/veld_train.yaml)
- https://github.com/acdh-oeaw/veld_code_18_clscorgi
- https://github.com/acdh-oeaw/veld_code_19_we_preprocessing
  - [veld_preprocess_clean.yaml](https://github.com/acdh-oeaw/veld_code_19_we_preprocessing/blob/main/veld_preprocess_clean.yaml)
  - [veld_preprocess_lowercase.yaml](https://github.com/acdh-oeaw/veld_code_19_we_preprocessing/blob/main/veld_preprocess_lowercase.yaml)
  - [veld_preprocess_remove_punctuation.yaml](https://github.com/acdh-oeaw/veld_code_19_we_preprocessing/blob/main/veld_preprocess_remove_punctuation.yaml)
  - [veld_preprocess_sample.yaml](https://github.com/acdh-oeaw/veld_code_19_we_preprocessing/blob/main/veld_preprocess_sample.yaml)
  - [veld_preprocess_strip.yaml](https://github.com/acdh-oeaw/veld_code_19_we_preprocessing/blob/main/veld_preprocess_strip.yaml)
- https://github.com/acdh-oeaw/veld_code_20_wikipedia_nlp_preprocessing
  - [veld_download_and_extract.yaml](https://github.com/acdh-oeaw/veld_code_20_wikipedia_nlp_preprocessing/blob/main/veld_download_and_extract.yaml)
  - [veld_transform_wiki_json_to_txt.yaml](https://github.com/acdh-oeaw/veld_code_20_wikipedia_nlp_preprocessing/blob/main/veld_transform_wiki_json_to_txt.yaml)

# data velds

- https://github.com/acdh-oeaw/veld_data_5_apis_oebl__ner_gold
  - [veld.yaml](https://github.com/acdh-oeaw/veld_data_5_apis_oebl__ner_gold/blob/main/veld.yaml)
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_6_apis_ner_models
  - [veld.yaml](https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_6_apis_ner_models/blob/main/veld.yaml)
- https://github.com/acdh-oeaw/veld_data_7_akp_ner_linkedcat
  - [veld.yaml](https://github.com/acdh-oeaw/veld_data_7_akp_ner_linkedcat/blob/main/veld.yaml)
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_8_fasttext_models
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_9_wikpedia_we_training_data
- https://github.com/acdh-oeaw/veld_data_10_we_evaluation
  - [evaluation_gold_data/capitalized/veld.yaml](https://github.com/acdh-oeaw/veld_data_10_we_evaluation/blob/main/evaluation_gold_data/capitalized/veld.yaml)
  - [evaluation_gold_data/lowercase/veld.yaml](https://github.com/acdh-oeaw/veld_data_10_we_evaluation/blob/main/evaluation_gold_data/lowercase/veld.yaml)
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_11_word2vec_models
- https://github.com/acdh-oeaw/veld_data_12_eltec_original_selection
  - [veld.yaml](https://github.com/acdh-oeaw/veld_data_12_eltec_original_selection/blob/main/veld.yaml)
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_13_eltec_txt_transformed
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_14_udpipe_models
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_15_eltec_udpipe_conllu
- https://github.com/acdh-oeaw/veld_data_16_eltec_conllu_stats
  - [veld.yaml](https://github.com/acdh-oeaw/veld_data_16_eltec_conllu_stats/blob/main/veld.yaml)
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_17_glove_models
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_18_amc_we_training_data
- https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_19_mara_models
  - [veld.yaml](https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_data_19_mara_models/blob/main/veld.yaml)
- https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner
  - [veld.yaml](https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner/blob/main/veld.yaml)

