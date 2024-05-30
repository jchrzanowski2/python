import pygame
from constants import Constants


class Bullet(pygame.sprite.Sprite):
    """Class representing a bullet in the game."""

    def __init__(self, x: int, y: int, direction: int) -> None:
        """
        Initialize a Bullet object.

        Args:
            x (int): The x-coordinate of the bullet.
            y (int): The y-coordinate of the bullet.
            direction (int): The direction in which the bullet will move.
        """
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load("img/icons/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, player) -> None:
        """
        Update the position of the bullet.

        Args:
            player: The player character to check for collisions.
        """
        self.rect.x += self.direction * self.speed

        if self.rect.right < 0 or self.rect.left > Constants.SCREEN_WIDTH:
            self.kill()

        if pygame.sprite.spritecollide(player, Constants.bullet_group, False):
            if player.alive:
                player.health -= 20
                self.kill()

        for enemy in Constants.enemy_group:
            if pygame.sprite.spritecollide(enemy, Constants.bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
