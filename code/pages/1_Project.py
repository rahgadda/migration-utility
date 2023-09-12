import streamlit as st
import os
import pandas as pd
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
st.title("Project")

# -- Add Project Details
st.text("")
st.text("")
st.text("")
col1, col2, col3 = st.columns(3)
project = col1.text_input(label="Enter Project Name",placeholder="Project Name",key="project",label_visibility="collapsed")
source_app = col1.text_input(label="Enter Source Application Name",placeholder="Source Application Name",key="source_app",label_visibility="collapsed")
destination_app = col1.text_input(label="Enter Destination Application Name",placeholder="Destination Application Name",key="destination_app",label_visibility="collapsed")

# -- Add Project
col1, col2, col3 = st.columns([0.3,0.2,2.5])
if col1.button("Add Project"):
    # -- Create new Row
    new_data = {"Project": project, "Source": source_app, "Destination": destination_app}
    
    # -- Add new row
    st.session_state.project_data = pd.concat([st.session_state.project_data, pd.DataFrame([new_data])], ignore_index=True)
    st.session_state.project_data = st.session_state.project_data.drop_duplicates(subset='Project', keep="last")
    
    # -- Save data to CSV
    st.session_state.project_data['Id'] = st.session_state.project_data.index
    st.session_state.project_data.to_csv(script_directory+'/data/project.csv', index=False)

if col2.button("Save"):
    # -- Save data to CSV
    st.session_state.project_data['Id'] = st.session_state.project_data.index
    st.session_state.project_data.to_csv(script_directory+'/data/project.csv', index=False)

st.text("")
st.text("")
st.text("")

if len(st.session_state.project_data)>0:
        st.session_state.project_data=st.data_editor(st.session_state.project_data, hide_index=True)