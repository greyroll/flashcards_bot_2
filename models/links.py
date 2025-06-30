from sqlmodel import SQLModel, Field

class DeckCard(SQLModel, table=True):
	__tablename__ = "deck_card"

	deck_id: int = Field(foreign_key="deck.id", primary_key=True)
	card_id: int = Field(foreign_key="card.id", primary_key=True)


class CategoryDeck(SQLModel, table=True):
	__tablename__ = "category_deck"

	category_id: int = Field(foreign_key="category.id", primary_key=True)
	deck_id: int = Field(foreign_key="deck.id", primary_key=True)

