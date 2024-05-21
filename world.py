from constants import Constants
from character import Character
import pygame
import csv
from world_objects import Decorations, Water, Exit, SpriteGroups, Diamond

img_list = []

for x in range(Constants.TILE_TYPES):
    img = pygame.image.load(f"img/tile/{x}.png")
    img = pygame.transform.scale(img, (Constants.TILE_SIZE, Constants.TILE_SIZE))
    img_list.append(img)


class World:
    def __init__(self, map_no: int) -> None:
        self.obstacle_list = []
        self.groups = SpriteGroups()
        self.stop = False
        self.map_no = map_no

    def process_data(self, data: tuple[tuple[int]]) -> tuple[Character, SpriteGroups]:
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * Constants.TILE_SIZE
                    img_rect.y = y * Constants.TILE_SIZE
                    tile_data = (img, img_rect)

                    if tile <= 8:
                        self.obstacle_list.append(tile_data)

                    elif tile >= 9 and tile <= 10:
                        water = Water(
                            img, x * Constants.TILE_SIZE, y * Constants.TILE_SIZE
                        )
                        self.groups.water_group.add(water)

                    elif tile >= 11 and tile <= 14:
                        decoration = Decorations(
                            img, x * Constants.TILE_SIZE, y * Constants.TILE_SIZE
                        )
                        self.groups.decoration_group.add(decoration)

                    elif tile == 15:  # player
                        player = Character(
                            "player",
                            x * Constants.TILE_SIZE,
                            y * Constants.TILE_SIZE,
                            2,
                            5,
                            20,
                            health=200,
                        )
                    elif tile == 16:  # enemy
                        enemy = Character(
                            "enemy",
                            x * Constants.TILE_SIZE,
                            y * Constants.TILE_SIZE,
                            2,
                            2,
                            20,
                        )
                        Constants.enemy_group.add(enemy)
                    elif tile == 20:
                        exit = Exit(
                            img, x * Constants.TILE_SIZE, y * Constants.TILE_SIZE
                        )
                        self.groups.exit_group.add(exit)
                    elif tile == 21:
                        diamond = Diamond(
                            img, x * Constants.TILE_SIZE, y * Constants.TILE_SIZE
                        )
                        self.groups.diamond_group.add(diamond)

        return player, self.groups

    def draw(self, screen: pygame.Surface, screen_scroll: int) -> None:
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


def make_world(map_no: int) -> tuple[Character, World, SpriteGroups]:
    world_data = []
    for row in range(Constants.ROWS):
        r = [-1] * Constants.COLS
        world_data.append(r)

    with open(f"level{map_no}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    world = World(map_no)
    player, groups = world.process_data(world_data)

    return player, world, groups
