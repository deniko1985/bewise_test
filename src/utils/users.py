import uuid
import os
import mimetypes
from pydub import AudioSegment
from sqlalchemy.exc import SQLAlchemyError
from pydantic.types import UUID4

from models.users import users_table as users, audio_recording_table as audio_recording
from utils.db import database


PATH_AUDIO_WAV = "./audio_files/wav/"
PATH_AUDIO_MP3 = "./audio_files/mp3/"


async def create_or_get_user(username: str):
    try:
        query = users.select().where(users.c.username == username)
        record = await database.fetch_one(query)
        if not record:
            query = (
                        users.insert()
                        .values(
                            username=username,
                            auth_token=uuid.uuid4()
                        )
                        .returning(
                            users.c.id,
                            users.c.auth_token,
                        )
                    )
            return await database.fetch_one(query)
        else:
            return record
    except SQLAlchemyError as error:
        return {"error": str(error)}


async def get_user_by_id(user_id: int, auth_token: str = None):
    try:
        q = users.select()
        if user_id:
            q = q.where(users.c.id == user_id)
        if auth_token:
            q = q.where(users.c.auth_token == auth_token)
        return await database.fetch_one(q)
    except SQLAlchemyError as error:
        return {"error": str(error)}


async def convert_file_to_mp3(filename: str, user_id: int, auth_token: str):
    try:
        new_filename = uuid.uuid4()
        user = await get_user_by_id(user_id=user_id, auth_token=auth_token)
        if user:
            AudioSegment.from_wav(filename).export(f"{PATH_AUDIO_MP3}{new_filename}.mp3", format="mp3")
            query = (
                        audio_recording.insert()
                        .values(
                            id=new_filename,
                            user_id=user_id,
                            path=f"{PATH_AUDIO_MP3}{new_filename}.mp3",
                        )
                        .returning(
                            audio_recording.c.id,
                            audio_recording.c.user_id,
                        )
                    )
            return await database.fetch_one(query)
        else:
            return {"error": "User does not exist"}
    except SQLAlchemyError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


async def try_upload_file(file, user_id, auth_token):
    try:
        filename = f"{PATH_AUDIO_WAV}{str(uuid.uuid4())}.wav"
        with open(filename, "wb+") as f:
            f.write(file.file.read())
            f.close()
        record = await convert_file_to_mp3(filename, user_id, auth_token)
        return record
    except Exception:
        os.remove(filename)
        return {"error": "file upload error"}


async def get_file_mp3(record_id: UUID4, user_id: int):
    try:
        user = await get_user_by_id(user_id=user_id)
        if user:
            query = (
                        audio_recording.select()
                        .where(audio_recording.c.id == record_id)
                        .where(audio_recording.c.user_id == user_id)
                    )
            record = await database.fetch_one(query)
            if record:
                mimetype = mimetypes.guess_type(record.path)[0]
                with open(record.path, "rb") as fs:
                    data = fs.read()
                return [data, mimetype]
            else:
                return {"error": "Audio file does not exist"}
        else:
            return {"error": "User does not exist"}
    except SQLAlchemyError as error:
        return {"error": str(error)}
