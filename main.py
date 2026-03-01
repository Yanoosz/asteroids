import sys

import pygame

from asteroidfield import AsteroidField
from asteroids import Asteroid
from background import StarfieldBackground
from constants import ASTEROID_MIN_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from particles import ParticleManager
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
    Asteroid.containers = (asteroids, updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    Shot.containers = (shots, updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    Asteroid.containers = (asteroids, updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    AsteroidField.containers = updatable  # pyright: ignore[reportAttributeAccessIssue]

    Player.containers = (updatable, drawable)  # pyright: ignore[reportAttributeAccessIssue]
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Create the asteroid field (added to updatable group, updated automatically)
    _asteroid_field = AsteroidField()  # pyright: ignore[reportUnusedVariable]

    # Create an initial asteroid to ensure there's something to interact with
    initial_asteroid = Asteroid(
        SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 2 + 200, ASTEROID_MIN_RADIUS * 3
    )
    initial_asteroid.velocity = pygame.Vector2(50, 20)

    # Create the starfield background
    background = StarfieldBackground()

    # Create particle manager for effects
    particle_manager = ParticleManager()

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for shot in shots:
            for asteroid in asteroids:
                if asteroid.collisions(shot):
                    # Add explosion effect at asteroid position
                    particle_manager.add_explosion(
                        asteroid.position.x, asteroid.position.y, (255, 255, 0)
                    )
                    # Get the new asteroids from split (if any)
                    new_asteroids = asteroid.split()
                    # Add explosion effects for the new asteroids if any were created
                    for new_asteroid in new_asteroids:
                        particle_manager.add_explosion(
                            new_asteroid.position.x,
                            new_asteroid.position.y,
                            (255, 200, 0),
                        )
                    shot.kill()

        for obj in updatable:
            obj.update(dt)

        # Update background
        background.update(dt)

        # Update particle effects
        particle_manager.update(dt)

        for asteroid in asteroids:
            if asteroid.collisions(player):
                print("Game over!")
                sys.exit()

        # Draw the starfield background instead of filling with black
        background.draw(screen)

        # Draw particle effects
        particle_manager.draw(screen)

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
