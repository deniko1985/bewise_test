import datetime
import sqlalchemy

metadata = sqlalchemy.MetaData()


questions_table = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
        ),
    sqlalchemy.Column("source_id", sqlalchemy.Integer, unique=True, index=True),
    sqlalchemy.Column("question", sqlalchemy.String()),
    sqlalchemy.Column("answer", sqlalchemy.String()),
    sqlalchemy.Column("category", sqlalchemy.String()),
    sqlalchemy.Column("air_date", sqlalchemy.String()),
    sqlalchemy.Column("source_created_at", sqlalchemy.String()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), default=datetime.datetime.utcnow)
)
