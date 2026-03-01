import random
from typing import List, Tuple

import pygame


class Particle:
    def __init__(
        self,
        x: float,
        y: float,
        velocity: pygame.Vector2,
        lifetime: float,
        color: Tuple[int, int, int],
    ):
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = random.randint(2, 5)

    def update(self, dt: float) -> bool:
        """Update particle and return True if still alive"""
        self.position += self.velocity * dt
        self.lifetime -= dt

        # Apply gravity-like effect
        self.velocity.y += 20 * dt

        return self.lifetime > 0

    def draw(self, screen: pygame.Surface):
        # Fade out as lifetime decreases by reducing color intensity
        faded_color = (
            max(0, int(self.color[0] * (self.lifetime / self.max_lifetime))),
            max(0, int(self.color[1] * (self.lifetime / self.max_lifetime))),
            max(0, int(self.color[2] * (self.lifetime / self.max_lifetime))),
        )

        # Simple circle particle with fading effect
        pygame.draw.circle(
            screen, faded_color, (int(self.position.x), int(self.position.y)), self.size
        )


class ExplosionEffect:
    def __init__(
        self, x: float, y: float, color: Tuple[int, int, int] = (255, 255, 255)
    ):
        self.particles: List[Particle] = []
        self.create_explosion(x, y, color)

    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int]):
        """Create particles for explosion effect"""
        particle_count = random.randint(8, 15)
        for _ in range(particle_count):
            # Random velocity direction
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 200)
            velocity = pygame.Vector2(0, -1).rotate(angle) * speed

            # Random lifetime
            lifetime = random.uniform(0.5, 1.5)

            # Slightly vary the color
            r = max(0, min(255, color[0] + random.randint(-30, 30)))
            g = max(0, min(255, color[1] + random.randint(-30, 30)))
            b = max(0, min(255, color[2] + random.randint(-30, 30)))
            varied_color = (r, g, b)

            particle = Particle(x, y, velocity, lifetime, varied_color)
            self.particles.append(particle)

    def update(self, dt: float) -> bool:
        """Update all particles and return True if still active"""
        # Update particles and remove dead ones
        self.particles = [p for p in self.particles if p.update(dt)]
        return len(self.particles) > 0

    def draw(self, screen: pygame.Surface):
        for particle in self.particles:
            particle.draw(screen)


class ParticleManager:
    def __init__(self):
        self.effects: List[ExplosionEffect] = []

    def add_explosion(
        self, x: float, y: float, color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """Add a new explosion effect"""
        explosion = ExplosionEffect(x, y, color)
        self.effects.append(explosion)

    def update(self, dt: float):
        """Update all effects and remove finished ones"""
        self.effects = [effect for effect in self.effects if effect.update(dt)]

    def draw(self, screen: pygame.Surface):
        """Draw all effects"""
        for effect in self.effects:
            effect.draw(screen)
