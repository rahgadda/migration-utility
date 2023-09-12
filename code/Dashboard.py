import streamlit as st
import lib.gdrive as gdrive
import os
import sys

################################
######### Variables ############
################################

################################
####### GenericFunctions #######
################################

# -- Save Files
def save_data_files():
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    if len(script_directory) == 0:
        gdrive.download_file("project.csv",script_directory+"/data/")


################################
####### Display of data ########
################################

# -- Streamlit Settings
st.set_page_config(layout='wide')
st.title("Dashboard")

# -- Load base files from Google Drive
save_data_files()
