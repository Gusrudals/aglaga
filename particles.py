"""
Particle effects for Galaga
"""
import pygame
import random
import math
from constants import *


class Particle:
    """Single particle"""
    def __init__(self, x, y, color, velocity_x, velocity_y, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity_x
        self.vy = velocity_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 4)
        self.active = True

    def update(self):
        """Update particle"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.active = False

    def draw(self, screen):
        """Draw particle"""
        if self.active:
            # Fade out based on lifetime
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (
                min(255, self.color[0]),
                min(255, self.color[1]),
                min(255, self.color[2])
            )

            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)


class Explosion:
    """Explosion effect"""
    def __init__(self, x, y, color=YELLOW, num_particles=20):
        self.x = x
        self.y = y
        self.particles = []
        self.active = True

        # Create particles
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.randint(20, 40)

            particle = Particle(x, y, color, vx, vy, lifetime)
            self.particles.append(particle)

    def update(self):
        """Update explosion"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.active:
                self.particles.remove(particle)

        if not self.particles:
            self.active = False

    def draw(self, screen):
        """Draw explosion"""
        for particle in self.particles:
            particle.draw(screen)


class StarField:
    """Scrolling star field background"""
    def __init__(self):
        self.stars = []
        # Create stars
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            speed = random.uniform(0.5, 2)
            brightness = random.randint(100, 255)
            self.stars.append({
                'x': x,
                'y': y,
                'speed': speed,
                'brightness': brightness
            })

    def update(self):
        """Update star positions"""
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        """Draw stars"""
        for star in self.stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), 1)
