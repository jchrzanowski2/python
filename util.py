import pygame
from constants import Constants

pygame.font.init()
font = pygame.font.Font(None, 20)
BORDER = 20


class Button:
    """Class representing a clickable button in the game."""

    def __init__(
        self, text: str, left: int, top: int, function=lambda x, y: None
    ) -> None:
        """
        Initialize a Button object.

        Args:
            text (str): The text displayed on the button.
            left (int): The left coordinate of the button.
            top (int): The top coordinate of the button.
            function (callable): The function to be called when the button is clicked.
                Default is a function that does nothing.
        """
        self.text = text
        self.text_surface = font.render(self.text, True, Constants.BLACK)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (
            left + BORDER + self.text_rect.width // 2,
            top + BORDER + self.text_rect.height // 2,
        )
        self.rect = pygame.Rect(
            left,
            top,
            self.text_rect.width + 2 * BORDER,
            self.text_rect.height + 2 * BORDER,
        )
        self.function: function = function
        self.was_clicked = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button on the screen."""
        if self.was_clicked:
            pygame.draw.rect(screen, Constants.WHITE, self.rect)
            self.was_clicked -= 1
        else:
            pygame.draw.rect(screen, Constants.GREY, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def clicked(self, x: int, y: int) -> bool:
        """
        Check if the button is clicked.

        Args:
            x (int): The x-coordinate of the click.
            y (int): The y-coordinate of the click.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        self.was_clicked = 10
        return self.rect.collidepoint(x, y)


font = pygame.font.Font(None, 36)


def make_surface(
    text: str, position: tuple[int, int], *, to_left: bool = False
) -> tuple[pygame.Surface, pygame.Rect]:
    """
    Create a surface with text rendered on it.

    Args:
        text (str): The text to render on the surface.
        position (tuple): The position of the text surface.
        to_left (bool, optional): If True, align the text surface to the left of the position.
            Defaults to False.

    Returns:
        tuple[pygame.Surface, pygame.Rect]: A tuple containing the text surface and its rectangle.
    """
    text_surface = font.render(text, True, Constants.BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    if to_left:
        text_rect.left = position[0]

    return text_surface, text_rect
