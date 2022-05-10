# %%
import os
import pandas as pd
import numpy as np
import re
import os
import random
import string

# %%
from transformers import TFAutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from transformers import AdamWeightDecay
from transformers.keras_callbacks import KerasMetricCallback
from tensorflow.keras.callbacks import TensorBoard

# %%
from sklearn.model_selection import train_test_split
import tensorflow as tf



# %%
import transformers
import datasets
from datasets import load_dataset, load_metric
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig

# %%
import nltk


# %%
df = pd.read_csv("BBCarticles_csv.csv", encoding="ISO-8859-1")
df.head()

# %%
df = df.dropna().reset_index()
df['Text'] = df['Text'].apply(lambda x: x.replace('\n',' '))
df['Summary'] = df['Summary'].apply(lambda x: x.replace('\n',' '))
df.head()
print("Current Shape ", df)

# %%
truncated_df = df.head(30)
df = truncated_df
print(df.shape)

# %%
train, test = train_test_split(df, test_size=0.1, random_state=42)
print(len(train), len(test))

# %%
train.head()

# %%
pretrained_model_name = "facebook/bart-base"

# %%
metric = load_metric("rouge")
metric

# %%
def show_random_example(df):
    rand = random.randint(0,df.shape[0])
    print("\nExample number: ", rand)
    sample_text = df.iloc[rand,2]
    gold_summary = df.iloc[rand,1]
    print("\nText: ", sample_text)
    print("\nGold Summary: ", gold_summary)

# %%
show_random_example(df)

# %% [markdown]
# # Preprocessing the dataset

# %%
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)

# %%
tokenizer("This is a test sentence")

# %%
max_input_length = 1024
max_target_length = 512

# %%
def preprocess_function(examples):
    inputs = [doc for doc in examples["Text"]]
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            examples["Summary"], max_length=max_target_length, truncation=True
        )

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# %%
tds = Dataset.from_pandas(train)
vds = Dataset.from_pandas(test)
ds = DatasetDict()

ds['train'] = tds
ds['validation'] = vds

print(ds)

# %%
tokenized_datasets = ds.map(preprocess_function, batched=True)

# %%
print(tokenized_datasets)

# %%
model = TFAutoModelForSeq2SeqLM.from_pretrained(pretrained_model_name)

# %%
batch_size =2
learning_rate = 2e-5
weight_decay = 0.01
epochs = 1

model_name = "bart-fine-tuned"

# %%
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="tf")

# %%
tokenized_datasets["train"]

# %%
train_dataset = tokenized_datasets["train"].to_tf_dataset(
    batch_size=batch_size,
    columns=["input_ids", "attention_mask", "labels"],
    shuffle=True,
    collate_fn=data_collator,
)
validation_dataset = tokenized_datasets["validation"].to_tf_dataset(
    batch_size=batch_size,
    columns=["input_ids", "attention_mask", "labels"],
    shuffle=False,
    collate_fn=data_collator,
)
# generation_dataset = (
#     tokenized_datasets["validation"]
#     .shuffle()
#     .select(list(range(200)))
#     .to_tf_dataset(
#         batch_size=8,
#         columns=["input_ids", "attention_mask", "labels"],
#         shuffle=False,
#         collate_fn=data_collator,
#     )
# )

# %%
optimizer = AdamWeightDecay(learning_rate=learning_rate, weight_decay_rate=weight_decay)

# %%
model.compile(optimizer=optimizer)

# %%
def metric_fn(eval_predictions):
    predictions, labels = eval_predictions
    decoded_predictions = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    for label in labels:
        label[label < 0] = tokenizer.pad_token_id  # Replace masked label tokens
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    # Rouge expects a newline after each sentence
    decoded_predictions = [
        "\n".join(nltk.sent_tokenize(pred.strip())) for pred in decoded_predictions
    ]
    decoded_labels = [
        "\n".join(nltk.sent_tokenize(label.strip())) for label in decoded_labels
    ]
    result = metric.compute(
        predictions=decoded_predictions, references=decoded_labels, use_stemmer=True
    )
    # Extract a few results
    result = {key: value.mid.fmeasure * 100 for key, value in result.items()}
    # Add mean generated length
    prediction_lens = [
        np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions
    ]
    result["gen_len"] = np.mean(prediction_lens)

    return result

# %%
tensorboard_callback = TensorBoard(log_dir="./summarization_model_save/logs")

metric_callback = KerasMetricCallback(
    metric_fn, eval_dataset=validation_dataset, predict_with_generate=True
)


# %%
tf.keras.backend.clear_session()

# %%
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.compat.v1.Session(config=config)

# %%
early_stopping= EarlyStopping(patience=10, verbose=1),
lr_decay = ReduceLROnPlateau(factor=0.1, patience=5, min_lr=0.00001, verbose=1),
model_checkpoint = ModelCheckpoint('model-checkpoint.h5', verbose=1, save_best_only=True, save_weights_only=True)


callbacks = [metric_callback, tensorboard_callback, early_stopping, lr_decay, model_checkpoint]

model.fit(
    train_dataset, validation_data=validation_dataset, epochs=epochs, callbacks=callbacks, verbose = 1
)

# %%
example = test.iloc[0]
sample_text= "Tanjiro Kamado is a kind-hearted and intelligent boy who lives with his family in the mountains. He became his family's breadwinner after his father's death, making trips to the nearby village to sell charcoal. Everything changed when he came home one day to discover that his family was attacked and slaughtered by a demon. Tanjiro and his sister Nezuko were the sole survivors of the incident, with Nezuko being transformed into a demon, but still surprisingly showing signs of human emotion and thought. After an encounter with Giyū Tomioka, a demon slayer, Tanjiro is recruited by Giyū and sent to his retired master Sakonji Urokodaki for training to also become a demon slayer, beginning his quest to help his sister turn into human again and avenge the death of his family. After two years of strenuous training, Tanjiro takes part in a formidable exam and is one of the few survivors to pass, officially making him a member of the Demon Slayer Corps. He begins his work of hunting down and slaying demons alongside Nezuko, who has been hypnotized to bring no harm to humans and who occasionally helps him in battle. One of Tanjiro's assignments brings him to Asakusa where he encounters Muzan Kibutsuji, the progenitor of all demons and the one who murdered his family. He also meets Tamayo, a demon who is free of Muzan's control. Tamayo allies with Tanjiro and begins to develop a cure for Nezuko, though it will require Tanjiro to supply her with blood from the Twelve Kizuki, the most powerful demons under Muzan's command."

# %%
inputs = tokenizer.batch_encode_plus([sample_text], max_length=2048, return_tensors='tf')
summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=128, early_stopping=True)
summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]

# %%
print(summary)

# %%



