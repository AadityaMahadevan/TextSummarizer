import torch
import transformers
import string
from transformers import AutoTokenizer

def get_abstractive_summary(input_text, checkpoint_path, model_checkpoint):
    
    model = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    device = "cpu"

    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    summary_text_ids = model.generate(
        input_ids=input_ids,
        bos_token_id=model.config.bos_token_id,
        eos_token_id=model.config.eos_token_id,
        length_penalty=2.0,
        max_length=256,
        min_length=128,
        num_beams=4,
        do_sample=False,
    )
    summary = [tokenizer.decode(g, skip_special_tokens=True) for g in summary_text_ids]
    summary = clean_summary(summary)

    return summary

def clean_summary(summary):
    summary = summary[0]
    summary = summary.strip()
    summary = summary.replace("\n", " ")
    return summary