import os
import w3storage
import pandas as pd

################################
######### Variables ############
################################
W3_API_KEY = os.environ.get("W3_API_KEY")
PROJECT_CIDR = os.environ.get("PROJECT_CIDR")
BASE_URL = os.environ.get("BASE_URL")
w3 = None

################################
####### GenericFunctions #######
################################
def load_dataset():
    w3 = w3storage.API(token=W3_API_KEY)
    df = pd.read_csv(f"{BASE_URL}/{PROJECT_CIDR}/project.csv")

    # print(df)
    return df