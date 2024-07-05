from pydantic import BaseModel


class Question(BaseModel):
    content: str
    query_option: bool
    n_results: int = 5
    source: str = "context"
