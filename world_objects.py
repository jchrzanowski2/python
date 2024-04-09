import pygame
from constants import Constants


class SpriteGroups:
    def __init__(self) -> None:
        self.decoration_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.diamond_group = pygame.sprite.Group()

    def update_draw(self, screen: pygame.Surface, player: "Player") -> None:
        self.decoration_group.update()
        self.water_group.update()
        self.exit_group.update()
        self.diamond_group.update(player)
        self.decoration_group.draw(screen)
        self.water_group.draw(screen)
        self.exit_group.draw(screen)
        self.diamond_group.draw(screen)


# Code repetition, but TODO different collision handling for each
class Decorations(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + Constants.TILE_SIZE // 2,
            y + (Constants.TILE_SIZE - self.image.get_height()),
        )

    def update(self):
        self.rect.x += Constants.screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + Constants.TILE_SIZE // 2,
            y + (Constants.TILE_SIZE - self.image.get_height()),
        )

    def update(self):
        self.rect.x += Constants.screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + Constants.TILE_SIZE // 2,
            y + (Constants.TILE_SIZE - self.image.get_height()),
        )

    def update(self):
        self.rect.x += Constants.screen_scroll

class Diamond(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + Constants.TILE_SIZE // 2, y + (Constants.TILE_SIZE - self.image.get_height()))

    def update(self, player):
        self.rect.x += Constants.screen_scroll
        if pygame.sprite.collide_rect(self, player):
            player.points += 100
            self.kill()

# TODO Other elements?
