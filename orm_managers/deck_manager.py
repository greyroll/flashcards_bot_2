from sqlmodel import Session, select

from models import Deck, Category
from orm_managers.base_manager import BaseManager


class DeckManager(BaseManager):
	model = Deck # Used for inherited methods of BaseManager

	def get_by_id(self, deck_id: int) -> Deck | None:
		"""Get deck by id."""
		with Session(self.engine) as session:
			return session.exec(select(Deck).where(Deck.id == deck_id)).one_or_none()

	def get_by_name_category(self, deck_name: str, category_id: int) -> Deck | None:
		with Session(self.engine) as session:
			deck = session.exec(select(Deck).join(Deck.category).where(Deck.name == deck_name, Category.id == category_id)).one_or_none()
			return deck

	def get_by_category(self, category_id: int) -> list[Deck]:
		with Session(self.engine) as session:
			decks = session.exec(select(Deck).join(Deck.category).where(Category.id == category_id)).all()
			return list(decks)

