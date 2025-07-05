from sqlmodel import Session, create_engine, SQLModel

from models import Card, Category, Deck, DeckCard, CategoryDeck, Session as SessionModel, SessionCard, User
from config import DB_PATH


class BaseManager:
	model: SQLModel | None = None

	def __init__(self):
		path = f"sqlite:///{DB_PATH}"
		# print({"path": path})
		self.engine = create_engine(path)

	def create_all_tables(self):
		"""Create all tables in the database."""
		SQLModel.metadata.create_all(self.engine)

	def add(self, obj: SQLModel):
		"""Add an object to the database."""
		with Session(self.engine) as session:
			session.add(obj)
			session.commit()
			session.refresh(obj)

	def delete(self, obj_id: int):
		"""Delete an object from the database."""
		if self.model is None:
			raise AttributeError("Define model to use delete")
		with Session(self.engine) as session:
			obj = session.get(self.model, obj_id)
			session.delete(obj)
			session.commit()
