from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    tg_id: int = Field(index=True, unique=True)
    name: str
    is_admin: bool = False
    active_session_id: int | None = Field(default=None, foreign_key="session.id")

