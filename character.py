import pygame
import os
from constants import Constants


class Character(pygame.sprite.Sprite):
    def __init__(
        self, char_type: str, x: int, y: int, scale: float, speed: float
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        animamation_types = ["Idle", "Run", "Jump"]
        for animation in animamation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png")
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.vel_y = 0
        self.in_air = True
        self.flip = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # ai specific variables
        self.move_counter = 0

    def move(self, moving_left: bool, moving_right: bool, obstacle_list: list) -> None:
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

        self.vel_y += Constants.GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in obstacle_list:
            if tile[1].colliderect(
                self.rect.x + dx, self.rect.y, self.width, self.height
            ):
                dx = 0
                # if the ai has hit a wall then make it turn around
                if self.char_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(
                self.rect.x, self.rect.y + dy, self.width, self.height
            ):
                # if below the ground
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # if above the ground
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom - 1

        self.rect.x += dx
        self.rect.y += dy

        # update scroll
        if self.char_type == "player":
            if (
                self.rect.right > Constants.SCREEN_WIDTH - Constants.SCROLL_THRESH
                or self.rect.left < Constants.SCROLL_THRESH
            ):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def ai(self, obstacle_list):
        if self.alive:
            self.update_action(1)
            if self.direction == 1:
                ai_moving_right = True
            else:
                ai_moving_right = False
            ai_moving_left = not ai_moving_right
            self.move(ai_moving_left, ai_moving_right, obstacle_list)
        self.rect.x += Constants.screen_scroll

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
