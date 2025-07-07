import pytest
from sqlalchemy import text, create_engine
from sqlmodel import Session, SQLModel

from config import LEARNED_THRESHOLD
from enums import GameMode, LanguageMode, SessionState, SessionCardState
from models import Category, Deck, Card, Session as SessionModel, User, SessionCard
from orm_managers import CardManager, CategoryManager, DeckManager, StatsManager, UserManager
from services.user_service import UserService


@pytest.fixture
def test_engine():
	engine = create_engine("sqlite://", echo=False)
	SQLModel.metadata.create_all(engine)
	return engine

@pytest.fixture
def user_manager(test_engine):
	user_manager = UserManager()
	user_manager.engine = test_engine
	return user_manager

@pytest.fixture
def stats_manager(test_engine):
	stats_manager = StatsManager()
	stats_manager.engine = test_engine
	return stats_manager

@pytest.fixture
def category_manager(test_engine):
	category_manager = CategoryManager()
	category_manager.engine = test_engine
	return category_manager

@pytest.fixture
def deck_manager(test_engine):
	deck_manager = DeckManager()
	deck_manager.engine = test_engine
	return deck_manager

@pytest.fixture
def card_manager(test_engine):
	card_manager = CardManager()
	card_manager.engine = test_engine
	return card_manager

@pytest.fixture
def user_service(user_manager, stats_manager, category_manager, deck_manager, card_manager):
	return UserService(
		user_manager=user_manager,
		stats_manager=stats_manager,
		category_manager=category_manager,
		deck_manager=deck_manager,
		card_manager=card_manager
	)


@pytest.fixture
def mock_user(user_manager):
	return user_manager.create(123, "Lizzy")


@pytest.fixture
def mock_category(category_manager):
	category = Category(name="Test Category")
	with Session(category_manager.engine) as sql_session:
		sql_session.add(category)
		sql_session.commit()
		sql_session.refresh(category)

		return category.id



@pytest.fixture
def mock_deck(deck_manager, category_manager, mock_category):
	deck = Deck(name="Test Deck")
	category = category_manager.get_by_id(mock_category)
	with Session(deck_manager.engine) as sql_session:
		sql_session.add(deck)
		sql_session.commit()
		sql_session.refresh(deck)
		deck.category = category
		sql_session.add(deck)
		sql_session.commit()
		sql_session.refresh(deck)
		return deck


@pytest.fixture
def mock_card(card_manager, mock_deck):
	card = Card(front="Front", back="Back", deck_id=mock_deck.id)
	with Session(card_manager.engine) as sql_session:
		sql_session.add(card)
		sql_session.commit()
		sql_session.refresh(card)
	return card

@pytest.fixture
def mock_session(test_engine, mock_user):
	with Session(test_engine) as session:
		session_model = SessionModel(
			user_id=mock_user.id,
			deck_id=1,
			game_mode=GameMode.FLASH,
			language_mode=LanguageMode.ENG_TO_RU,
			state=SessionState.ACTIVE
		)
		session.add(session_model)
		session.commit()
		session.refresh(session_model)
		return session_model

@pytest.fixture
def setup_stats_data(test_engine):
	with Session(test_engine) as session:
		user = User(id=1, tg_id=12345, name="User")
		cards = [
			Card(id=1, deck_id=1, front="Hi", back="Привет"),
			Card(id=2, deck_id=1, front="Bye", back="Пока"),
			Card(id=3, deck_id=1, front="Thanks", back="Спасибо"),
		]
		session.add(user)
		session.add_all(cards)

		sessions = [
			SessionModel(id=100, user_id=1, deck_id=1, game_mode=GameMode.FLASH, language_mode=LanguageMode.ENG_TO_RU, state=SessionState.FINISHED),
			SessionModel(id=101, user_id=1, deck_id=1, game_mode=GameMode.FLASH, language_mode=LanguageMode.ENG_TO_RU, state=SessionState.FINISHED),
		]
		session.add_all(sessions)

		session_cards = [
			# session 100
			SessionCard(session_id=100, card_id=1, known_level=0.1, state=SessionCardState.OPENED),
			SessionCard(session_id=100, card_id=2, known_level=LEARNED_THRESHOLD + 0.1, state=SessionCardState.OPENED),

			# session 101 (позднее, новая карточка + уже встречавшаяся)
			SessionCard(session_id=101, card_id=2, known_level=LEARNED_THRESHOLD + 0.2, state=SessionCardState.SURRENDERED),
			SessionCard(session_id=101, card_id=3, known_level=LEARNED_THRESHOLD + 0.1, state=SessionCardState.OPENED),
		]
		session.add_all(session_cards)
		session.commit()

