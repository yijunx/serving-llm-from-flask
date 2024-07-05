"""To initialize chroma db"""
import chromadb

from chromadb.api.models.Collection import Collection
from chromadb.config import Settings
from chromadb.utils import embedding_functions


def get_chroma_collection(
    collection_name: str, embedding_model: str, chromadb_host: str, chromadb_port: str
) -> Collection:
    """init ucare chroma server

    Returns:
        Collection: chroma server Collection
    """
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=embedding_model, device="cpu"
    )
    chroma_client = chromadb.Client(
        Settings(
            chroma_api_impl="rest",
            chroma_server_host=chromadb_host,
            chroma_server_http_port=chromadb_port,
            chroma_server_ssl_enabled=False,
        )
    )
    collectiondb = chroma_client.get_or_create_collection(
        name=collection_name, embedding_function=embed_func
    )

    print(f"init collection finished: {collectiondb}, count: {collectiondb.count()}")
    print("all collection:", chroma_client.list_collections())
    return collectiondb
