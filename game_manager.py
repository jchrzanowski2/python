from constants import Constants
from states import *
import pygame
from typing import List
import config as c


class GameManager:
    """Class managing the game state and transitions."""

    def __init__(self) -> None:
        """Initialize the GameManager object."""
        self.current_state: GameState = MenuState()

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handle events based on the current game state.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        self.current_state.handle_events(event)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the game on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        self.current_state.draw(screen)

    def update(self) -> None:
        """Update the game state."""
        self.current_state.update()

    def change_state(self, action: int) -> None:
        """
        Change the game state based on the action.

        Args:
            action (int): The action to perform.
        """
        if action == Constants.Actions.GAME_END:
            self.current_state = EndState(
                self.current_state.world.stop,
                pygame.time.get_ticks() - self.current_state.start_time,
                self.current_state.player.statistics,
            )
            return
        elif action == Constants.Actions.GAME_START:
            self.current_state = RunState()
            return
        elif action == Constants.Actions.GAME_SCORE:
            self.current_state = ScoreState()

    def get_info(self, infos: List[int]) -> None:
        """
        Receive and process information from the game.

        Args:
            infos (List[int]): List of information to process.
        """
        while infos:
            info = infos.pop()
            if info == Constants.KILL:
                self.current_state.player.statistics.points += c.KILL_PTS
                self.current_state.player.statistics.kills += 1
            elif info == Constants.KILL_RED:
                self.current_state.player.statistics.points += c.RED_KILL_PTS
                self.current_state.player.statistics.kills += 1
                self.current_state.player.health += c.RED_KILL_HP
            elif info == Constants.KILL_PURPLE:
                self.current_state.player.statistics.points += c.PURPLE_KILL_PTS
                self.current_state.player.statistics.kills += 1
                self.current_state.player.health += c.PURPLE_KILL_HP
