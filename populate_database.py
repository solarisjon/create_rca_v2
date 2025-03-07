import os
import shutil
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
#from langchain.vectorstores.chroma import Chroma
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma


def main():
    pass


def load_documents(data_path: str) -> list[Document]:
    """
    Loads documents from the specified directory path.

    Args:
        data_path (str): The path to the directory containing the PDF documents.

    Returns:
        list: A list of loaded documents.
    """
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()



def add_to_chroma(chunks , OPENAI_ENDPOINT, \
                           OPENAI_EMBEDDING_MODEL, OPENAPI_KEY, CHROMA_PATH) -> None:

    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, \
        embedding_function=get_embedding_function(OPENAI_ENDPOINT, 
                                                  OPENAI_EMBEDDING_MODEL, 
                                                  OPENAPI_KEY)
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        # db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database(chroma_path) -> None:
    """
    Deletes the directory at the specified path if it exists.

    Args:
        chroma_path (str): The path to the directory to be deleted.

    Raises:
        OSError: If the directory cannot be removed.
    """
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)


if __name__ == "__main__":
    main()