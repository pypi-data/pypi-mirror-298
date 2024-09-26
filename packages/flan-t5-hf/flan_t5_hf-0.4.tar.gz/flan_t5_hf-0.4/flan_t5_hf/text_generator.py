from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import os

def get_model_directory():
    """Returns the directory where the model should be stored locally."""
    # Choose a local directory (e.g., in the user's home directory)
    home_dir = os.path.expanduser("~")
    model_dir = os.path.join(home_dir, ".flan_t5_hf", "flan_t5_xl")

    # Create the directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)

    return model_dir

def download_model_if_needed(model_dir):
    """Downloads the model if it does not already exist."""
    # Check if the model files exist
    model_files = ["pytorch_model.bin", "config.json", "tokenizer_config.json"]
    if not all(os.path.exists(os.path.join(model_dir, f)) for f in model_files):
        print(f"Downloading google/flan-t5-xl model to {model_dir}...")

        # Download and save the model and tokenizer
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl")
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xl")

        model.save_pretrained(model_dir)
        tokenizer.save_pretrained(model_dir)
        print("Download complete.")
    else:
        print("Model already downloaded.")

def load_classifier():
    """Loads the pipeline with the locally stored model."""
    model_dir = get_model_directory()

    # Check if model needs to be downloaded
    download_model_if_needed(model_dir)

    # Load the model from the local directory
    classifier = pipeline("text2text-generation", model=model_dir, device="cpu")

    return classifier
