import pygame
from constants import Constants
from character import Character

class SpriteGroups:
    """Class representing different groups of sprites in the game."""

    def __init__(self) -> None:
        """Initialize sprite groups."""
        self.decoration_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.diamond_group = pygame.sprite.Group()

    def update_draw(
        self, screen: pygame.Surface, player: "Player", world
    ) -> None | int:
        """
        Update and draw sprite groups on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
            player (Player): The player character object.
            world (World): The world object.

        Returns:
            None | int: If a condition is met, returns an integer.
        """
        self.decoration_group.update()
        self.water_group.update()
        self.exit_group.update(player, world)
        self.diamond_group.update(player)
        self.decoration_group.draw(screen)
        self.water_group.draw(screen)
        self.exit_group.draw(screen)
        self.diamond_group.draw(screen)


class Decorations(pygame.sprite.Sprite):
    """Class representing decoration objects in the game."""

    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        """
        Initialize a decoration object.

        Args:
            img (pygame.Surface): The image of the decoration.
            x (int): The x-coordinate of the decoration.
            y (int): The y-coordinate of the decoration.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + Constants.TILE_SIZE // 2,
            y + (Constants.TILE_SIZE - self.image.get_height()),
        )

    def update(self):
        """Update the decoration object."""
        self.rect.x += Constants.screen_scroll


class Water(pygame.sprite.Sprite):
    """Class representing water objects in the game."""

    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        """
        Initialize a water object.

        Args:
            img (pygame.Surface): The image of the water.
            x (int): The x-coordinate of the water.
            y (int): The y-coordinate of the water.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + Constants.TILE_SIZE // 2,
            y + (Constants.TILE_SIZE - self.image.get_height()),
        )

    def update(self):
        """Update the water object."""
        self.rect.x += Constants.screen_scroll


class Exit(pygame.sprite.Sprite):
    """Class representing the exit object in the game."""

    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        """
        Initialize an exit object.

        Args:
            img (pygame.Surface): The image of the exit.
            x (int): The x-coordinate of the exit.
            y (int): The y-coordinate of the exit.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + Constants.TILE_SIZE // 2,
            y + (Constants.TILE_SIZE - self.image.get_height()),
        )

    def update(self, player: Character, world: "World"):
        """
        Update the exit object.

        Args:
            player (Character): The player character object.
            world (World): The world object.
        """
        self.rect.x += Constants.screen_scroll
        if pygame.sprite.collide_rect(self, player):
            if world.map_no == Constants.LEVEL_NUM:
                world.stop = True
            else:
                world.map_no += 1


class Diamond(pygame.sprite.Sprite):
    """Class representing diamond objects in the game."""

    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        """
        Initialize a diamond object.

        Args:
            img (pygame.Surface): The image of the diamond.
            x (int): The x-coordinate of the diamond.
            y (int): The y-coordinate of the diamond.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + Constants.TILE_SIZE // 2,
            y + (Constants.TILE_SIZE - self.image.get_height()),
        )

    def update(self, player: Character) -> None:
        """
        Update the diamond object.

        Args:
            player (Character): The player character object.
        """
        self.rect.x += Constants.screen_scroll
        if pygame.sprite.collide_rect(self, player):
            player.statistics.points += 100
            self.kill()
