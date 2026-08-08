# tests/test_event_dispatcher.py
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import MoraEvent


def test_event_dispatcher_singleton_and_emission():
    dispatcher = EventDispatcher()

    # Variable locale pour capturer l'exécution du callback
    callback_called = False
    received_kwargs = {}

    def mock_callback(**kwargs):
        nonlocal callback_called, received_kwargs
        callback_called = True
        received_kwargs = kwargs

    dispatcher.subscribe(MoraEvent.VICTORY_ACHIEVED, mock_callback)
    dispatcher.emit(MoraEvent.VICTORY_ACHIEVED, message="Gagné !")

    # Vérifications
    assert callback_called is True
    assert received_kwargs.get("message") == "Gagné !"
