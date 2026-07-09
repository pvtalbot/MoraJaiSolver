# tests/test_event_dispatcher.py
from morajai_solver.event_dispatcher import EventDispatcher
from morajai_solver.models.MoraEvent import MoraEvent


def test_event_dispatcher_singleton_and_emission():
    dispatcher1 = EventDispatcher()
    dispatcher2 = EventDispatcher()

    # Vérification que c'est bien le même Singleton
    assert dispatcher1 is dispatcher2

    # Variable locale pour capturer l'exécution du callback
    callback_called = False
    received_kwargs = {}

    def mock_callback(**kwargs):
        nonlocal callback_called, received_kwargs
        callback_called = True
        received_kwargs = kwargs

    # On s'abonne via la première instance
    dispatcher1.subscribe(MoraEvent.VICTORY_ACHIEVED, mock_callback)

    # On émet via la deuxième instance
    dispatcher2.emit(MoraEvent.VICTORY_ACHIEVED, message="Gagné !")

    # Vérifications
    assert callback_called is True
    assert received_kwargs.get("message") == "Gagné !"
