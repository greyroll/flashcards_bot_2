def test_get_by_id(setup_decks):
	manager, _ = setup_decks
	deck = manager.get_by_id(1)
	assert deck is not None
	assert deck.name == "English A1"


def test_get_by_name_category(setup_decks):
	manager, category_id = setup_decks
	deck = manager.get_by_name_category("English A2", category_id)
	assert deck is not None
	assert deck.name == "English A2"

def test_get_by_category(setup_decks):
	manager, category_id = setup_decks
	decks = manager.get_by_category(category_id)
	assert len(decks) == 2
	assert decks[0].name == "English A1"