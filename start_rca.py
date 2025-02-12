import streamlit as st
import os
import shutil
from handle_config_file import handle_config
from create_rcav2 import start_processing_request as process_request


# Function to clean and recreate the uploads directory
def clean_and_recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)


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
    footer {
        visibility: hidden;
    }
    .footer {
        visibility: visible;
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0067C5;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Created by Jon Bowman</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Add NetApp logo at the top of the sidebar
st.sidebar.image("netapp_logo.png", use_container_width=True)

# Sidebar for uploading files
st.sidebar.header("Upload PDFs")
uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

# Sidebar for selecting RCA type
st.sidebar.header("Select RCA Type")
document_type = st.sidebar.selectbox("Choose the type of RCA", ["Formal RCA", "Initial Case Analysis"])

# Sidebar for setting temperature
st.sidebar.header("Set Temperature")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=3.0, value=0.5, step=0.1)


# Main window content
st.title("NetApp RCA and Case Generator")
st.header("Uploaded PDF Details")

if document_type == "Initial Case Analysis":
    document_type = "initial_analysis"
elif document_type == "Formal RCA":
    document_type = "formal_rca"
else:
    print("No valid document type found")



prompt_type = "result_initial_analysis"
temperature = 0.5
document_location, llm_creds = handle_config()
uploads_path = document_location["uploads-path"]

print(f'{uploaded_files}')
if st.button("Start"):
    if uploaded_files:
        # Ensure the uploads directory is clean
        clean_and_recreate_directory(uploads_path)
        file_paths = []
        for uploaded_file in uploaded_files:
            # Save each uploaded file to the temporary directory
            file_path = os.path.join(uploads_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)
        print(f'file path is {file_path}')
        response = process_request(temperature, document_type)
        st.write(response)

    else:
        st.write("Please upload CPE, CONTAP, SAP files using the sidebar.")




def main():
    print("in main")

# Run the Streamlit app
if __name__ == "__main__":
    main()
