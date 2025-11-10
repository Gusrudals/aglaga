"""
Enemy classes for Galaga
"""
import pygame
import math
import random
from constants import *
from bullet import EnemyBullet, CaptureBeam


class Enemy:
    """Base enemy class"""
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.active = True
        self.in_formation = False
        self.formation_x = x
        self.formation_y = y
        self.state = 'entering'  # entering, formation, diving, returning
        self.path = []
        self.path_index = 0
        self.animation_frame = 0
        self.shoot_timer = random.randint(60, 300)

        # Enemy type specific properties
        if enemy_type == ENEMY_BEE:
            self.color = YELLOW
            self.score_value = SCORE_BEE
            self.max_health = 1
        elif enemy_type == ENEMY_BUTTERFLY:
            self.color = RED
            self.score_value = SCORE_BUTTERFLY
            self.max_health = 1
        elif enemy_type == ENEMY_BOSS:
            self.color = BLUE
            self.score_value = SCORE_BOSS
            self.max_health = 2
            self.has_captured_fighter = False

        self.health = self.max_health

    def update(self):
        """Update enemy state"""
        self.animation_frame = (self.animation_frame + 1) % 60

        if self.state == 'entering':
            self.follow_path()
        elif self.state == 'formation':
            self.update_formation()
        elif self.state == 'diving':
            self.follow_path()
        elif self.state == 'returning':
            self.follow_path()

        # Shooting
        if self.in_formation:
            self.shoot_timer -= 1

    def follow_path(self):
        """Follow a predefined path"""
        if self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]

            # Move towards target
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < DIVE_SPEED:
                self.x = target_x
                self.y = target_y
                self.path_index += 1
            else:
                self.x += (dx / distance) * DIVE_SPEED
                self.y += (dy / distance) * DIVE_SPEED
        else:
            # Path completed
            if self.state == 'entering':
                self.state = 'formation'
                self.in_formation = True
            elif self.state == 'diving':
                # Check if enemy flew off screen
                if self.y > SCREEN_HEIGHT or self.x < 0 or self.x > SCREEN_WIDTH:
                    # Create return path
                    self.create_return_path()
                    self.state = 'returning'
            elif self.state == 'returning':
                self.state = 'formation'
                self.in_formation = True
                self.x = self.formation_x
                self.y = self.formation_y

    def update_formation(self):
        """Update position while in formation (swaying motion)"""
        # Simple sway animation
        sway_offset = math.sin(self.animation_frame * FORMATION_SWAY_SPEED) * FORMATION_SWAY_AMOUNT
        self.x = self.formation_x + sway_offset

    def start_dive_attack(self, player_x, player_y):
        """Begin a diving attack"""
        if self.state != 'formation':
            return

        self.state = 'diving'
        self.in_formation = False
        self.path = []
        self.path_index = 0

        # Create dive path based on enemy type
        if self.enemy_type == ENEMY_BEE:
            self.create_bee_dive_path(player_x, player_y)
        elif self.enemy_type == ENEMY_BUTTERFLY:
            self.create_butterfly_dive_path(player_x, player_y)
        elif self.enemy_type == ENEMY_BOSS:
            self.create_boss_dive_path(player_x, player_y)

    def create_bee_dive_path(self, player_x, player_y):
        """Create simple dive path for bee"""
        # Simple swooping dive
        steps = 30
        for i in range(steps):
            t = i / steps
            # Bezier curve for smooth dive
            x = self.x + (player_x - self.x) * t
            y = self.y + (player_y - self.y) * t + math.sin(t * math.pi) * 100
            self.path.append((x, y))

        # Continue off screen
        self.path.append((player_x, SCREEN_HEIGHT + 50))

    def create_butterfly_dive_path(self, player_x, player_y):
        """Create looping dive path for butterfly"""
        # Loop-de-loop dive
        steps = 40
        for i in range(steps):
            t = i / steps
            angle = t * math.pi * 2
            x = self.x + math.sin(angle) * 150 + (player_x - self.x) * t
            y = self.y + i * 10
            self.path.append((x, y))

        # Continue off screen
        self.path.append((player_x, SCREEN_HEIGHT + 50))

    def create_boss_dive_path(self, player_x, player_y):
        """Create boss dive path (can deploy capture beam)"""
        # Slower, more deliberate dive
        steps = 35
        for i in range(steps):
            t = i / steps
            x = self.x + (player_x - self.x) * t * 1.2
            y = self.y + i * 8
            self.path.append((x, y))

        # Continue off screen
        self.path.append((player_x, SCREEN_HEIGHT + 50))

    def create_return_path(self):
        """Create path to return to formation"""
        self.path = []
        self.path_index = 0

        # Create arc back to formation position
        steps = 30
        for i in range(steps):
            t = i / steps
            x = self.x + (self.formation_x - self.x) * t
            y = self.y + (self.formation_y - self.y) * t - math.sin(t * math.pi) * 100
            self.path.append((x, y))

    def shoot(self):
        """Fire a bullet"""
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(120, 300)
            return EnemyBullet(self.x, self.y + self.height // 2)
        return None

    def deploy_capture_beam(self):
        """Boss deploys capture beam"""
        if self.enemy_type == ENEMY_BOSS and self.state == 'diving':
            return CaptureBeam(self.x, self.y + self.height // 2)
        return None

    def draw(self, screen):
        """Draw enemy"""
        if not self.active:
            return

        # Animation (flapping wings effect)
        frame = (self.animation_frame // 10) % 2

        if self.enemy_type == ENEMY_BEE:
            self.draw_bee(screen, frame)
        elif self.enemy_type == ENEMY_BUTTERFLY:
            self.draw_butterfly(screen, frame)
        elif self.enemy_type == ENEMY_BOSS:
            self.draw_boss(screen, frame)

    def draw_bee(self, screen, frame):
        """Draw bee enemy"""
        # Body
        pygame.draw.ellipse(screen, YELLOW,
                          (self.x - self.width // 2, self.y - self.height // 2,
                           self.width, self.height))

        # Stripes
        stripe_width = 2
        for i in range(3):
            y_offset = -self.height // 2 + i * (self.height // 3)
            pygame.draw.line(screen, BLACK,
                           (self.x - self.width // 2, self.y + y_offset),
                           (self.x + self.width // 2, self.y + y_offset),
                           stripe_width)

        # Wings (animated)
        wing_offset = 5 if frame == 0 else 2
        # Left wing
        pygame.draw.ellipse(screen, WHITE,
                          (self.x - self.width // 2 - wing_offset,
                           self.y - self.height // 2,
                           self.width // 2, self.height // 2))
        # Right wing
        pygame.draw.ellipse(screen, WHITE,
                          (self.x + wing_offset,
                           self.y - self.height // 2,
                           self.width // 2, self.height // 2))

    def draw_butterfly(self, screen, frame):
        """Draw butterfly enemy"""
        # Body
        pygame.draw.ellipse(screen, RED,
                          (self.x - self.width // 4, self.y - self.height // 2,
                           self.width // 2, self.height))

        # Wings (animated)
        wing_offset = 8 if frame == 0 else 4
        # Left wing
        points_left = [
            (self.x, self.y),
            (self.x - self.width // 2 - wing_offset, self.y - self.height // 3),
            (self.x - self.width // 2 - wing_offset, self.y + self.height // 3),
        ]
        pygame.draw.polygon(screen, BLUE, points_left)

        # Right wing
        points_right = [
            (self.x, self.y),
            (self.x + self.width // 2 + wing_offset, self.y - self.height // 3),
            (self.x + self.width // 2 + wing_offset, self.y + self.height // 3),
        ]
        pygame.draw.polygon(screen, BLUE, points_right)

        # Wing patterns
        pygame.draw.circle(screen, YELLOW,
                          (self.x - self.width // 3 - wing_offset // 2, self.y),
                          3 * SCALE)
        pygame.draw.circle(screen, YELLOW,
                          (self.x + self.width // 3 + wing_offset // 2, self.y),
                          3 * SCALE)

    def draw_boss(self, screen, frame):
        """Draw boss Galaga enemy"""
        # Main body (larger than other enemies)
        body_width = self.width * 1.3
        body_height = self.height * 1.3

        # Body
        pygame.draw.ellipse(screen, BLUE,
                          (self.x - body_width // 2, self.y - body_height // 2,
                           body_width, body_height))

        # Eyes
        eye_offset = body_width // 4
        pygame.draw.circle(screen, RED,
                          (int(self.x - eye_offset), int(self.y - body_height // 4)),
                          3 * SCALE)
        pygame.draw.circle(screen, RED,
                          (int(self.x + eye_offset), int(self.y - body_height // 4)),
                          3 * SCALE)

        # Antennae
        pygame.draw.line(screen, YELLOW,
                        (self.x - body_width // 3, self.y - body_height // 2),
                        (self.x - body_width // 2, self.y - body_height),
                        2)
        pygame.draw.line(screen, YELLOW,
                        (self.x + body_width // 3, self.y - body_height // 2),
                        (self.x + body_width // 2, self.y - body_height),
                        2)

        # Wings (animated)
        wing_offset = 6 if frame == 0 else 3
        # Left wing
        pygame.draw.polygon(screen, CYAN,
                          [(self.x - body_width // 4, self.y),
                           (self.x - body_width // 2 - wing_offset, self.y - body_height // 4),
                           (self.x - body_width // 2 - wing_offset, self.y + body_height // 4)])

        # Right wing
        pygame.draw.polygon(screen, CYAN,
                          [(self.x + body_width // 4, self.y),
                           (self.x + body_width // 2 + wing_offset, self.y - body_height // 4),
                           (self.x + body_width // 2 + wing_offset, self.y + body_height // 4)])

        # If has captured fighter, draw it
        if self.has_captured_fighter:
            fighter_y = self.y + body_height // 2 + 10
            pygame.draw.polygon(screen, WHITE,
                              [(self.x, fighter_y - 5),
                               (self.x - 5, fighter_y + 5),
                               (self.x + 5, fighter_y + 5)])

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)

    def hit(self, damage=1):
        """Enemy takes damage"""
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False
