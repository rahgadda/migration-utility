import os
import sys
import io
import re
import base64
import streamlit as st
import pandas as pd
import pandasql as psql

################################
######### Variables ############
################################
# -- Loading Variables
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
file_details =  pd.DataFrame(columns=['file_name', 'data'])

# -- Loading Session Data
if 'project_data' not in st.session_state:
    st.session_state.project_data = pd.read_csv(script_directory+'/data/project.csv')

if 'global_dataframe' not in st.session_state:
    st.session_state.global_dataframe=file_details

if 'load_sql' not in st.session_state:
    st.session_state.load_sql=False

if 'run_sql' not in st.session_state:
    st.session_state.run_sql=False

################################
####### GenericFunctions #######
################################
# -- Create Dynamic Columns
def generate_column_names(end):
    if 1 > end:
        raise ValueError("End value must be grater than 1")

    column_names = [f"Col{i}" for i in range(1, end+2)]
    return column_names

# -- Add missing separator
def add_missing_separators(file_data,separator,max_header_count):
    # Create a list to hold the modified rows
    modified_rows = []

    for line in file_data:
        
        # Count the occurrences of the separator
        count = line.count(separator)

        # Append the separator if the count is less than the max_header_count
        if count < max_header_count:
            separator_str=separator * (max_header_count - count)
            line = line + separator_str

        # Added modified line
        modified_rows.append(line)
    
    return modified_rows

# -- Create global dataframes
def create_global_df(sep=",", usecols=None, max_header_count=1):
    file_details =  pd.DataFrame(columns=['file_name','data'])
    try:
        if uploaded_files is not None:
            for file in uploaded_files:
                if usecols is not None:
                    file_data = io.StringIO(file.read().decode())
                    modified_rows = add_missing_separators(file_data, sep,max_header_count)
                    df = pd.DataFrame(each_row.split(sep) for each_row in modified_rows)
                    df.columns = usecols
                else:
                    df = pd.read_csv(file, sep=sep)

                pattern = r'([^/]+)\.csv$'
                match = re.search(pattern, file.name)
                file_name = match.group(1)
                file_details.loc[len(file_details)] =  {
                                                          'file_name':file_name,
                                                          'data':df
                                                       }

        st.session_state.global_dataframe = file_details
    except Exception as e:
        st.error(f"Error processing csv: {str(e)}")
        raise e

# -- Load global dataframes
def load_global_df():
    if st.session_state.header:
        print("Added Headers")
        usecols = generate_column_names(st.session_state.header_count)
        create_global_df(sep,usecols,st.session_state.header_count)
    else:
        print("No Headers Added")
        create_global_df(sep)

# -- Run SQL Data
def run_sql_df():
    for index, row in st.session_state.global_dataframe.iterrows():
        globals()['%s' % row['file_name']] = row['data']

    try:
        sql_query = st.text_area(label="Sql Query", value="", key="sql_query", height=200)
        
        if st.button("Run SQL Query"):
            result_df = psql.sqldf(sql_query, globals())
            st.write("Query Result")
            st.dataframe(result_df)
            
            csv_data = result_df.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download Result CSV</a>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")

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

# -- Add header Indicator
header=col3.checkbox(
                label='Add Header',
                key="header"
            )

# -- Dynamic Headers Count
if header:
    header_count=col4.number_input(
                                        label="No of Header",
                                        value=2,
                                        key="header_count",
                                        min_value=1, 
                                        max_value=100,
                                        step=1
                                )

# -- Load Data
st.text("")
col1, col2, col3 = st.columns([1,1,8])
sep = st.session_state.delimiter
if col1.button("Load Data"):
    st.session_state.load_sql=True
    st.session_state.run_sql=False

    load_global_df()

# -- Run SQL Query
if col2.button("SQL"):
    st.session_state.load_sql=False
    st.session_state.run_sql=True

    run_sql_df()

# -- Display SQL Query Data
if st.session_state.run_sql:
   run_sql_df() 

# -- Display Loaded Data
if (len(st.session_state.global_dataframe)>0 and st.session_state.load_sql):
    # print("Count of stored files - "+str(len(st.session_state.global_dataframe)))
    col1, col2, col3 = st.columns(3)
    col1.selectbox(
                        label="Select Table Name",
                        key="table_name",
                        options=st.session_state.global_dataframe['file_name']
                  )

    for index, row in st.session_state.global_dataframe.iterrows():
        globals()['%s' % row['file_name']] = row['data']

    st.dataframe(psql.sqldf("select * from "+st.session_state.table_name, globals()))