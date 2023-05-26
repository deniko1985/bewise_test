import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Response
from pydantic.types import UUID4

from schemas.schemas import CountQuestions, GetUsername
from utils import users, questions
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("DOMAIN")

router = APIRouter()


@router.post("/questions")
async def questions_handler(entry: CountQuestions):
    response = await questions.get_questions(entry.questions_num)
    if type(response) == dict and response["error"]:
        raise HTTPException(status_code=400, detail=response["error"])
    else:
        return response


@router.post("/user")
async def user_handler(entry: GetUsername):
    user = await users.create_or_get_user(entry.username)
    if type(user) == dict and user["error"]:
        raise HTTPException(status_code=400, detail=user["error"])
    else:
        return user


@router.put("/file")
async def file_handler(
    user_id: int = Form(...),
    auth_token: str = Form(...),
    file: UploadFile = File(...),
):
    record = await users.try_upload_file(file, user_id, auth_token)
    if type(record) == dict and record["error"]:
        raise HTTPException(status_code=400, detail=record["error"])
    else:
        return f"{DOMAIN}/record?id={record.id}&user={record.user_id}"


@router.get("/record", tags=["user_record"])
async def record_handler(id: UUID4, user: int):
    data = await users.get_file_mp3(id, user)
    if type(data) == dict and data["error"]:
        raise HTTPException(status_code=400, detail=data["error"])
    else:
        return Response(content=data[0], media_type=data[1])
