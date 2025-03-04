from langchain_chroma import Chroma
#from langchain.vectorstores import Chroma
#from langchain.embeddings import OpenAIEmbeddings
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
import os

def get_embedding_function(OPENAI_ENDPOINT, OPENAI_EMBEDDING_MODEL, OPENAI_KEY):

    print(f"Connect to {OPENAI_ENDPOINT} with Model {OPENAI_EMBEDDING_MODEL} ({OPENAI_KEY})")


    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        openai_api_base=OPENAI_ENDPOINT,
        openai_api_key=OPENAI_KEY,
        show_progress_bar=True,
    )
    return embeddings


pem_path = "/usr/local/etc/openssl@3/certs/../cert.pem"
os.environ['REQUESTS_CA_BUNDLE'] = pem_path
os.environ['SSL_CERT_FILE'] = pem_path

OPENAI_ENDPOINT = "https://llm-proxy-api.ai.eng.netapp.com"
OPENAI_API_KEY = "user=jbowman&key=sk_2517eac5bd5ef5f9696dfa61b337a06218a2e62d00a64890fffc6e50d70b299e"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"

# Specify the directory where your ChromaDB data is stored
persist_directory = "./chroma"

# Initialize the embedding function (use the same configuration as when the DB was populated)
embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Load the existing Chroma vector store
chroma_db = Chroma(persist_directory=persist_directory, 
                   embedding_function=get_embedding_function(OPENAI_ENDPOINT, 
                                                  OPENAI_EMBEDDING_MODEL, 
                                                  OPENAI_API_KEY))

# Now you can perform operations, e.g., search:
query = "zookeeper bugs"
results = chroma_db.similarity_search(query)

print(results)

