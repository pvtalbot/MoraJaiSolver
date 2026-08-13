import inspect
import logging
from typing import Callable, TypeVar

from morajai_solver.infra.events import MoraEvent

logger = logging.getLogger(__name__)

E = TypeVar("E", bound=MoraEvent)


class EventDispatcher:
    def __init__(self):
        self._listeners = {}

    def subscribe(
        self, event_type: type[E], callback: Callable[[E], None] | Callable[[], None]
    ):
        if event_type not in self._listeners:
            self._listeners[event_type] = list()
        self._listeners[event_type].append(callback)
        logger.debug(f"Nouvel abonnement à l'événement : {event_type}")

    def emit(self, event: MoraEvent):
        event_type = type(event)
        logger.debug(f"Event {event_type}")
        if event_type not in self._listeners:
            return

        for callback in self._listeners[event_type]:
            signature = inspect.signature(callback)
            if len(signature.parameters) == 0:
                callback()
            else:
                callback(event)
