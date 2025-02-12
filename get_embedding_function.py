from langchain_openai import OpenAIEmbeddings

def get_embedding_function(OPENAI_ENDPOINT, OPENAI_EMBEDDING_MODEL, OPENAI_KEY):
    print(f"Connect to {OPENAI_ENDPOINT} with Model {OPENAI_EMBEDDING_MODEL} ({OPENAI_KEY})")


    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        openai_api_base=OPENAI_ENDPOINT,
        openai_api_key=OPENAI_KEY,
        show_progress_bar=True,
    )
    return embeddings