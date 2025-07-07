import pytest
from sqlmodel import Session, text

from models import Category, Deck


def test_get_or_create_user_creates(user_service):
    user = user_service.get_or_create_user(999, "TestUser")
    assert user.tg_id == 999
    assert user.name == "TestUser"


def test_get_or_create_user_returns_existing(user_service, mock_user):
    user = user_service.get_or_create_user(mock_user.tg_id, "OtherName")
    assert user.id == mock_user.id
    assert user.name == mock_user.name


def test_set_active_session_sets_id(user_service, mock_user, mock_session, user_manager):
    user_service.set_active_session(mock_user.tg_id, mock_session.id)
    updated = user_manager.get_by_tg_id(mock_user.tg_id)
    assert updated.active_session_id == mock_session.id


def test_set_active_session_user_not_found(user_service):
    with pytest.raises(Exception):
        user_service.set_active_session(99999, 1)


def test_get_words_progress_returns_zero(user_service, mock_user):
    progress = user_service.get_words_progress(mock_user.tg_id)
    assert isinstance(progress, int)


def test_get_words_progress_with_data(user_service, setup_stats_data):
    progress = user_service.get_words_progress(12345)  # из setup_stats_data
    assert progress == 2  # две карточки с known_level > LEARNED_THRESHOLD


def test_get_stats_by_deck(user_service, setup_stats_data):
    stats = user_service.get_stats_by_deck(user_tg_id=12345, deck_id=1)
    assert stats == {"cards_learned": 2, "sessions_played": 2}


def test_get_cards_by_deck_category_success(user_service, mock_category, mock_deck, mock_card):
    cards = user_service.get_cards_by_deck_category(mock_deck.name, mock_category)
    assert len(cards) == 1
    assert cards[0].id == mock_card.id


def test_get_cards_by_deck_category_no_deck(user_service, mock_category):
    with pytest.raises(Exception):
        user_service.get_cards_by_deck_category("NotExist", mock_category)


def test_get_cards_by_deck_category_no_cards(user_service, category_manager, deck_manager):
    cat = category_manager.add(Category(name="Empty"))
    deck = deck_manager.add(Deck(name="EmptyDeck"))
    with pytest.raises(Exception):
        user_service.get_cards_by_deck_category(deck.name, cat.id)


def test_get_decks_by_category_id_success(user_service, mock_category, mock_deck):
    decks = user_service.get_decks_by_category_id(mock_category)
    assert any(d.id == mock_deck.id for d in decks)


def test_get_decks_by_category_id_not_found(user_service):
    with pytest.raises(Exception):
        user_service.get_decks_by_category_id(999)


def test_get_deck_by_name_category_success(user_service, mock_category, mock_deck):
    deck = user_service.get_deck_by_name_category(mock_deck.name, mock_category)
    assert deck.id == mock_deck.id


def test_get_deck_by_name_category_not_found(user_service):
    with pytest.raises(Exception):
        user_service.get_deck_by_name_category("Nope", 999)


def test_get_top_categories_success(user_service, mock_category):
    cats = user_service.get_top_categories()
    assert any(c.id == mock_category for c in cats)


def test_get_top_categories_empty(user_service, category_manager):
    with Session(category_manager.engine) as session:
        session.exec(text("DELETE FROM category"))
        session.commit()
    with pytest.raises(Exception):
        user_service.get_top_categories()


def test_get_subcategories_by_parent_id_empty(user_service):
    with pytest.raises(Exception):
        user_service.get_subcategories_by_parent_id(999)


def test_get_category_by_name_success(user_service, category_manager):
    mock_category = Category(name="MockCategory")
    category_manager.add(mock_category)
    cat = user_service.get_category_by_name("MockCategory")
    assert cat.id == mock_category.id


def test_get_category_by_name_not_found(user_service):
    with pytest.raises(Exception):
        user_service.get_category_by_name("NotARealName")
