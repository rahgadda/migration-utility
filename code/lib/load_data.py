import os
from datasets import load_dataset

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