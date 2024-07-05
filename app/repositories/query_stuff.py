import random
import openai
from chromadb.api.models.Collection import Collection
from langchain.chains import LLMChain


def db_get_by_id(db: Collection, ids: list):
    """Get info from db by id

    Args:
        db (Collection): db chroma collection
        ids (list): list of ids

    Returns:
        list: list of documents from db
    """
    # remove duplicated id
    ids = list(set(ids))
    docs = db.get(ids=ids)
    return docs["documents"]


def query_with_db(db: Collection, query: str, n_results: int, source: str):
    """Query db and chain

    Args:
        db (Collection): vector db
        chain (LLMChain): chain to answer question based on context
        query (str): question to be answered
        n_results (int, optional): number of documents retrieved from vector db per query. Defaults to 6.
        source (str, optional): search range for vector db. choose from ["all", "context", "QA"]. Defaults to "context".

    Returns:
        db_output (str): relevant QA pairs from db
        context (str): document contents from db
    """
    assert source in [
        "all",
        "context",
        "QA",
    ], "Source not supported, please select from ['all', 'context', 'QA']"

    prompt_condense_query = """Given a question, your task is to come up with a relevant search term that would retrieve relevant articles from a scientific database."""
    query_db = query_openai(query=query, system_prompt=prompt_condense_query)

    if source == "all":
        ### pretty formatting of model output not inplemented for this choice ###
        related_docs = db.query(
            query_texts=[query_db],
            n_results=n_results,
            include=["documents", "distances", "metadatas"],
        )

        db_output = []
        for idx in range(len(related_docs)):
            if related_docs["metadatas"][0][idx]["source"] == "QA":
                db_output.append(
                    str(related_docs["documents"][0][idx])
                    + ". "
                    + str(related_docs["metadatas"][0][idx]["answer"])
                )
            else:
                db_output.append(related_docs["documents"][0][idx])

        ### seperate between pieces, otherwise the model may confuse on settings between different sentences
        db_output = "\n\n".join(db_output)

    elif source == "context":
        # set search filter, i.e. the "where" arg in db.query
        # guideline_filter = dict(st.session_state["guideline_name_filter"])
        # guideline_filter.update({"source": "context"})
        guideline_filter = {"source": "context"}  # , "guideline": "diabetes"

        related_docs = db.query(
            query_texts=[query_db],
            n_results=n_results,
            # where={"source": "context"},
            where=guideline_filter,
            include=["documents", "distances", "metadatas"],
        )

        context = "\n\n".join(related_docs["documents"][0])

        # # get summarized moh context as str
        # context_summarized = query_openai(query=context, system_prompt="You are an AI assistant who is good at summarizing paragraphs")

        # get qa of the first context
        db_output_id = list(set([ids for ids in related_docs["ids"][0]]))
        q = []
        a = []
        # get all qa to the context
        for idx in range(0, len(db_output_id)):
            qa = db.get(where={"context_id": db_output_id[idx]})
            q.extend(qa["documents"])
            a.extend([mata["answer"] for mata in qa["metadatas"]])
        # retrieve answer in qa from matadata
        meta_answers = [mata["answer"] for mata in qa["metadatas"]]
        # format Q and A into str
        qa = [q[idx] + "   \n" + a[idx] for idx in range(len(a))]
        qa = "\n\n".join(random.sample(qa, k=min(len(qa), 8)))

        # add in summarized source context before answering the user question
        # db_output = "*Context from MOH guideline:*\n\n" + context_summarized + f"\n\n*Question and Answers based on the context:*\n\n" + qa
        db_output = f"_Relevant Question and Answers_\n\n" + qa

    elif source == "QA":
        # set search filter, i.e. the "where" arg in db.query
        # guideline_filter = dict(st.session_state["guideline_name_filter"])
        # guideline_filter.update({"source": "QA"})

        guideline_filter = {"source": "QA", "guideline": "diabetes"}
        # get related docs form db
        related_docs = db.query(
            query_texts=[query_db],
            n_results=n_results,
            where=guideline_filter,
            include=["documents", "distances", "metadatas"],
        )

        # retrieve matadata & id for source context
        meta_answers = [mata["answer"] for mata in related_docs["metadatas"][0]]
        context_ids = [meta["context_id"] for meta in related_docs["metadatas"][0]]

        # get source context of all the QA
        context = db_get_by_id(db=db, ids=context_ids)

        # # get summarized moh context as str
        # context = query_openai(query="; ".join(context), system_prompt="You are an AI assistant who is good at summarizing paragraphs")
        context = "   \n".join(context)

        # format related docs from db into string
        db_output = "\n\n".join(
            [
                related_docs["documents"][0][idx] + "   \n" + meta_answers[idx]
                for idx in range(len(meta_answers))
            ]
        )
        # add in summarized source context
        # db_output = "*Context from MOH guideline:*\n\n" + context + f"\n\n*Question and Answers based on the context:*\n\n" + db_output
        db_output = f"_Relevant Question and Answers:_\n\n" + db_output

    return db_output, context


def query_openai(
    query: str, system_prompt: str = "Answer the question with reasoning."
) -> str:
    """Query gpt 3.5 turbo with system prompt

    Args:
        query (str): the question
        system_prompt (str, optional): system prompt for the model. Defaults to "Answer the question with reasoning.".

    Returns:
        str: model response string
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
                # "content": "Answer the question in json format with fields 'answer' and 'reasoning'. The 'answer' is answer to the question, should be 'True' or 'False'; 'reasoning' is reasoning to explain the answer.",
            },
            {"role": "user", "content": query},
        ],
        n=1,
        temperature=0,
    )
    response = response["choices"][0]["message"]["content"]
    # remove spaces at the beginning and end of paragraphs
    return "\n\n".join([d.strip() for d in response.split("\n\n")])


def query_chain(query: str, db_output: str, chain: LLMChain):
    """Query chain and parse response

    Args:
        query (str): question to be asked
        db_output (str): reference context for the chain to answer query
        chain (LLMChain): LLM chain to answer question

    Returns:
        str: model response
    """
    # query openai to answer the original question
    response = chain.predict_and_parse(
        context=db_output,
        question=query,
    )
    # cast json formatted llm response into str
    if isinstance(response, dict):
        response = response["answer"] + ". " + response["reasoning"]
    return response
