"""application."""
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Provider, Factory, Singleton

from src.core.deck.abstract.deck import AbstractDeck
from src.core.deck.deck import LongDeck
from src.core.games.abstract.rule import AbstractRule
from src.core.games.texas_holdem.rule import HoldEmPokerRule
from src.core.state.holdem_state import HoldemState
from src.dispatcher import Dispatcher


class ApplicationContainer(DeclarativeContainer):
    """Application container."""

    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=["src.routes"],
    )
    config: Configuration = Configuration()
    poker_deck: Provider[AbstractDeck] = Factory[LongDeck](
        LongDeck,
    )
    holdem_rule: Provider[AbstractRule] = Factory[HoldEmPokerRule](
        HoldEmPokerRule,
        deck=poker_deck
    )
    holdem_state: Provider[HoldemState] = Factory[HoldemState](
        HoldemState,
        rule=holdem_rule,
    )
    dispatcher_holdem: Provider[Dispatcher] = Singleton[Dispatcher](
        Dispatcher,
        holdem_state,
    )
