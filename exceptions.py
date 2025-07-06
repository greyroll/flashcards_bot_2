class ServiceError(Exception): pass

class UserNotFoundError(ServiceError): pass
class CategoryNotFoundError(ServiceError): pass
class NoCategoriesFoundError(ServiceError): pass

class DeckNotFoundError(ServiceError): pass
class NoDecksFoundError(ServiceError): pass
class NoCardsFoundError(ServiceError): pass

# class ActiveSessionAlreadyExists(ServiceError): pass
