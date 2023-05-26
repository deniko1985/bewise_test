import requests
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from models.questions import questions_table
from utils.db import database


async def get_questions(count: int):
    try:
        query = questions_table.select().order_by(questions_table.c.id.desc())
        record = await database.fetch_one(query)
        await request_for_questions(count)
        if record:
            return record
        else:
            return {}
    except Exception as error:
        return {"error": str(error)}


async def request_for_questions(count: int):
    to_load = count
    while to_load > 0:
        try:
            questions = requests.get(f"https://jservice.io/api/random?count={to_load}")
            for question in questions.json():
                if (await try_save(question)):
                    to_load -= 1
        except SQLAlchemyError as error:
            return {"error": str(error)}
        except requests.ConnectionError:
            return {"error": "ConnectionError"}
        except requests.exceptions.HTTPError:
            return {"error": "HTTPError"}
        except requests.exceptions.RequestException:
            return {"error": f"status_code: {questions.status_code}"}


async def try_save(question: dict):
    query = questions_table.select().where(questions_table.c.source_id == question["id"])
    record = await database.fetch_one(query)
    if not record:
        q = questions_table.insert().values(
            source_id=question["id"],
            question=question["question"],
            answer=question["answer"],
            category=question["category"]["title"],
            air_date=question["airdate"],
            source_created_at=question["created_at"],
            created_at=datetime.now()
        )
        await database.execute(q)
        return True
    else:
        return False
