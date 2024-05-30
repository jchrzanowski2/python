import pygame
from observer import Observer


class GameState:
    """Base class representing a game state."""

    def __init__(self) -> None:
        """
        Initialize a GameState object.
        """
        self.observer = None

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handle events in the game state.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        pass

    def update(self) -> None:
        """
        Update the game state.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the game state on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        pass

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the game state.

        Args:
            observer (Observer): The observer to attach.
        """
        self.observer = observer
