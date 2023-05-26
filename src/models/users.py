import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

metadata = sqlalchemy.MetaData()


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        sqlalchemy.Sequence("users_id_seq"),
        primary_key=True,
        autoincrement=True
        ),
    sqlalchemy.Column("username", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column(
        "auth_token",
        UUID(as_uuid=False),
        default=""),
)

audio_recording_table = sqlalchemy.Table(
    "audio_recording",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=False),
        unique=True,
        index=True,
        primary_key=True,
        ),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("path", sqlalchemy.String()),
)
