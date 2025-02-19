from dataclasses import dataclass
from configparser import ConfigParser


config_object = ConfigParser()
config_object.read("config.ini")

@dataclass(frozen=True)
class Document_Config:
    UPLOADS_PATH: str = config_object["Documents"]["UPLOADS_PATH"]
    CHROMA_PATH: str = config_object["Documents"]["CHROMA_PATH"]
    PROMPTS_PATH: str = config_object["Documents"]["PROMPTS_PATH"]


@dataclass(frozen=True)
class LLM_Config:
    key : str
    OPENAI_USERNAME: str = config_object["LLM_Config"]["OPENAI_USERNAME"]
    OPENAI_ENDPOINT: str = config_object["LLM_Config"]["OPENAI_ENDPOINT"]
    OPENAI_API_KEY: str = config_object["LLM_Config"]["OPENAI_API_KEY"]
    OPENAI_MODEL: str = config_object["LLM_Config"]["OPENAI_MODEL"]
    OPENAI_EMBEDDING_MODEL: str = config_object["LLM_Config"]["OPENAI_EMBEDDING_MODEL"]

@dataclass(frozen=True)
class RAG_Config:
    RAG_QUERY_SCOPE_DEFAULT: int = config_object["RAG_Config"]["RAG_QUERY_SCOPE_DEFAULT"]


@dataclass(frozen=True)
class Chroma_Config:
    CHROMA_CHUNK_SIZE: int = config_object["Chroma_Config"]["CHROMA_CHUNK_SIZE"]
    CHROMA_CHUNK_OVERLAP: int  = config_object["Chroma_Config"]["CHROMA_CHUNK_OVERLAP"]