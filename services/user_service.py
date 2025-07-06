from exceptions import UserNotFoundError, NoCategoriesFoundError, CategoryNotFoundError, NoDecksFoundError, \
	DeckNotFoundError, NoCardsFoundError
from models import Category, Deck
from orm_managers import UserManager, StatsManager, CategoryManager, DeckManager, CardManager


class UserService:
	def __init__(self, user_manager: UserManager, stats_manager: StatsManager, category_manager: CategoryManager, deck_manager: DeckManager, card_manager: CardManager):
		self.user_manager = user_manager
		self.stats_manager = stats_manager
		self.category_manager = category_manager
		self.deck_manager = deck_manager
		self.card_manager = card_manager

	# 	region User methods

	def get_or_create_user(self, user_tg_id: int, user_name: str, is_admin: bool = False):
		"""Get user from database or create new if not found."""
		user = self.user_manager.get_by_tg_id(user_tg_id)
		if not user:
			user = self.user_manager.create(user_tg_id, user_name, is_admin)
		return user

	def set_active_session(self, user_tg_id: int, session_id: int):
		"""Set active training session for user."""
		user = self.user_manager.get_by_tg_id(user_tg_id)
		if not user:
			raise UserNotFoundError(f"User with tg_id {user_tg_id} not found")
		self.user_manager.set_active_session(user.id, session_id)

	# endregion

	# region Stats methods

	def get_words_progress(self, user_tg_id: int):
		"""Get total count of cards learned by user."""
		user = self.user_manager.get_by_tg_id(user_tg_id)
		if not user:
			raise UserNotFoundError(f"User with tg_id {user_tg_id} not found")
		return self.stats_manager.get_words_total_progress(user.id)

	def get_stats_by_deck(self, user_tg_id: int, deck_id: int) -> dict [str: int]:
		"""Get count of cards learned by user in a specific deck."""
		user = self.user_manager.get_by_tg_id(user_tg_id)
		if not user:
			raise UserNotFoundError(f"User with tg_id {user_tg_id} not found")
		cards_learned_count = self.stats_manager.get_cards_learned_by_deck(user.id, deck_id)
		sessions_played_count = self.stats_manager.get_sessions_played_by_deck(user.id, deck_id)
		return {"cards_learned": cards_learned_count, "sessions_played": sessions_played_count}

	# endregion

	# 	region Deck and Card methods
	def get_cards_by_deck_category(self, deck_name: str, category_id: int):
		deck = self.deck_manager.get_by_name_category(deck_name, category_id)
		if not deck:
			raise DeckNotFoundError(f"Deck with name {deck_name} not found in category {category_id}")
		cards = self.card_manager.get_all_by_deck_id(deck.id)
		if len(cards) == 0:
			raise NoCardsFoundError(f"No cards found for deck {deck_name} in category {category_id}")
		return cards

	def get_decks_by_category_id(self, category_id: int) -> list[Deck]:
		decks = self.deck_manager.get_by_category(category_id)
		if len(decks) == 0:
			raise NoDecksFoundError(f"No decks found for category id {category_id}")
		return decks

	def get_deck_by_name_category(self, deck_name: str, category_id: int) -> Deck:
		deck = self.deck_manager.get_by_name_category(deck_name, category_id)
		if not deck:
			raise DeckNotFoundError(f"Deck with name {deck_name} not found in category {category_id}")
		return deck

	# endregion

	# region Category methods
	def get_top_categories(self) -> list[Category]:
		"""Get top level categories."""
		top_cats = self.category_manager.get_top_level_cats()
		if len(top_cats) == 0:
			raise NoCategoriesFoundError(f"No top level categories found")
		return top_cats

	def get_subcategories_by_parent_id(self, parent_id: int) -> list[Category]:
		"""Get subcategories by parent id."""
		subcats = self.category_manager.get_subcats_by_parent_id(parent_id)
		if len(subcats) == 0:
			raise NoCategoriesFoundError(f"No subcategories found for parent id {parent_id}")
		return subcats

	def get_category_by_name(self, cat_name: str) -> Category:
		"""Get category by name."""
		category = self.category_manager.get_by_name(cat_name)
		if not category:
			raise CategoryNotFoundError(f"Category with name {cat_name} not found")
		return category

	# endregion