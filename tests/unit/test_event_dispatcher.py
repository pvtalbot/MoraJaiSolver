# tests/test_event_dispatcher.py
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.events import VictoryAchievedEvent


def test_event_dispatcher_singleton_and_emission():
    dispatcher = EventDispatcher()

    # Variable locale pour capturer l'exécution du callback
    callback_called = False

    def mock_callback():
        nonlocal callback_called
        callback_called = True

    dispatcher.subscribe(VictoryAchievedEvent, mock_callback)
    dispatcher.emit(VictoryAchievedEvent())

    # Vérifications
    assert callback_called is True
