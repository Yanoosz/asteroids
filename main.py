import sys

import pygame

from asteroidfield import AsteroidField
from asteroids import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from shots import Shot


def main():
    print(
        f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: 1280\nScreen height: 720"
    )
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Type checker suppression for pygame dynamic attributes - these are valid in pygame
    # pyright: ignore[reportAttributeAccessIssue]
    Asteroid.containers = (asteroids, updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    Shot.containers = (shots, updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    Asteroid.containers = (asteroids, updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    AsteroidField.containers = updatable  # pyright: ignore[reportAttributeAccessIssue]

    Player.containers = (updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for shot in shots:
            for asteroid in asteroids:
                if asteroid.collisions(shot):
                    asteroid.split()
                    shot.kill()

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collisions(player):
                print("Game over!")
                sys.exit()

        screen.fill((0, 0, 0))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
