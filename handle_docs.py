from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from config_objects import Chroma_Config


def load_documents(data_path):
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()

def chunk_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(Chroma_Config.CHROMA_CHUNK_SIZE),
        chunk_overlap=int(Chroma_Config.CHROMA_CHUNK_OVERLAP),
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def main():
    print("MAIN")

if __name__ == '__main__':
    main()