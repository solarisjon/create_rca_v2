import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function
from chat_with_llm import chat_with_llm

from authenticate_ai import create_session

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str, OPENAI_ENDPOINT, OPENAI_MODEL, OPENAI_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_USERNAME, temperature, rag_query_scope_val):
    # Prepare the DB.
    embedding_function = get_embedding_function(OPENAI_ENDPOINT, OPENAI_EMBEDDING_MODEL, OPENAI_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=rag_query_scope_val)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    print(f'In query_rag --> {prompt}')

    response_text = chat_with_llm(prompt, create_session(OPENAI_KEY, OPENAI_ENDPOINT), OPENAI_USERNAME, temperature)
    

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\n\n\nSources: {sources}"
    return formatted_response


if __name__ == "__main__":
    main()