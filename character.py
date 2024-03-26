import pygame
from constants import Constants


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
        self.jump = False
        self.vel_y = 0
        self.in_air = True
        self.flip = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left : bool, moving_right : bool, obstacle_list: list) -> None:
        screen_scroll = 0
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

        if self.jump and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        # gravity
        self.vel_y += Constants.GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collistion
        for tile in obstacle_list:
            if pygame.Rect(tile[1]).colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if pygame.Rect(tile[1]).colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # if below the ground
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # if above the ground
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

        #update scroll
        if self.char_type == 'player':
            if self.rect.right > Constants.SCREEN_WIDTH - Constants.SCROLL_THRESH or self.rect.left < Constants.SCROLL_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll

    def draw(self, screen : pygame.Surface) -> None:
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)