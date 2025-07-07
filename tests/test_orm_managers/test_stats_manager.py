from config import LEARNED_THRESHOLD
from enums import SessionCardState


def test_get_words_total_progress(setup_stats_data):
	stats_manager = setup_stats_data
	assert stats_manager.get_words_total_progress(user_id=1) == 2

def test_get_cards_learned_by_deck(setup_stats_data):
	stats_manager = setup_stats_data
	assert stats_manager.get_cards_learned_by_deck(user_id=1, deck_id=1) == 2

def test_get_sessions_played_by_deck(setup_stats_data):
	stats_manager = setup_stats_data
	assert stats_manager.get_sessions_played_by_deck(user_id=1, deck_id=1) == 2

def test_get_total_cards_played_by_session(setup_stats_data):
	stats_manager = setup_stats_data
	cards = stats_manager.get_total_cards_played_by_session(session_id=100)
	assert len(cards) == 2
	assert all(card.state != SessionCardState.NOT_OPENED for card in cards)

def test_get_cards_learned_by_session(setup_stats_data):
	stats_manager = setup_stats_data
	cards = stats_manager.get_cards_learned_by_session(session_id=101)
	assert len(cards) == 2
	assert all(card.known_level >= LEARNED_THRESHOLD for card in cards)

def test_get_new_cards_learned_by_session(setup_stats_data):
	stats_manager = setup_stats_data
	cards = stats_manager.get_new_cards_learned_by_session(session_id=101)
	assert len(cards) == 1
	assert cards[0].card_id == 3

def test_get_remaining_cards_by_deck(setup_stats_data):
	stats_manager = setup_stats_data
	cards = stats_manager.get_remaining_cards_by_deck(user_id=1, deck_id=1)
	assert {card.card_id for card in cards} == {1}