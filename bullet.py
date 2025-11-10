"""
Bullet classes for Galaga
"""
import pygame
from constants import *


class Bullet:
    """Base bullet class"""
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 2 * SCALE
        self.height = 6 * SCALE
        self.active = True

    def update(self):
        """Update bullet position"""
        self.y -= self.speed

        # Deactivate if off screen
        if self.y < -self.height or self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        """Draw bullet"""
        if self.active:
            pygame.draw.rect(screen, self.color,
                           (self.x - self.width // 2, self.y, self.width, self.height))

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)


class PlayerBullet(Bullet):
    """Player bullet - travels upward"""
    def __init__(self, x, y):
        super().__init__(x, y, BULLET_SPEED, YELLOW)
        self.width = 3 * SCALE
        self.height = 8 * SCALE


class EnemyBullet(Bullet):
    """Enemy bullet - travels downward"""
    def __init__(self, x, y):
        super().__init__(x, y, -ENEMY_BULLET_SPEED, RED)
        self.width = 2 * SCALE
        self.height = 8 * SCALE

    def update(self):
        """Enemy bullets move downward"""
        self.y -= self.speed  # speed is negative, so this moves down

        if self.y < -self.height or self.y > SCREEN_HEIGHT:
            self.active = False


class CaptureBeam:
    """Capture beam shot by Boss Galaga"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = CAPTURE_BEAM_WIDTH
        self.height = CAPTURE_BEAM_LENGTH
        self.speed = CAPTURE_BEAM_SPEED
        self.active = True
        self.captured_fighter = None

    def update(self):
        """Update capture beam position"""
        self.y += self.speed

        if self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        """Draw capture beam with animated effect"""
        if self.active:
            # Draw pulsating beam
            colors = [CYAN, BLUE, CYAN]
            segment_height = self.height // len(colors)

            for i, color in enumerate(colors):
                pygame.draw.rect(screen, color,
                               (self.x - self.width // 2,
                                self.y + i * segment_height,
                                self.width, segment_height))

            # Draw outline
            pygame.draw.rect(screen, WHITE,
                           (self.x - self.width // 2, self.y, self.width, self.height), 1)

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
