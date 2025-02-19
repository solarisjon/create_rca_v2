from handle_docs import load_documents, chunk_documents
from populate_database import add_to_chroma
from query_rag import query_rag
from handle_prompts import load_prompts
from authenticate_ai import create_session


def start_processing_request(temperature, document_type, rag_query_scope_val, doc_config, llm_config):
    """
    The primary function that kicks everything off

    Returns:
        
    
    Raises:
        
    """


    # Create a session handle to the LLM
    session = create_session(llm_config.OPENAI_API_KEY, llm_config.OPENAI_ENDPOINT)

    print("Load Documented")
    documents = load_documents(doc_config.UPLOADS_PATH)
    print("Chunk the Documents")
    chunked_data = chunk_documents(documents)
    print(chunked_data[0])
    add_to_chroma(chunked_data, llm_config.OPENAI_ENDPOINT, llm_config.OPENAI_EMBEDDING_MODEL, llm_config.OPENAI_API_KEY, \
                   doc_config.CHROMA_PATH)

    print("Obtain prompts")
    available_prompts = load_prompts(doc_config.PROMPTS_PATH)
    document_type_prompt = ""
    for key, value in available_prompts.items():
        if key == document_type:
            document_type_prompt = value
    print(f'Document Prompt is {document_type_prompt}')
    document_prompt =  document_type_prompt + available_prompts["netapp"] + available_prompts["context"]
    print("Start Query")

    response = query_rag(document_prompt, \
            llm_config.OPENAI_ENDPOINT, llm_config.OPENAI_MODEL, llm_config.OPENAI_API_KEY, llm_config.OPENAI_EMBEDDING_MODEL, llm_config.OPENAI_USERNAME, temperature, rag_query_scope_val)
    return  response


def main():
    start_processing_request

if __name__ == "__main__":
    main()





