"""application."""
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration


class ApplicationContainer(DeclarativeContainer):
    """Application container."""

    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[
            "server",
        ],
    )
    config: Configuration = Configuration()

    # holdem_state: Provider[HoldemState] = Factory[HoldemState](
    #     HoldemState,
    # )
