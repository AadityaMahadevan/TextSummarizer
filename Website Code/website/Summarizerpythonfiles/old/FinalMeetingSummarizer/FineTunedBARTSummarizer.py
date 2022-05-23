import transformers
import tensorflow as tf
import os
import pandas as pd
import numpy as np

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
base_dir = str(Path(BASE_DIR))
from transformers import TFAutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from transformers import AutoTokenizer


def get_abstractive_summary(sample_text, checkpoint_path, pretrained_model_name,max_length):
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(pretrained_model_name)
    model.load_weights(base_dir+'/'+checkpoint_path)

    inputs = tokenizer.batch_encode_plus([sample_text], return_tensors='tf', truncation = True, max_length = max_length,  add_special_tokens = False, verbose = True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=5, no_repeat_ngram_size = 2, max_length=max_length)
    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in summary_ids]

    return summary
