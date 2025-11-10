"""
Player class for Galaga
"""
import pygame
from constants import *
from bullet import PlayerBullet


class Player:
    """Player fighter ship"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_START_LIVES
        self.score = 0
        self.active = True
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.bullets = []
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.is_captured = False
        self.dual_fighter = False  # Dual fighter mode after rescue

    def update(self, keys):
        """Update player state"""
        # Handle invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        # Keep player on screen
        self.x = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, self.x))

        # Shooting
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            if self.shoot_cooldown == 0:
                self.can_shoot = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and self.can_shoot:
            self.shoot()

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)

    def shoot(self):
        """Fire bullet(s)"""
        if self.dual_fighter:
            # Dual fighter shoots two bullets
            self.bullets.append(PlayerBullet(self.x - 10, self.y - self.height // 2))
            self.bullets.append(PlayerBullet(self.x + 10, self.y - self.height // 2))
        else:
            # Single fighter shoots one bullet
            self.bullets.append(PlayerBullet(self.x, self.y - self.height // 2))

        self.can_shoot = False
        self.shoot_cooldown = 15  # Cooldown frames

    def draw(self, screen):
        """Draw player ship"""
        if not self.active:
            return

        # Blinking effect when invulnerable
        if self.invulnerable and (self.invulnerable_timer // 5) % 2 == 0:
            return

        # Draw player ship (simplified geometric shape like original)
        # Main body
        points = [
            (self.x, self.y - self.height // 2),  # Top point
            (self.x - self.width // 3, self.y),  # Left middle
            (self.x - self.width // 2, self.y + self.height // 2),  # Left bottom
            (self.x + self.width // 2, self.y + self.height // 2),  # Right bottom
            (self.x + self.width // 3, self.y),  # Right middle
        ]
        pygame.draw.polygon(screen, BLUE, points)
        pygame.draw.polygon(screen, CYAN, points, 2)  # Outline

        # Cockpit
        pygame.draw.circle(screen, RED, (self.x, self.y), 3 * SCALE)

        # Draw dual fighter if active
        if self.dual_fighter:
            # Draw second fighter next to first
            offset_x = 15
            points2 = [
                (self.x + offset_x, self.y - self.height // 2),
                (self.x + offset_x - self.width // 3, self.y),
                (self.x + offset_x - self.width // 2, self.y + self.height // 2),
                (self.x + offset_x + self.width // 2, self.y + self.height // 2),
                (self.x + offset_x + self.width // 3, self.y),
            ]
            pygame.draw.polygon(screen, YELLOW, points2)
            pygame.draw.polygon(screen, WHITE, points2, 2)
            pygame.draw.circle(screen, RED, (self.x + offset_x, self.y), 3 * SCALE)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)

    def hit(self):
        """Player got hit"""
        if not self.invulnerable and not self.is_captured:
            if self.dual_fighter:
                # Lose dual fighter mode but don't lose a life
                self.dual_fighter = False
                self.make_invulnerable()
            else:
                self.lives -= 1
                if self.lives > 0:
                    self.reset_position()
                    self.make_invulnerable()
                else:
                    self.active = False

    def make_invulnerable(self, frames=180):
        """Make player invulnerable for a duration"""
        self.invulnerable = True
        self.invulnerable_timer = frames

    def reset_position(self):
        """Reset player to starting position"""
        self.x = SCREEN_WIDTH // 2
        self.y = PLAYER_Y_POSITION

    def captured(self):
        """Player ship got captured by tractor beam"""
        self.is_captured = True
        self.active = False

    def rescue_captured_ship(self):
        """Rescue captured ship and activate dual fighter"""
        self.dual_fighter = True
        self.score += SCORE_DUAL_FIGHTER_BONUS

    def add_score(self, points):
        """Add points to score"""
        self.score += points
