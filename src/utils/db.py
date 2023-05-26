import sqlalchemy
import databases
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)
