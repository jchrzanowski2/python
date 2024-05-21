import pygame
from constants import Constants


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int) -> int:
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load("img/icons/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, player) -> None:
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
