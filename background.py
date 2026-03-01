import random
from typing import List

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)
        self.brightness = random.randint(150, 255)

    def update(self, dt: float):
        # Move stars downward to simulate movement
        self.y += self.speed * dt * 60
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface: pygame.Surface):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class StarfieldBackground:
    def __init__(self, num_stars: int = 200):
        self.stars: List[Star] = [Star() for _ in range(num_stars)]
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_surface.fill((0, 0, 0))  # Black space background

    def update(self, dt: float):
        for star in self.stars:
            star.update(dt)

    def draw(self, surface: pygame.Surface):
        # Draw the black background
        surface.blit(self.background_surface, (0, 0))

        # Draw all stars
        for star in self.stars:
            star.draw(surface)
