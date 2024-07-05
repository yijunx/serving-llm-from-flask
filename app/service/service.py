from app.models.schemas import Question
from app.repositories.query_stuff import query_with_db, query_openai, query_chain
from chromadb.api.models.Collection import Collection
from langchain.chains import LLMChain


def get_submitted_and_query(
    question: Question, collection: Collection, chain: LLMChain
) -> str:
    """Get user input and query, show history in ui and update session state when query completed

    Return:
        None
    """
    if question.query_option:
        db_context, raw_context = query_with_db(
            db=collection,
            query=question.content,
            n_results=question.n_results,
            source=question.source,
        )
        context_summarized = query_openai(
            query=raw_context,
            system_prompt="You are an AI assistant who is good at summarizing paragraphs",
        )
        context_summarized = "_Context from MOH guideline:_\n\n" + context_summarized
        db_context = db_context + "\n\n" + context_summarized

        model_output = query_chain(
            query=question.content,
            db_output=db_context,
            chain=chain,
        )

        # model_output += "\n\n" + db_context
        model_output = "\n\n_Final answer:_   \n" + model_output
    else:
        db_context = ""
        model_output = query_openai(query=question.content)
    return model_output

    # # query LLM
    # if str(st.session_state["query_option"]).startswith("Yes"):

    # else:
    #     model_output = query_openai(query=user_input)

    # try:
    #     with chat_area:
    #         if "demo_diabetes_questions" in st.session_state:
    #             user_input = st.session_state["demo_diabetes_questions"]

    #         if "user_input" in st.session_state:
    #             if st.session_state["user_input"] is not None:
    #                 user_input = st.session_state["user_input"]
    #         # else:
    #         #     st.warning("Please key in your question", icon="⚠️")

    #         # show past history
    #         for i in range(0, len(st.session_state["diabetes_generated"])):
    #             st.chat_message(
    #                 name="user", avatar=io.BytesIO(avatar_user_bytes)
    #             ).write(st.session_state["diabetes_past"][i])
    #             st.chat_message(
    #                 name="assistant", avatar=Image.open(io.BytesIO(avatar_system_bytes))
    #             ).write(st.session_state["diabetes_generated"][i])

    #         # query DB if user chose Yes
    #         if str(st.session_state["query_option"]).startswith("Yes"):
    #             db_context, raw_context = query_with_db(
    #                 db=st.session_state["chroma_collection"],
    #                 query=user_input,
    #                 n_results=N_RESULTS,
    #                 source=SOURCE,
    #             )

    #             # show intermediate step
    #             st.chat_message(
    #                 name="user", avatar=Image.open(io.BytesIO(avatar_user_bytes))
    #             ).write(user_input)
    #             st.chat_message(
    #                 name="assistant", avatar=Image.open(io.BytesIO(avatar_system_bytes))
    #             ).write(db_context)

    #             # get summarized moh context as str
    #             context_summarized = query_openai(
    #                 query=raw_context,
    #                 system_prompt="You are an AI assistant who is good at summarizing paragraphs",
    #             )
    #             context_summarized = (
    #                 "_Context from MOH guideline:_\n\n" + context_summarized
    #             )
    #             # show intermediate step
    #             st.chat_message(
    #                 name="assistant", avatar=Image.open(io.BytesIO(avatar_system_bytes))
    #             ).write(context_summarized)

    #             # add in summarized source context
    #             db_context = db_context + "\n\n" + context_summarized

    #         else:
    #             st.chat_message(
    #                 name="user", avatar=Image.open(io.BytesIO(avatar_user_bytes))
    #             ).write(user_input)
    #             db_context = ""

    #         # query LLM
    #         if str(st.session_state["query_option"]).startswith("Yes"):
    #             model_output = query_chain(
    #                 query=user_input,
    #                 db_output=db_context,
    #                 chain=st.session_state["chain"],
    #             )

    #             # model_output += "\n\n" + db_context
    #             model_output = "\n\n_Final answer:_   \n" + model_output

    #         else:
    #             model_output = query_openai(query=user_input)

    #         # show intermediate step
    #         st.chat_message(
    #             name="assistant", avatar=Image.open(io.BytesIO(avatar_system_bytes))
    #         ).write(model_output)

    #         # append to history
    #         st.session_state["diabetes_generated"].append(db_context + model_output)
    #         st.session_state["diabetes_past"].append(user_input)

    #         # log input output
    #         msg = {"USER_INPUT": user_input, "MODEL_OUTPUT": db_context + model_output}
    #         logger.info(msg)

    # except Exception as e:
    #     st.warning(f"Error when generating response: {e}", icon="⚠️")
    #     logger.error("Error at generating output", exc_info=e)
