import os
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from bourguiba.model_downloader import download_model

class Bourguiba:
    def __init__(self):
        # Set the custom model directory
        self.model_dir = os.path.join(os.path.expanduser("~"), ".bourguiba_model")
        
        # Download the model if not already present
        download_model(self.model_dir)

        # Load the model and tokenizer from the custom directory
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_dir)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_dir)

    def generate_command(self, description):
        # Prepare the input for the model
        input_text = f"generate command: {description}"
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')

        # Generate the command
        with torch.no_grad():
            output = self.model.generate(input_ids)

        # Decode the generated command
        command = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return command


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: bourguiba <command_description>")
        sys.exit(1)

    description = " ".join(sys.argv[1:])
    bourguiba = Bourguiba()
    command = bourguiba.generate_command(description)
    print(f"Generated command: {command}")
