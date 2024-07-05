from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate


def get_chain(
    openai_api_key: str,
) -> LLMChain:
    """Init and store LLMChain in st.session_state

    Args:
        openai_api_key (str): api key

    Returns:
        None
    """
    answer_schema = ResponseSchema(
        name="answer",
        description="The answer to the question",
    )
    reasoning_schema = ResponseSchema(
        name="reasoning", description="The reasoning to explain the answer"
    )
    response_schema = [answer_schema, reasoning_schema]

    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas=response_schema
    )
    format_instructions = output_parser.get_format_instructions()

    PROMPT = PromptTemplate(
        template="""Given the following context, answer the question at the end. Do not use knowledge outside the context. Do not make things up.
            
            Context: {context}
            Question: {question},
            
            {format_instructions}""",
        input_variables=["context", "question"],
        partial_variables={"format_instructions": format_instructions},
        output_parser=output_parser,
    )

    llm = ChatOpenAI(
        temperature=0, openai_api_key=openai_api_key, model_name="gpt-3.5-turbo"
    )

    return LLMChain(
        llm=llm,
        prompt=PROMPT,
    )
