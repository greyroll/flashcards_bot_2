from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Enum as SqlEnum
from enums import LanguageMode, SessionCardState




class SessionCard(SQLModel, table=True):
	__tablename__ = "session_card"

	id: int = Field(default=None, primary_key=True)
	session_id: int = Field(foreign_key="session.id")
	card_id: int = Field(foreign_key="card.id")
	state: SessionCardState = Field(SqlEnum(SessionCardState))
	known_level: float = Field(default=0.0)
	user_answer: str | None = Field(default=None)
	is_hint_used: bool = False
	created_at: datetime = Field(default_factory=lambda: datetime.now())

	session: "Session" = Relationship(back_populates="session_cards", sa_relationship_kwargs={"foreign_keys": "[SessionCard.session_id]"})  # 👈 обязательно!
	card: "Card" = Relationship(back_populates="session_cards")

	def get_public_side(self, language_mode: LanguageMode) -> str:
		return self.card.front if language_mode == LanguageMode.ENG_TO_RU else self.card.back

	def get_secret_side(self, language_mode: LanguageMode) -> str:
		return self.card.back if language_mode == LanguageMode.RU_TO_ENG else self.card.front