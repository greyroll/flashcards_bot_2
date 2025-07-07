def test_get_by_id(setup_cards):
	card_manager = setup_cards
	card = card_manager.get_by_id(1)
	assert card is not None
	assert card.front == "Hi"

def test_get_all_by_deck_id(setup_cards):
	card_manager = setup_cards
	cards = card_manager.get_all_by_deck_id(deck_id=10)
	assert len(cards) == 3

def test_get_weak_cards(setup_cards):
	card_manager = setup_cards
	cards = card_manager.get_weak_cards(user_id=1, deck_id=10)
	assert len(cards) == 1
	assert cards[0].id == 1

def test_get_learned_cards(setup_cards):
	card_manager = setup_cards
	cards = card_manager.get_learned_cards(user_id=1, deck_id=10)
	assert len(cards) == 1
	assert cards[0].id == 2

def test_get_new_cards(setup_cards):
	card_manager = setup_cards
	cards = card_manager.get_new_cards(user_id=1, deck_id=10)
	assert len(cards) == 1
	assert cards[0].id == 3  # ещё не встречалась