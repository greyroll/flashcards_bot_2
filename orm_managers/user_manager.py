from sqlmodel import Session, select

from models import User, Session as SessionModel
from orm_managers.base_manager import BaseManager


class UserManager(BaseManager):
	model = User # Used for inherited methods of BaseManager

	def get_by_tg_id(self, tg_id: int) -> User | None:
		"""Get user by telegram id."""
		with Session(self.engine) as session:
			return session.exec(select(User).where(User.tg_id == tg_id)).one_or_none()

	def create(self, tg_id: int, name: str, is_admin: bool = False) -> User:
		"""Create user and add to database."""
		user = User(tg_id=tg_id, name=name, is_admin=is_admin)
		self.add(user)
		return user

	def set_active_session(self, user_id: int, session_id: int):
		"""Set active training session for user."""
		with Session(self.engine) as session:
			user = session.get(User, user_id)
			user.active_session_id = session_id
			session.add(user)
			session.commit()
			session.refresh(user)

	def get_active_session(self, user_id: int) -> SessionModel | None:
		"""Get active training session for user."""
		with Session(self.engine) as session:
			user = session.get(User, user_id)
			active_session = session.get(SessionModel, user.active_session_id)
			return active_session



