from sqlmodel import SQLModel, Field, Relationship

from models.links import DeckCard, CategoryDeck


class Deck(SQLModel, table=True):
	__tablename__ = "deck"

	id: int = Field(default=None, primary_key=True)
	name: str
	description: str | None

	cards: list["Card"] = Relationship(back_populates="linked_decks", link_model=DeckCard)
	category: "Category" = Relationship(back_populates="decks_in_category", link_model=CategoryDeck)




