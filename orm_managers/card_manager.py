from sqlmodel import Session, select

from config import LEARNED_THRESHOLD
from models import Card, SessionCard, Session as SessionModel, User
from orm_managers.base_manager import BaseManager


class CardManager(BaseManager):
	model = Card # Used for inherited methods of BaseManager

	def get_by_id(self, card_id: int) -> Card | None:
		"""Get card by id."""
		with Session(self.engine) as session:
			return session.exec(select(Card).where(Card.id == card_id)).one_or_none()


	def get_all_by_deck_id(self, deck_id: int) -> list[Card]:
		"""Get all cards by deck id."""
		with Session(self.engine) as session:
			cards = session.exec(select(Card).where(Card.deck_id == deck_id)).all()
			return list(cards)

	# limit(5)? or random.sample
	def get_weak_cards(self, user_id: int, deck_id: int) -> list[Card]:
		"""
		Get weak cards for a user in a specific deck.
		Weak cards - cards shown before which user hasn't mastered yet
		"""

		with Session(self.engine) as session:
			statement = (
				select(Card)
				.select_from(Card)
				.join(SessionCard, SessionCard.card_id == Card.id)
				.join(SessionModel, SessionModel.id == SessionCard.session_id)
				.where(
					SessionModel.user_id == user_id,
					SessionModel.deck_id == deck_id,
					SessionCard.known_level < LEARNED_THRESHOLD
				)
				.group_by(Card.id)
			)
			cards = session.exec(statement).all()
			return list(cards)

	def get_new_cards(self, user_id: int, deck_id: int) -> list[Card]:
		"""
		Get new cards for a user in a specific deck.
		New cards - cards that have not been shown to the user yet.
		"""
		with Session(self.engine) as session:
			# ids of all cards shown before
			subquery = (
				select(SessionCard.card_id)
				.join(SessionModel, SessionCard.session_id == SessionModel.id)
				.where(
					SessionModel.user_id == user_id,
					SessionModel.deck_id == deck_id
				)
				.group_by(SessionCard.card_id)
			)

			# all cards except those shown before
			statement = (
				select(Card)
				.where(Card.deck_id == deck_id)
				.where(Card.id.not_in(subquery))
			)

			cards = session.exec(statement).all()
			return list(cards)

	def get_learned_cards(self, user_id: int, deck_id: int) -> list[Card]:
		"""
		Get learned cards for a user in a specific deck.
		Learned cards - cards shown before which user has mastered.
		"""
		with Session(self.engine) as session:
			statement = (
				select(Card)
				.join(SessionCard, SessionCard.card_id == Card.id)
				.join(SessionModel, SessionModel.id == SessionCard.session_id)
				.where(
					Card.deck_id == deck_id,
					SessionModel.user_id == user_id,
					SessionModel.deck_id == deck_id,
					SessionCard.known_level >= LEARNED_THRESHOLD
				)
				.group_by(Card.id)
			)
			cards = session.exec(statement).all()
			return list(cards)

