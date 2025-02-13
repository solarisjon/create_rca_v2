from handle_docs import load_documents, chunk_documents
from configparser import ConfigParser
from populate_database import add_to_chroma
from query_rag import query_rag
from handle_prompts import load_prompts
from authenticate_ai import create_session

def handle_config():
    # Create a ConfigParser object
    config_object = ConfigParser()

    # Read the configuration from the 'config.ini' file
    config_object.read("config.ini")
    file_info = config_object["Documents"]
    llmproxy_creds = config_object["LLM"]
    return file_info, llmproxy_creds


def start_processing_request(data_path, temperature, document_type):
    """
    The primary function that kicks everything off

    Returns:
        
    
    Raises:
        
    """

    # Read in the configuration file to get key parameters.
    data_info, llm_creds = handle_config()
    OPENAI_ENDPOINT = llm_creds["OPENAI_ENDPOINT"]
    OPENAI_API_KEY = llm_creds["OPENAI_API_KEY"]
    OPENAI_MODEL = llm_creds["OPENAI_MODEL"]
    OPENAI_EMBEDDING_MODEL= llm_creds["OPENAI_EMBEDDING_MODEL"]
    OPENAI_USERNAME = llm_creds["OPENAI_USERNAME"]

    # Create a session handle to the LLM
    session = create_session(OPENAI_API_KEY, OPENAI_ENDPOINT)

    print("Load Documented")
    documents = load_documents(data_path)
    print("Chunk the Documents")
    chunked_data = chunk_documents(documents)
    print(chunked_data[0])
    add_to_chroma(chunked_data, OPENAI_ENDPOINT, OPENAI_EMBEDDING_MODEL, OPENAI_API_KEY)

    print("Obtain prompts")
    available_prompts = load_prompts()
    document_type_prompt = ""
    for key, value in available_prompts.items():
        if key == document_type:
            document_type_prompt = value
    print(f'Document Prompt is {document_type_prompt}')
    document_prompt =  document_type_prompt + available_prompts["netapp"] + available_prompts["context"]
    print("Start Query")

    response = query_rag(document_prompt, \
            OPENAI_ENDPOINT, OPENAI_MODEL, OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_USERNAME, temperature)
    return  response


def main():
    start_processing_request

if __name__ == "__main__":
    main()