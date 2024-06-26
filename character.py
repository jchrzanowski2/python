import pygame
import os
import random
from constants import Constants, Statistics, SoundEffect
from bullet import Bullet
from typing import List
import config as c

pygame.font.init()
font = pygame.font.SysFont(None, 20)


class Character(pygame.sprite.Sprite):
    """Class representing a character in the game."""

    def __init__(
        self,
        char_type: str,
        x: int,
        y: int,
        scale: float,
        speed: float,
        ammo: int,
        health: int = 100,
        danger: int = 0,
    ) -> None:
        """
        Initialize a Character object.

        Args:
            char_type (str): The type of character.
            x (int): The x-coordinate of the character.
            y (int): The y-coordinate of the character.
            scale (float): The scale factor for the character's images.
            speed (float): The speed of the character.
            ammo (int): The initial ammo count of the character.
            health (int, optional): The initial health of the character. Defaults to 100.
            danger (int): Enemy difficulty specifier.
        """
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.shoot_cooldown = 0
        self.health = health
        self.max_health = self.health
        self.ammo = ammo
        self.starat_ammo = ammo
        self.update_time = pygame.time.get_ticks()
        animamation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in animamation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f"img/{self.char_type}/{animation}/{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.danger = 0 if danger in range(0, 7) else 1 if danger in range(7, 10) else 2
        self.image: pygame.Surface = self.animation_list[self.action][self.frame_index]
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
        self.sound = SoundEffect()
        self.hit_cntdown = 20
        # ai specific variables
        if self.char_type == "enemy":
            self.residual_ammo = random.randint(3, 8)
            if self.danger > 0:
                self.skull_img = pygame.image.load(
                    f"img/skull/{self.danger}.png"
                ).convert_alpha()
                self.skull_img = pygame.transform.scale(
                    self.skull_img,
                    (
                        int(self.skull_img.get_width() * 0.3),
                        int(self.skull_img.get_height() * 0.3),
                    ),
                )
                self.health += 60 * self.danger
                self.residual_ammo += 4 * self.danger
                self.speed += 0.3 * self.danger
                self.ammo += 30 * self.danger
            self.move_counter = 0
            self.vision = pygame.Rect(0, 0, 150, 20)
            self.idling = False
            self.idling_counter = 0
        else:
            self.statistics = Statistics()

    def update(self) -> int | None:
        """
        Update the character's state.

        Returns:
            bool: True if the character is killed, None otherwise.
        """
        if self.rect.x > Constants.SCREEN_WIDTH + 200 or self.rect.x < -200:
            return
        self.update_animation()
        alive = self.check_alive()
        if alive:
            return alive

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(
        self, moving_left, moving_right, obstacle_list: List[pygame.Surface]
    ) -> None:
        """
        Move the character.

        Args:
            moving_left (bool): Indicates if the character is moving left.
            moving_right (bool): Indicates if the character is moving right.
            obstacle_list (list): List of obstacles to consider for collision detection.
        """
        if self.char_type == "enemy":
            if self.rect.x > Constants.SCREEN_WIDTH + 200 or self.rect.x < -200:
                return
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
            self.vel_y = -c.JUMP
            self.jump = False
            self.in_air = True

        self.vel_y += Constants.GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
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

        if self.char_type == "player":
            for enemy in Constants.enemy_group:
                if enemy.rect.x > Constants.SCREEN_WIDTH + 200 or enemy.rect.x < -200:
                    continue
                if enemy.rect.colliderect(
                    self.rect.x, self.rect.y, self.width, self.height
                ):
                    if not enemy.alive:
                        if enemy.residual_ammo > 0:
                            self.ammo += enemy.residual_ammo
                            enemy.residual_ammo = 0
                    elif enemy.alive and self.alive:
                        self.health -= 10 if self.hit_cntdown == 10 else 0
                        self.hit_cntdown -= 1
                        if self.hit_cntdown == 0:
                            self.hit_cntdown = 20

        self.rect.x += dx
        self.rect.y += dy
        if self.char_type == "player":
            self.statistics.distance_travelled += (dx**2 + dy**2) ** (1 / 2)

        # update scroll
        if self.char_type == "player":
            if (
                self.rect.right > Constants.SCREEN_WIDTH - Constants.SCROLL_THRESH
                or self.rect.left < Constants.SCROLL_THRESH
            ):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll

    def shoot(self) -> None:
        """Make the character shoot."""
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = (
                20 if self.danger == 0 else 14 if self.danger == 1 else 10
            )
            bullet = Bullet(
                self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),
                self.rect.centery,
                self.direction,
            )
            Constants.bullet_group.add(bullet)
            self.sound.shot_fx.play()

            self.ammo -= 1
            if self.char_type == "player":
                self.statistics.bullets_shot += 1

    def update_animation(self) -> None:
        """Update the character's animation."""
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action: int) -> None:
        """
        Update the character's action.

        Args:
            new_action (int): The new action to be performed by the character.
        """
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def ai(self, obstacle_list: List[int], player) -> None:
        """
        Implement the AI behavior for the character.

        Args:
            obstacle_list (List[int]): List of obstacles to consider for collision detection.
            player: The player character to interact with.
        """
        if self.rect.x > Constants.SCREEN_WIDTH + 200 or self.rect.x < -200:
            pass
        elif self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            # if ai sees player
            if self.vision.colliderect(player.rect):
                self.update_action(0)  # idle
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False

                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, obstacle_list)
                    self.update_action(1)  # run
                    self.move_counter += 1

                    # ai vision
                    self.vision.center = (
                        self.rect.centerx + 75 * self.direction,
                        self.rect.centery,
                    )

                    if self.move_counter > Constants.TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False

        self.rect.x += Constants.screen_scroll

    def check_alive(self) -> int:
        """
        Check if the character is alive.

        Returns:
            int: The kill constant if the character is dead, 0 otherwise.
        """
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.update_action(3)
            if self.alive:
                self.alive = False
                return Constants.KILL + self.danger
            return 0
        return 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the character on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the character on.
        """
        if self.char_type == "enemy":
            if self.rect.x > Constants.SCREEN_WIDTH + 200 or self.rect.x < -200:
                return
            if self.danger:
                skullrect = self.rect.move(25, -35)
                screen.blit(
                    pygame.transform.flip(self.skull_img, not self.flip, False),
                    skullrect,
                )

        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
