from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Enum as SqlEnum
from enums import GameMode, LanguageMode, SessionState

from models.session_card import SessionCard

class Session(SQLModel, table=True):
	__tablename__ = "session"

	id: int = Field(default=None, primary_key=True)
	user_id: int = Field(foreign_key="user.id")
	deck_id: int = Field(foreign_key="deck.id")
	game_mode: GameMode = Field(SqlEnum(GameMode))
	language_mode: LanguageMode = Field(SqlEnum(LanguageMode))
	active_card_id: int | None = Field(default=None, foreign_key="session_card.id")
	state: SessionState = Field(SqlEnum(SessionState))
	created_at: datetime = Field(default_factory=lambda: datetime.now())
	finished_at: datetime | None = Field(default=None)

	session_cards: list["SessionCard"] = Relationship(back_populates="session", sa_relationship_kwargs={"foreign_keys": [SessionCard.session_id]})




