import streamlit as st
import lib.gdrive as gdrive
import os
import sys
import pandas as pd

################################
######### Variables ############
################################
# -- Loading Variables
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# -- Loading Session Data
if 'project_data' not in st.session_state:
    st.session_state.project_data = pd.read_csv(script_directory+'/data/project.csv')

################################
####### GenericFunctions #######
################################
# -- Save Files
def save_data_files():
    if not os.listdir(script_directory+"/data"):
        gdrive.download_file("project.csv",script_directory+"/data/")
    else:
        print("Project details already exists")

################################
####### Display of data ########
################################
# -- Streamlit Settings
st.set_page_config(layout='wide')
st.title("Dashboard")

# -- Load base files from Google Drive
save_data_files()

# -- Show Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Projects", len(st.session_state.project_data))

# -- Transformations Performed
col2.metric("Transformations", "12")