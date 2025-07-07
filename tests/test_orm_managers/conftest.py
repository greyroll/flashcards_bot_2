import pytest
from sqlalchemy import text, create_engine
from sqlmodel import Session, SQLModel

from config import LEARNED_THRESHOLD
from enums import GameMode, LanguageMode, SessionState, SessionCardState
from models import Category, Deck, User, Session as SessionModel, SessionCard, Card
from orm_managers import CardManager, CategoryManager, DeckManager, SessionManager, StatsManager, UserManager


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
def setup_categories(test_engine):
	manager = CategoryManager()
	manager.engine = test_engine

	root_cat = Category(name="Top Level", description="Main", parent_id=None)
	sub_cat = Category(name="Sub Level", description="Child", parent_id=1)

	with Session(manager.engine) as session:
		session.add(root_cat)
		session.commit()
		session.refresh(root_cat)
		sub_cat.parent_id = root_cat.id
		session.add(sub_cat)
		session.commit()

	return manager


@pytest.fixture
def setup_decks(test_engine):
	manager = DeckManager()
	manager.engine = test_engine

	with Session(manager.engine) as session:

		category = Category(name="Languages")
		session.add(category)
		session.commit()

		deck1 = Deck(name="English A1", description="Basic English")
		deck2 = Deck(name="English A2", description="Elementary English")
		session.add_all([deck1, deck2])
		session.commit()

		category.decks_in_category = [deck1, deck2]
		session.add(category)
		session.commit()
		session.refresh(category)

		category_id = category.id
	return manager, category_id

@pytest.fixture
def setup_session_data(test_engine):
	manager = SessionManager()
	manager.engine = test_engine

	with Session(manager.engine) as session:

		user = User(name="Test User", tg_id=111)
		deck = Deck(name="Test Deck", description="Testing deck")

		session.add_all([user, deck])
		session.commit()
		session.refresh(user)
		session.refresh(deck)

		new_session = SessionModel(
			user_id=user.id,
			deck_id=deck.id,
			game_mode=GameMode.FLASH,
			language_mode=LanguageMode.ENG_TO_RU,
			state=SessionState.CREATED
		)
		session.add(new_session)
		session.commit()
		session.refresh(new_session)

		card1 = Card(deck_id = deck.id, front="Q1", back="A1")
		card2 = Card(deck_id = deck.id, front="Q2", back="A2")
		session.add_all([card1, card2])
		session.commit()
		session.refresh(card1)
		session.refresh(card2)

		session_card1 = SessionCard(session_id=new_session.id, card_id=card1.id)
		session_card2 = SessionCard(session_id=new_session.id, card_id=card2.id)
		session.add_all([session_card1, session_card2])
		session.commit()
		session.refresh(session_card1)
		session.refresh(session_card2)

		return manager, new_session.id, session_card1.id, session_card2.id


@pytest.fixture
def setup_cards(test_engine):
	manager = CardManager()
	manager.engine = test_engine
	with Session(manager.engine) as session:

		user = User(id=1, tg_id=12345, name="TestUser")
		session.add(user)

		cards = [
			Card(id=1, deck_id=10, front="Hi", back="Привет"),
			Card(id=2, deck_id=10, front="Bye", back="Пока"),
			Card(id=3, deck_id=10, front="Thanks", back="Спасибо"),
		]
		session.add_all(cards)
		session.commit()

		session_model = SessionModel(
			id=100,
			user_id=1,
			deck_id=10,
			game_mode=GameMode.FLASH,
			language_mode=LanguageMode.ENG_TO_RU,
			state=SessionState.ACTIVE
		)
		session.add(session_model)
		session.commit()

		session_cards = [
			SessionCard(session_id=100, card_id=1, known_level=0),  # слабая
			SessionCard(session_id=100, card_id=2, known_level=LEARNED_THRESHOLD + 1),  # выучена
		]
		session.add_all(session_cards)
		session.commit()
	return manager

@pytest.fixture
def setup_stats_data(test_engine):
	manager = StatsManager()
	manager.engine = test_engine
	with Session(manager.engine) as session:
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
	return manager

