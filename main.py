import sys
import pygame
from constants import *
from player import Player
from circleshape import CircleShape
from asteroids import Asteroid
from asteroidfield import AsteroidField
from shots import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
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
