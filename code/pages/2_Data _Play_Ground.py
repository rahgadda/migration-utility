import streamlit as st
import os
import sys

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

################################
####### Display of data ########
################################
# -- Streamlit Settings
st.set_page_config(layout='wide')
st.title("Data Play Ground")
