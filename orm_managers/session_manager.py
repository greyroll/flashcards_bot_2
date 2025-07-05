from datetime import datetime
from sqlmodel import Session, select

from enums import GameMode, LanguageMode, SessionState, SessionCardState
from models import Session as SessionModel, SessionCard
from orm_managers.base_manager import BaseManager


class SessionManager(BaseManager):
	model = SessionModel # Used for inherited methods of BaseManager


	def get_by_id(self, session_id: int) -> SessionModel | None:
		"""Get game session by id."""
		with Session(self.engine) as session:
			return session.exec(select(SessionModel).where(SessionModel.id == session_id)).one_or_none()

	def create_session(self, user_id: int, deck_id: int, game_mode: GameMode, language_mode: LanguageMode) -> SessionModel:
		"""Create new game session."""
		session = SessionModel(user_id=user_id, deck_id=deck_id,  game_mode=game_mode, language_mode=language_mode, state=SessionState.CREATED)
		with Session(self.engine) as sql_session:
			sql_session.add(session)
			sql_session.commit()
			sql_session.refresh(session)
		return session

	def set_active_card(self, session_id: int, session_card_id: int):
		"""Set active card for a session."""
		with Session(self.engine) as sql_session:
			session = sql_session.get(SessionModel, session_id)
			session_card = sql_session.get(SessionCard, session_card_id)
			session.active_card_id = session_card_id
			session.state = SessionState.ACTIVE
			session_card.state = SessionCardState.OPENED
			sql_session.add(session)
			sql_session.add(session_card)
			sql_session.commit()
			sql_session.refresh(session)
			sql_session.refresh(session_card)


	def get_next_active_card(self, session_id: int) -> SessionCard | None:
		"""Get next active card for a session."""
		with Session(self.engine) as sql_session:
			statement = (
				select(SessionCard)
				.where(
					SessionCard.session_id == session_id,
					SessionCard.state == SessionCardState.NOT_OPENED
				)
				.order_by(SessionCard.created_at)
			)
			session_card = sql_session.exec(statement).first()
			return session_card

	def update_active_card(self, session_id: int, known_level: float, user_answer: str):
		"""Update active card for a session."""
		with Session(self.engine) as sql_session:
			session = sql_session.get(SessionModel, session_id)
			if session.active_card_id is None:
				raise Exception("No active card")

			session_card = sql_session.get(SessionCard, session.active_card_id)
			session_card.known_level = known_level
			session_card.user_answer = user_answer
			session_card.state = SessionCardState.OPENED

			sql_session.add(session_card)
			sql_session.commit()
			sql_session.refresh(session_card)

	def mark_hint_usage(self, session_id: int):
		"""Mark hint usage for a session."""
		with Session(self.engine) as sql_session:
			session = sql_session.get(SessionModel, session_id)
			if session.active_card_id is None:
				raise Exception("No active card")

			session_card = sql_session.get(SessionCard, session.active_card_id)
			session_card.is_hint_used = True

			sql_session.add(session_card)
			sql_session.commit()
			sql_session.refresh(session_card)

	def finish_session(self, session_id: int):
		"""Finish a session."""
		with Session(self.engine) as sql_session:
			session = sql_session.get(SessionModel, session_id)
			session.state = SessionState.FINISHED
			session.finished_at = datetime.now()

			sql_session.add(session)
			sql_session.commit()
			sql_session.refresh(session)


