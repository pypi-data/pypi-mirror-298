import os
from transformers import T5ForConditionalGeneration, T5Tokenizer

def download_model(model_dir):
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

       
        print("Downloading T5 model...")
        T5Tokenizer.from_pretrained('t5-small', cache_dir=model_dir)
        T5ForConditionalGeneration.from_pretrained('t5-small', cache_dir=model_dir)
        print(f"Model downloaded and saved in {model_dir}")
    else:
        print(f"Model already exists in {model_dir}.")
