import streamlit as st
import pandas as pd
from datasets import load_dataset
import os

################################
######### Variables ############
################################
HF_API_KEY = os.environ.get("HF_API_KEY")
DATA_SET = os.environ.get("DATA_SET")

################################
####### GenericFunctions #######
################################
def load_hf_dataset():
    dataset = load_dataset(DATA_SET)
    return dataset
    
def save_dataset():
    # Load a dataset from the Hugging Face Hub
    dataset = load_hf_dataset()

    # Create a directory to save the files
    output_directory = "data"
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through the dataset and save each file to the data folder
    for split in dataset.keys():
        for file_name, file_content in enumerate(dataset[split]):
            file_path = os.path.join(output_directory, file_name)    
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(file_content)
    
            print(f"Saved: {file_path}")

    print("All files saved successfully.")

    
################################
####### Display of data ########
################################
save_dataset()