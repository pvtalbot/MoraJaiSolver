import logging

from morajai_solver.infra.events import MoraEvent
from morajai_solver.infra.singleton import SingletonMeta

logger = logging.getLogger(__name__)


class EventDispatcher(metaclass=SingletonMeta):
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type: MoraEvent, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = list()
        self._listeners[event_type].append(callback)
        logger.debug(f"Nouvel abonnement à l'événement : {event_type}")

    def emit(self, event_type: MoraEvent, *args, **kwargs):
        logger.debug(f"Event {event_type}, {kwargs}")
        if event_type not in self._listeners:
            return

        for callback in self._listeners[event_type]:
            callback(*args, **kwargs)
