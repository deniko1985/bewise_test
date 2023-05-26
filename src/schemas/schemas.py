from pydantic import BaseModel


class CountQuestions(BaseModel):
    questions_num: int


class GetUsername(BaseModel):
    username: str
