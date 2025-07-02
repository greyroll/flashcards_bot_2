from sqlmodel import SQLModel, Field, Relationship

from models.links import CategoryDeck


class Category(SQLModel, table=True):
	__tablename__ = "category"

	id: int = Field(default=None, primary_key=True)
	parent_id: int | None = Field(default=None, foreign_key="category.id")
	name: str
	description: str | None

	parent: "Category" = Relationship(back_populates="subcategories", sa_relationship_kwargs={"remote_side": "Category.id"})
	subcategories: list["Category"] = Relationship(back_populates="parent")
	decks_in_category: list["Deck"] = Relationship(back_populates="category", link_model=CategoryDeck)

