import sys
import os
import csv
import streamlit as st
import pandas as pd
from datetime import date
import pandasql as psql
import base64

################################
######### Variables ############
################################
# -- Loading Variables
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# -- Loading Session Data
if 'project_data' not in st.session_state:
    st.session_state.project_data = pd.read_csv(script_directory+'/data/project.csv')

if 'mapping_df' not in st.session_state:
    st.session_state.mapping_df = pd.DataFrame(columns=["Sno","DestinationColumn","SourceColumn","Type","Expression"])

################################
####### GenericFunctions #######
################################
# -- Load Mapping File
def load_mapping_file():
    if 'project_name' in st.session_state:
        try:
            # print("project_name - "+st.session_state.project_name)
            cond = (st.session_state.project_data['Project'] == st.session_state.project_name)
            file_name = script_directory+'/data/'+str(st.session_state.project_data[cond].Id.values[0])+"_"+st.session_state.project_data[cond].Source.values[0]+"_"+st.session_state.project_data[cond].Destination.values[0]+'.csv'
            # print("file_name - "+file_name)
            st.session_state.mapping_df = pd.read_csv(file_name,sep="|",quoting=csv.QUOTE_NONE)
        except Exception as e:
            st.session_state.mapping_df = pd.DataFrame(columns=["Sno","DestinationColumn","SourceColumn","Type","Expression"])
            st.error(f"Unable to load mapping file - {e}")

################################
####### Display of data ########
################################
# -- Streamlit Settings
st.set_page_config(layout='wide')
st.title("Data Generation")

# -- Add Project Dropdown
st.text("")
st.text("")
st.text("")
col1, col2, col3 = st.columns(3)
project_name = col1.selectbox(
                                'Select Project',
                                st.session_state.project_data['Project'],
                                key="project_name",
                                on_change=load_mapping_file()
                             )

# -- Upload Data
if len(st.session_state.mapping_df)>0:
    st.text("")
    st.text("")
    st.text("")
    col1, col2, col3 = st.columns(3)

    cond = (st.session_state.project_data['Project'] == st.session_state.project_name)
    result = st.session_state.project_data[cond].Source.values[0]
    with col1:
        source_data_file = st.file_uploader(
            "Source data file name - "+str(result)+".csv",
            type="csv",
            key="source_data_file",
            accept_multiple_files=True
        )

# -- Button Show Data
st.text("")
st.text("")
col1, col2, col3 = st.columns([0.3,0.5,2.2])

if col1.button("Show Data"):
    if source_data_file is not None:
        for file in source_data_file:
            df = pd.read_csv(file)

    # Update dataframe with Pandas Mapping Fields
    for index, row in st.session_state.mapping_df.iterrows():
        if row['Type'] == 'Pandas':
            column_name = row['DestinationColumn']
            expression = row['Expression'].replace("'", "")
            df[column_name] = eval(expression)

    # Creating SQL Statement
    sql_statement = "SELECT "
    for index, row in st.session_state.mapping_df.iterrows():
        destination_column = row['DestinationColumn']
        source_column = row['SourceColumn']
        column_type = row['Type']
        expression = row['Expression'] if 'Expression' in row else None

        if column_type == 'Constant':
            # Create a dummy column with the provided expression
            sql_statement += str(expression) + ' AS "' + str(destination_column) + '",'
        elif column_type == 'Pandas':
            sql_statement += '"' + str(destination_column) + '" AS "' + str(destination_column) + '",'
        else:
            # Use the source column as-is
            sql_statement += '"' + str(source_column) + '" AS "' + str(destination_column) + '",'

    
    # Remove the trailing comma and space
    sql_statement = sql_statement[:-1]+" from df"
    # st.write(sql_statement+" from df")

    st.session_state.df = df
    st.session_state.sql_statement = sql_statement

    # Display Data
    st.dataframe(df)

# -- Button Generate Data
if col2.button("Generate Data"):
    df = st.session_state.df
    if len(df) == 0 :
        st.error("No records available to run query, click on Show Data")
    else:
        sql_query = st.text_area(label="Sql Query", value=st.session_state.sql_statement, key="sql_query", height=200)
        try:
            result_df = psql.sqldf(sql_query, locals())
            st.write("Query Result")
            st.dataframe(result_df)
            csv_data = result_df.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download Result CSV</a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error executing SQL query: {str(e)}")