from datetime import datetime
from sqlmodel import Session, select, or_

from config import LEARNED_THRESHOLD
from enums import GameMode, LanguageMode, SessionState, SessionCardState
from models import Session as SessionModel, SessionCard
from orm_managers.base_manager import BaseManager


class StatsManager(BaseManager):
	model = SessionModel # Used for inherited methods of BaseManager


	def get_words_total_progress(self, user_id: int) -> int:
		"""
		Get total count of cards learned by user.
		Learned cards - cards with known_level >= LEARNED_THRESHOLD
		"""

		with Session(self.engine) as session:
			statement = (
				select(SessionCard.id)
				.join(SessionModel, SessionCard.session_id == SessionModel.id)
				.where(
					SessionModel.user_id == user_id,
					SessionCard.known_level >= LEARNED_THRESHOLD
				)
				.group_by(SessionCard.card_id)  # считаем только уникальные карточки
			)
			count = len(session.exec(statement).all())
			return count

	def get_cards_learned_by_deck(self, user_id: int, deck_id: int) -> int:
		"""
		Get count of cards learned by user in a specific deck.
		Learned cards - cards with known_level >= LEARNED_THRESHOLD
		"""
		with Session(self.engine) as session:
			statement = (
				select(SessionCard.card_id)
				.join(SessionModel, SessionCard.session_id == SessionModel.id)
				.where(
					SessionModel.user_id == user_id,
					SessionModel.deck_id == deck_id,
					SessionCard.known_level >= LEARNED_THRESHOLD
				)
				.group_by(SessionCard.card_id)
			)
			count = len(session.exec(statement).all())
			return count

	def get_sessions_played_by_deck(self, user_id: int, deck_id: int) -> int:
		"""Get count of sessions played by user in a specific deck."""
		with Session(self.engine) as session:
			statement = (
				select(SessionModel.id)
				.where(
					SessionModel.user_id == user_id,
					SessionModel.deck_id == deck_id,
					SessionModel.state == SessionState.FINISHED
				)
			)
			count = len(session.exec(statement).all())
			return count

	def get_total_cards_played_by_session(self, session_id: int) -> list[SessionCard]:
		"""Get count of all cards played by session."""
		with Session(self.engine) as session:
			statement = select(SessionCard).where(SessionCard.session_id == session_id, SessionCard.state != SessionCardState.NOT_OPENED)
			return list(session.exec(statement).all())

	def get_cards_learned_by_session(self, session_id: int) -> list[SessionCard]:
		"""Get count of cards learned by session."""
		with Session(self.engine) as session:
			statement = (
				select(SessionCard)
				.where(
					SessionCard.session_id == session_id,
					SessionCard.known_level >= LEARNED_THRESHOLD
				)
			)
			return list(session.exec(statement).all())

	def get_new_cards_learned_by_session(self, session_id: int) -> list[SessionCard]:
		"""
		Get count of new cards learned by session.
		New cards - cards that have not been shown to the user yet.
		"""
		with Session(self.engine) as session:
			current_session = session.get(SessionModel, session_id)

			# ids of cards from previous sessions
			subquery = (
				select(SessionCard.card_id)
				.join(SessionModel, SessionModel.id == SessionCard.session_id)
				.where(
					SessionModel.user_id == current_session.user_id,
					SessionModel.deck_id == current_session.deck_id,
					SessionModel.id < session_id
				)
			)
			old_card_ids = set(session.exec(subquery).all())

			# cards from current session that have not been shown before
			statement = (
				select(SessionCard)
				.where(
					SessionCard.session_id == session_id,
					SessionCard.known_level >= LEARNED_THRESHOLD
				)
			)
			candidates = session.exec(statement).all()

			return [card for card in candidates if card.card_id not in old_card_ids]

	def get_remaining_cards_by_deck(self, user_id: int, deck_id: int) -> list[SessionCard]:
		"""
		Get count of remaining cards by deck.
		Remaining cards - cards which user hasn't mastered yet or those that have not been shown yet.
		"""
		with Session(self.engine) as session:
			statement = (
				select(SessionCard)
				.join(SessionModel, SessionModel.id == SessionCard.session_id)
				.where(
					SessionModel.user_id == user_id,
					SessionModel.deck_id == deck_id,
					or_(
        				SessionCard.known_level < LEARNED_THRESHOLD,
        		SessionCard.known_level.is_(None)
    )
				)
			)
			return list(session.exec(statement).all())
