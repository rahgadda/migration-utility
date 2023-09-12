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

# -- Delimiter
st.text("")
st.text("")
st.text("")
col1, col2, col3 = st.columns(3)
delimiter = col1.selectbox(
                label="File Delimiter",
                options=[",","|"],
                key="delimiter"
            )

# -- Upload Sample Files
st.text("")
st.text("")
col1, col2, col3, col4 = st.columns([1,0.3,0.7,1])
uploaded_files = col1.file_uploader(
    "Choose a file",
    type="csv",
    key="uploaded_files",
    accept_multiple_files=True
)

# -- Add header
header=col3.checkbox(
                label='Add Header',
                key="header"
            )

# -- Dynamic Headers
if header:
    header_count=col4.number_input(
                                        label="No of Header",
                                        value=0,
                                        key="header_count",
                                        min_value=0, 
                                        max_value=100,
                                        step=1
                                )
