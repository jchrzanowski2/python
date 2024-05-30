from constants import Constants
from character import Character
import pygame
import csv
from typing import List
from world_objects import Decorations, Water, Exit, SpriteGroups, Diamond
from random import randint
import config as c

img_list = []

# Load images for tiles
for x in range(Constants.TILE_TYPES):
    img = pygame.image.load(f"img/tile/{x}.png")
    img = pygame.transform.scale(img, (Constants.TILE_SIZE, Constants.TILE_SIZE))
    img_list.append(img)


class World:
    """Class representing the game world."""

    def __init__(self, map_no: int) -> None:
        """
        Initialize the World object.

        Args:
            map_no (int): The number of the map to load.
        """
        self.obstacle_list: List[tuple[pygame.Surface, pygame.Rect]] = []
        self.groups = SpriteGroups()
        self.stop = False
        self.map_no = map_no

    def process_data(self, data: List[List[int]]) -> tuple[Character, SpriteGroups]:
        """
        Process map data to create game objects.

        Args:
            data (List[List[int]]): 2D list representing the map layout.

        Returns:
            tuple[Character, SpriteGroups]: A tuple containing the player Character object and SpriteGroups object.
        """
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img: pygame.Surface = img_list[tile]
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
                            c.PL_SPEED,
                            c.START_AMMO,
                            health=c.START_HP,
                            danger=0
                        )
                    elif tile == 16:  # enemy
                        enemy = Character(
                            "enemy",
                            x * Constants.TILE_SIZE,
                            y * Constants.TILE_SIZE,
                            2,
                            c.ENEMY_SPEED,
                            c.ENEMY_AMMO,
                            health=c.ENEMY_HP,
                            danger=randint(1, 10)
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
        """
        Draw the world on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
            screen_scroll (int): The amount to scroll the screen.
        """
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


def make_world(map_no: int) -> tuple[Character, World, SpriteGroups]:
    """
    Create a new game world.

    Args:
        map_no (int): The number of the map to load.

    Returns:
        tuple[Character, World, SpriteGroups]: A tuple containing the player Character object, World object, and SpriteGroups object.
    """
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
