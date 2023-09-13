import os
import sys
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import numpy as np
import torch
import faiss
from sentence_transformers import SentenceTransformer
import csv

################################
######### Variables ############
################################
# -- Loading Variables
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
source_df = pd.DataFrame()
destination_df = pd.DataFrame()
model = SentenceTransformer('all-mpnet-base-v2')

# -- Loading Session Data
if 'project_data' not in st.session_state:
    st.session_state.project_data = pd.read_csv(script_directory+'/data/project.csv')

################################
####### GenericFunctions #######
################################
# -- Create Embedding - all-mpnet-base-v2 - https://www.sbert.net/docs/pretrained_models.html
def embed_text(text):
    embedding = model.encode(text)
    return embedding

def embed_list(list):
    embeddings = []
    for text in list:
        embeddings.append(embed_text(text))
    return embeddings

# -- Store embeddings in a FAISS Vector database
def store_embeddings(embeddings):
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatIP(dimension)
    index.add(np.array(embeddings))
    # faiss.write_index(index, "data/vector_db.index")
    return index

# -- Perform semantic search using embeddings
def semantic_search(query_embedding, index, k=1):
    D, I = index.search(np.array([query_embedding]), k)
    return I[0][0]

################################
####### Display of data ########
################################
# -- Streamlit Settings
st.set_page_config(layout='wide')
st.title("Project")

# -- Add Project Dropdown
st.text("")
st.text("")
st.text("")
col1, col2, col3 = st.columns(3)
option = col1.selectbox('Select Project',st.session_state.project_data['Project'])
col1, col2, col3 = st.columns(3)


# -- Destination File Name
st.text("")
st.text("")

col1, col2, col3 = st.columns(3)
cond = (st.session_state.project_data['Project'] == option)
result = st.session_state.project_data[cond].Destination.values[0]
with col1:
    destination_file_format = st.file_uploader(
        "Destination file name - "+str(result)+".csv",
        type="csv",
        key="destination_file_format",
        accept_multiple_files=True
    )
    
if destination_file_format is not None:
    for file in destination_file_format:
        destination_df = pd.read_csv(file)

# -- Source File Name
cond = (st.session_state.project_data['Project'] == option)
result = st.session_state.project_data[cond].Source.values[0]
with col3:
    source_file_format = st.file_uploader(
        "Source file name - "+str(result)+".csv",
        type="csv",
        key="source_file_format",
        accept_multiple_files=True
    )

if source_file_format is not None:
    for file in source_file_format:
        source_df = pd.read_csv(file)

# -- Suggest Button
st.text("")
st.text("")
col1, col2, col3 = st.columns([0.25,0.2,2.55])
if col1.button("Suggest"):
    st.session_state.mapping_df = pd.DataFrame(columns=["Sno","DestinationColumn","SourceColumn","Type","Expression"])
    if len(destination_df) == 0 or len(source_df) == 0: 
        st.error("Select Source and Destination Files")
    else:
        new_data = []
        
        # Source - KnowledgeBase
        input_text = source_df["Columns"].tolist()
        embeddings = embed_list(input_text)
        index = store_embeddings(embeddings)
        
        # Map to Source
        for i in range(len(destination_df)):
            search_text = destination_df.loc[i, "Columns"]
            query_embeddings = embed_text(search_text)
            result = input_text[semantic_search(query_embeddings, index)]
            row = {
                    "Sno": i+1,
                    "DestinationColumn": destination_df.loc[i, "Columns"],
                    "SourceColumn": result,
                    "Type": None, 
                    "Expression":None
                }
            new_data.append(row)
        
        # Saving Mapping and displaying
        st.session_state.mapping_df = pd.concat(
                                                    [ st.session_state.mapping_df, pd.DataFrame(new_data)], 
                                                    ignore_index=True
                                                )

# -- Save Button
if col2.button("Save"):
    if (len(destination_df) > 0 and len(source_df) > 0 and len(st.session_state.mapping_df)>0):
        cond = (st.session_state.project_data['Project'] == option)
        file_name = script_directory+'/data/'+str(st.session_state.project_data[cond].Id.values[0])+"_"+st.session_state.project_data[cond].Source.values[0]+"_"+st.session_state.project_data[cond].Destination.values[0]+'.csv'
        st.session_state.mapping_df.to_csv(file_name, index=False, sep="|",quoting=csv.QUOTE_NONE)
    else:
        st.error("Transformation not created")