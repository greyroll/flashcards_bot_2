import pytest
from datetime import datetime
from sqlmodel import Session, delete

from models import Session as SessionModel, SessionCard, Deck, User, Card
from orm_managers.session_manager import SessionManager
from enums import GameMode, LanguageMode, SessionState, SessionCardState


def test_get_by_id(setup_session_data):
	manager, session_id, _, _ = setup_session_data
	session = manager.get_by_id(session_id)
	assert session is not None
	assert session.id == session_id


def test_create_session(setup_session_data):
	manager, _, _, _ = setup_session_data
	session = manager.create_session(user_id=111, deck_id=1, game_mode=GameMode.FLASH, language_mode=LanguageMode.ENG_TO_RU)
	assert session.id is not None
	assert session.user_id == 111
	assert session.deck_id == 1
	assert session.game_mode == GameMode.FLASH
	assert session.language_mode == LanguageMode.ENG_TO_RU
	assert session.state == SessionState.CREATED


def test_set_active_card(setup_session_data):
	manager, session_id, card1_id, _ = setup_session_data
	manager.set_active_card(session_id, card1_id)

	with Session(manager.engine) as s:
		session = s.get(SessionModel, session_id)
		assert session.active_card_id == card1_id
		assert session.state == SessionState.ACTIVE

		card = s.get(SessionCard, card1_id)
		assert card.state == SessionCardState.OPENED

def test_get_next_active_card(setup_session_data):
	manager, session_id, card1_id, _ = setup_session_data
	next_card = manager.get_next_active_card(session_id)
	assert next_card is not None
	assert next_card.id == card1_id

def test_update_active_card(setup_session_data):
	manager, session_id, card1_id, _ = setup_session_data
	manager.set_active_card(session_id, card1_id)
	manager.update_active_card(session_id, known_level=0.8, user_answer="A1")

	with Session(manager.engine) as s:
		card = s.get(SessionCard, card1_id)
		assert card.known_level == 0.8
		assert card.user_answer == "A1"
		assert card.state == SessionCardState.OPENED

def test_mark_hint_usage(setup_session_data):
	manager, session_id, card1_id, _ = setup_session_data
	manager.set_active_card(session_id, card1_id)
	manager.mark_hint_usage(session_id)

	with Session(manager.engine) as s:
		card = s.get(SessionCard, card1_id)
		assert card.is_hint_used is True

def test_finish_session(setup_session_data):
	manager, session_id, *_ = setup_session_data
	manager.finish_session(session_id)

	with Session(manager.engine) as s:
		sess = s.get(SessionModel, session_id)
		assert sess.state == SessionState.FINISHED
		assert isinstance(sess.finished_at, datetime)
