from enum import Enum

class GameMode(str, Enum):
	FLASH = "flash"
	QUIZ = "quiz"
	TEXT = "text"
	AUDIO = "audio"


class LanguageMode(str, Enum):
	ENG_TO_RU = "eng_to_ru"
	RU_TO_ENG = "ru_to_eng"


class SessionState(str, Enum):
	ACTIVE = "active"
	FINISHED = "finished"
	ABANDONED = "abandoned"


class SessionCardState(str, Enum):
	NOT_OPENED = "not_opened"
	OPENED = "opened"
	SURRENDERED = "surrendered"