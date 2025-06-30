from sqlmodel import SQLModel, Field, Relationship

from models.links import DeckCard


class Card(SQLModel, table=True):
	__tablename__ = "card"

	id: int = Field(default=None, primary_key=True)
	front: str
	back: str
	deck_id: int = Field(foreign_key="deck.id")

	decks: list["Deck"] = Relationship(back_populates="cards", link_model=DeckCard)
	session_cards: list["SessionCard"] = Relationship(back_populates="card")


