from sqlmodel import Session, select

from models import Category
from orm_managers.base_manager import BaseManager


class CategoryManager(BaseManager):
	model = Category # Used for inherited methods of BaseManager


	def get_by_id(self, cat_id: int) -> Category | None:
		"""Get category by id."""
		with Session(self.engine) as session:
			return session.exec(select(Category).where(Category.id == cat_id)).one_or_none()

	def get_by_name(self, category_name: str) -> Category | None:
		"""Get category by name."""
		with Session(self.engine) as session:
			category = session.exec(select(Category).where(Category.name == category_name)).one_or_none()
			return category

	def get_top_level_cats(self) -> list[Category]:
		"""Get top level categories."""
		with Session(self.engine) as session:
			categories = session.exec(select(Category).where(Category.parent_id == None)).all()
			return list(categories)

	def get_subcats_by_parent_id(self, parent_id: int) -> list[Category]:
		"""Get subcategories by parent id."""
		with Session(self.engine) as session:
			categories = session.exec(select(Category).where(Category.parent_id == parent_id)).all()
			return list(categories)