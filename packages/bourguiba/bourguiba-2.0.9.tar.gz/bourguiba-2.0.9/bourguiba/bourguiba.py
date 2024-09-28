import os
import sys
from transformers import T5Tokenizer, T5ForConditionalGeneration

class Bourguiba:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        if not os.path.exists(self.model_dir):
            print(f"Downloading T5 model to {self.model_dir}...")
            self.download_model()
        else:
            print(f"Model already exists in {self.model_dir}.")

        # Load tokenizer and model
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_dir)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_dir)

    def download_model(self):
        # Download the tokenizer and model files to model_dir
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small', cache_dir=self.model_dir)
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small', cache_dir=self.model_dir)
        print(f"Model downloaded and saved in {self.model_dir}")

    def generate_command(self, input_text):
        # Tokenize the input text and generate the output
        input_ids = self.tokenizer(input_text, return_tensors='pt').input_ids
        output_ids = self.model.generate(input_ids, max_length=50)
        command = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return command

def main():
    model_dir = os.path.expanduser('~/.bourguiba_model')
    bourguiba = Bourguiba(model_dir)

    if len(sys.argv) < 2:
        print("Usage: bourguiba '<description of command>'")
        sys.exit(1)

    input_text = sys.argv[1]
    command = bourguiba.generate_command(input_text)

    # Instead of executing the command, print it for the user
    print(f"Generated command: {command}")

if __name__ == "__main__":
    main()
