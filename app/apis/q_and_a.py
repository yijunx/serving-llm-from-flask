from flask import Blueprint
from logging import getLogger
from flask_pydantic import validate
from app.models.schemas import Question
from app.utils.config import find_which_config
from app.utils.init_chromadb import get_chroma_collection
from app.utils.init_chain import get_chain
from app.service.service import get_submitted_and_query
import os, threading
import time


logger = getLogger(__name__)
config = find_which_config()
bp = Blueprint("q_and_a_bp", __name__, url_prefix="/apis/q-and-a")
collection = get_chroma_collection(
    collection_name=config.CHROMADB_COL_NAME,
    embedding_model=config.EMBEDDING_MODEL,
    chromadb_host=config.CHROMADB_HOST,
    chromadb_port=config.CHROMADB_PORT,
)
chain = get_chain(openai_api_key=config.OPENAI_API_KEY)


@bp.route("/q", methods=["POST"])
@validate()
def ask_question(body: Question):
    print(f"api layer got it at {time.perf_counter()}")
    print(f"request handled with process id: {os.getpid()}")
    print(
        f"request handled request with thread id : {threading.current_thread().ident}"
    )
    result = get_submitted_and_query(question=body, collection=collection, chain=chain)
    return result


@bp.route("/mock-q", methods=["POST"])
@validate()
def ask_mock_question(body: Question):
    print(f"api layer got it at {time.perf_counter()}")
    print(f"request handled with process id: {os.getpid()}")
    print(
        f"request handled request with thread id : {threading.current_thread().ident}"
    )
    # result = get_submitted_and_query(question=body, collection=collection, chain=chain)
    time.sleep(1)
    return "mock result"
