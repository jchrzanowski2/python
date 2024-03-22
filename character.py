import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, char_type : str, x : int, y : int, scale : float, speed : float) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        img = pygame.image.load(f'img/{self.char_type}/character2.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = speed
        self.direction = 1
        self.flip = False

    def move(self, moving_left : bool, moving_right : bool) -> None:
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen : pygame.Surface) -> None:
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)