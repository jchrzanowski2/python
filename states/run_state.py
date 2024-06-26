from .game_state import GameState
from world import make_world
from constants import Constants, PlayerActions, Statistics, SoundEffect
import pygame

pygame.font.init()
font = pygame.font.Font(None, 36)


class RunState(GameState):
    def __init__(self) -> None:
        super().__init__()
        self.player, self.world, self.groups = make_world(1)
        self.map_no = 1
        self.start_time = pygame.time.get_ticks()

        self.player_actions = PlayerActions()
        self.finish = 120
        self.sound = SoundEffect()

    def draw(self, screen: pygame.Surface) -> None:
        def show_game_info():
            elapsed_time = pygame.time.get_ticks() - self.start_time
            elapsed_text = font.render(
                "Elapsed Time: {} h {} min {} s".format(
                    elapsed_time // 3600000,
                    elapsed_time // 60000 % 60,
                    elapsed_time // 1000 % 60,
                ),
                True,
                Constants.BLACK,
            )
            screen.blit(elapsed_text, (10, 10))

            points_text = font.render(
                "Points: {}".format(self.player.statistics.points),
                True,
                Constants.BLACK,
            )
            screen.blit(points_text, (600, 10))

            health = font.render(
                "Health: {}".format(self.player.health), True, Constants.BLACK
            )
            screen.blit(health, (10, 40))
            health = font.render(
                "Ammo: {}".format(self.player.ammo), True, Constants.BLACK
            )
            screen.blit(health, (10, 70))

        show_game_info()
        self.world.draw(screen, Constants.screen_scroll)
        self.world.groups.update_draw(screen, self.player, self.world)
        self.player.draw(screen)
        Constants.bullet_group.draw(screen)
        for enemy in Constants.enemy_group:
            enemy.draw(screen)

    def update(self) -> None:
        self.player.update()
        for enemy in Constants.enemy_group:
            enemy.ai(self.world.obstacle_list, self.player)
            killed = enemy.update()
            if killed:
                self.observer.notify(killed)

        def handle_player() -> None:
            if self.player.alive:
                if self.player_actions.shoot:
                    self.player.shoot()
                if self.player.in_air:
                    self.player.update_action(2)
                elif (
                    self.player_actions.moving_left or self.player_actions.moving_right
                ):
                    self.player.update_action(1)
                else:
                    self.player.update_action(0)
                Constants.screen_scroll = self.player.move(
                    self.player_actions.moving_left,
                    self.player_actions.moving_right,
                    self.world.obstacle_list,
                )
                Constants.bg_scroll += Constants.screen_scroll
            else:
                self.player_actions.moving_left = False
                self.player_actions.moving_right = False
                Constants.screen_scroll = self.player.move(
                    self.player_actions.moving_left,
                    self.player_actions.moving_right,
                    self.world.obstacle_list,
                )

        handle_player()
        if self.world.map_no > Constants.LEVEL_NUM:
            self.world.stop = True
        if self.world.map_no > self.map_no:
            _, self.world, self.groups = make_world(2)
            self.map_no += 1
        if self.world.stop:
            self.observer.alert(Constants.Actions.GAME_END)
        if self.player.rect.y >= 800:
            self.player.alive = False
        if not self.player.alive:
            if self.finish:
                self.finish -= 1
            else:
                self.observer.alert(Constants.Actions.GAME_END)
        Constants.bullet_group.update(self.player)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player_actions.moving_left = True
            if event.key == pygame.K_d:
                self.player_actions.moving_right = True
            if event.key == pygame.K_SPACE:
                self.player_actions.shoot = True
            if event.key == pygame.K_w and not self.player.in_air and self.player.alive:
                self.player.jump = True
                self.sound.jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                self.observer.alert(Constants.Actions.GAME_END)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.player_actions.moving_left = False
            if event.key == pygame.K_d:
                self.player_actions.moving_right = False
            if event.key == pygame.K_SPACE:
                self.player_actions.shoot = False
