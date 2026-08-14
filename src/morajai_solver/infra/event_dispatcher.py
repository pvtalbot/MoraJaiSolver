import logging
import threading
import customtkinter as ctk
from typing import Callable, TypeVar

from morajai_solver.infra.events import MoraEvent

logger = logging.getLogger(__name__)

E = TypeVar("E", bound=MoraEvent)


class EventDispatcher:
    def __init__(self):
        self._listeners = {}

    def configure_ctk_root(self, root: ctk.CTk):
        root.bind("<<AsyncMoraEvent>>", self._flush_async_queue)
        self._async_queue = []

        def event_generate():
            root.event_generate("<<AsyncMoraEvent>>", when="tail")

        self.async_event_generate = event_generate

    def subscribe(self, event_type: type[E], callback: Callable[[E], None]):
        if event_type not in self._listeners:
            self._listeners[event_type] = list()
        self._listeners[event_type].append(callback)
        logger.debug(f"Nouvel abonnement à l'événement : {event_type}")

    def emit(self, event: MoraEvent):
        if threading.current_thread() is not threading.main_thread():
            self._async_queue.append(event)
            self.async_event_generate()
        else:
            self._dispatch(event)

    def _dispatch(self, event: MoraEvent):
        event_type = type(event)
        logger.debug(f"Event {event_type}")
        if event_type not in self._listeners:
            return

        for callback in self._listeners[event_type]:
            callback(event)

    def _flush_async_queue(self, _):
        while self._async_queue:
            event = self._async_queue.pop(0)
            self._dispatch(event)
