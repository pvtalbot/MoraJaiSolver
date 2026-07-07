import logging

logger = logging.getLogger(__name__)

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            logger.debug(f"Création de l'instance unique de la classe : {cls.__name__}")
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class EventDispatcher(metaclass=SingletonMeta):
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type: str, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = list()
        self._listeners[event_type].append(callback)
        logger.debug(f"Nouvel abonnement à l'événement : {event_type}")

    def emit(self, event_type: str, *args, **kwargs):
        logger.debug(f"Event {event_type}, {kwargs}")
        if event_type not in self._listeners:
            return

        for callback in self._listeners[event_type]:
            callback(*args, **kwargs)