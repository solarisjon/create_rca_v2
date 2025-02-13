import streamlit as st
from PyPDF2 import PdfFileReader
import io
import os
import tempfile
from langchain.document_loaders import PyPDFDirectoryLoader
# A test for SCM V2

# Set the title of the app
st.set_page_config(page_title="NetApp RCA and Case Generator", page_icon="netapp_logo.png", layout="wide")

# Set the color theme
st.markdown(
    """
    <style>
    .css-18e3th9 {
        background-color: #0067C5;  /* NetApp blue */
    }
    .css-1d391kg {
        background-color: #0067C5;  /* NetApp blue */
    }
    .css-1v3fvcr {
        color: white;
    }
    .css-145kmo2 {
        color: white;
    }
    .css-1cpxqw2 {
        color: white;
    }
    .css-1inwz65 {
        color: white;
    }
    .css-1r6slb0 {
        color: white;
    }
    .css-1a32fsj {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add NetApp logo at the top of the sidebar
st.sidebar.image("netapp_logo.png", use_column_width=True)

# Sidebar for uploading files
st.sidebar.header("Upload PDFs")
uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

# Main window content
st.title("NetApp RCA and Case Generator")
st.header("Uploaded PDF Details")

if uploaded_files:
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_paths = []
        for uploaded_file in uploaded_files:
            # Save each uploaded file to the temporary directory
            file_path = os.path.join(tmpdirname, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)
            
            # Display file details
            st.subheader(f"File: {uploaded_file.name}")
            pdf_reader = PdfFileReader(io.BytesIO(uploaded_file.read()))
            num_pages = pdf_reader.getNumPages()
            st.write(f"Number of pages: {num_pages}")
            first_page = pdf_reader.getPage(0)
            st.write(first_page.extract_text())
        
        # Load PDFs using PyPDFDirectoryLoader from LangChain
        loader = PyPDFDirectoryLoader(tmpdirname)
        documents = loader.load()
        st.write("Loaded documents using LangChain's PyPDFDirectoryLoader:")
        st.write(documents)

else:
    st.write("No PDF files uploaded yet. Please upload files using the sidebar.")

