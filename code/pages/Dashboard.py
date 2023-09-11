import streamlit as st
import pandas as pd
from lib.load_dataset import load_dataset
import os

################################
######### Variables ############
################################

################################
####### GenericFunctions #######
################################
    
def save_dataset():
    # Load a dataset from the Hugging Face Hub
    dataset = load_dataset()

    # Create a directory to save the files
    output_directory = "data"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    # Iterate through the dataset and save each file to the data folder
    print(dataset)
    # for split in dataset.keys():
        # for file_name, file_content in enumerate(dataset[split]):
        #     file_path = os.path.join(output_directory, file_name)    
        #     with open(file_path, 'w', encoding='utf-8') as file:
        #         file.write(file_content)
    
            # print(f"Saved: {split}")

    # print("All files saved successfully.")

    
################################
####### Display of data ########
################################
save_dataset()