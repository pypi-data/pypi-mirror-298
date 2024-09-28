# bourguiba.py
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration

class Bourguiba:
    def __init__(self, model_dir):
        # Load the pre-trained T5 model and tokenizer
        self.tokenizer = T5Tokenizer.from_pretrained(model_dir)
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir)

    def generate_command(self, input_text):
        # Tokenize the input text
        inputs = self.tokenizer(input_text, return_tensors="pt")
        # Generate the command
        outputs = self.model.generate(**inputs, max_new_tokens=50)
        # Decode the generated tokens
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    import sys
    model_dir = os.path.join(os.path.expanduser("~"), ".bourguiba_model")

    # Initialize Bourguiba object
    bourguiba = Bourguiba(model_dir)

    # Capture the user input
    if len(sys.argv) < 2:
        print("Usage: bourguiba \"command description\"")
        sys.exit(1)

    # Get the input description for the command
    input_text = sys.argv[1]

    # Generate the shell command based on the input description
    command = bourguiba.generate_command(input_text)

    # Print the generated command to the terminal
    print(f"Generated command: {command}")
