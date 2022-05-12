import transformers
import tensorflow as tf
import os
import pandas as pd
import numpy as np

from transformers import TFAutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from transformers import AutoTokenizer

pretrained_model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)

model = TFAutoModelForSeq2SeqLM.from_pretrained(pretrained_model_name)
model.load_weights('summarizer-checkpoint.h5')

file_text = open("input.txt", "r")
sample_text = file_text.read()

inputs = tokenizer.batch_encode_plus([sample_text], return_tensors='tf', truncation = False,  add_special_tokens = False, verbose = True)
summary_ids = model.generate(inputs['input_ids'], num_beams=5, no_repeat_ngram_size = 2, max_length=512)
summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in summary_ids]

print(summary)
