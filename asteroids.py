import random
from typing import List

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self) -> List["Asteroid"]:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return []  # No new asteroids created

        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # Type checker needs help understanding that self.position is a Vector2
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)  # pyright: ignore[reportAttributeAccessIssue]
        asteroid1.velocity = a * 1.2
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)  # pyright: ignore[reportAttributeAccessIssue]
        asteroid2.velocity = b * 1.2

        # Return the new asteroids so they can be used for effects
        return [asteroid1, asteroid2]
