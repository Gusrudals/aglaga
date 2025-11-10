"""
Main Galaga Game Engine
"""
import pygame
import random
import math
from constants import *
from player import Player
from enemy import Enemy
from formation import Formation
from particles import Explosion, StarField
from bullet import EnemyBullet


class Game:
    """Main game class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GALAGA")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.running = True

        # Game state
        self.state = STATE_TITLE
        self.stage = 1
        self.high_score = 0

        # Game objects
        self.player = None
        self.formation = None
        self.enemies = []
        self.enemy_bullets = []
        self.capture_beams = []
        self.explosions = []
        self.starfield = StarField()

        # Stage management
        self.entry_sequence = []
        self.entry_timer = 0
        self.stage_clear_timer = 0

        # Attack management
        self.attack_timer = 0
        self.attack_cooldown = 120  # Frames between attacks

        # Formation sway
        self.formation_sway_angle = 0

    def start_new_game(self):
        """Start a new game"""
        self.stage = 1
        self.player = Player(SCREEN_WIDTH // 2, PLAYER_Y_POSITION)
        self.formation = Formation()
        self.start_stage(self.stage)
        self.state = STATE_STAGE_START

    def start_stage(self, stage_num):
        """Start a new stage"""
        self.stage = stage_num
        self.enemies = []
        self.enemy_bullets = []
        self.capture_beams = []
        self.explosions = []

        # Create entry sequence
        self.entry_sequence = self.formation.create_stage_enemies(stage_num)
        self.entry_timer = 0

        # Reset attack timer
        self.attack_timer = self.attack_cooldown

    def update(self):
        """Update game state"""
        if self.state == STATE_TITLE:
            self.update_title()
        elif self.state == STATE_STAGE_START:
            self.update_stage_start()
        elif self.state == STATE_PLAYING:
            self.update_playing()
        elif self.state == STATE_GAME_OVER:
            self.update_game_over()

    def update_title(self):
        """Update title screen"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.start_new_game()

    def update_stage_start(self):
        """Update stage start (enemy entry sequence)"""
        self.starfield.update()

        # Spawn enemies from entry sequence
        self.entry_timer += 1

        for entry in self.entry_sequence:
            if not entry['spawned'] and self.entry_timer >= entry['delay']:
                self.enemies.append(entry['enemy'])
                entry['spawned'] = True

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

        # Check if all enemies have entered formation
        all_in_formation = all(
            entry['spawned'] and entry['enemy'].in_formation
            for entry in self.entry_sequence
        )

        if all_in_formation:
            self.state = STATE_PLAYING

    def update_playing(self):
        """Update main gameplay"""
        keys = pygame.key.get_pressed()

        # Update starfield
        self.starfield.update()

        # Update player
        if self.player.active:
            self.player.update(keys)

        # Update formation sway
        self.formation_sway_angle += FORMATION_SWAY_SPEED
        sway_offset = math.sin(self.formation_sway_angle) * FORMATION_SWAY_AMOUNT
        self.formation.update_formation_sway(sway_offset)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()

            # Enemy shooting
            if enemy.in_formation and random.random() < 0.002:
                bullet = enemy.shoot()
                if bullet:
                    self.enemy_bullets.append(bullet)

            # Remove dead enemies
            if not enemy.active:
                self.enemies.remove(enemy)
                self.formation.remove_enemy(enemy)
                # Create explosion
                self.explosions.append(Explosion(enemy.x, enemy.y, enemy.color))

        # Trigger dive attacks
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.trigger_dive_attack()
            self.attack_cooldown = max(60, 120 - self.stage * 5)  # Faster attacks on higher stages
            self.attack_timer = self.attack_cooldown

        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if not bullet.active:
                self.enemy_bullets.remove(bullet)

        # Update capture beams
        for beam in self.capture_beams[:]:
            beam.update()
            if not beam.active:
                self.capture_beams.remove(beam)

        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.active:
                self.explosions.remove(explosion)

        # Collision detection
        self.check_collisions()

        # Check stage clear
        if self.formation.is_formation_empty():
            self.stage_clear_timer += 1
            if self.stage_clear_timer >= STAGE_CLEAR_DELAY // (1000 // FPS):
                self.stage += 1
                self.start_stage(self.stage)
                self.state = STATE_STAGE_START
                self.stage_clear_timer = 0

        # Check game over
        if not self.player.active and self.player.lives <= 0:
            self.state = STATE_GAME_OVER
            if self.player.score > self.high_score:
                self.high_score = self.player.score

    def update_game_over(self):
        """Update game over screen"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.start_new_game()

    def trigger_dive_attack(self):
        """Trigger enemy dive attack"""
        # Select 1-3 enemies to dive
        num_attackers = min(random.randint(1, 3), self.formation.get_enemies_in_formation())

        for _ in range(num_attackers):
            enemy = self.formation.get_random_enemy_for_dive()
            if enemy:
                enemy.start_dive_attack(self.player.x, self.player.y)

                # Boss enemies might deploy capture beam
                if enemy.enemy_type == ENEMY_BOSS and random.random() < 0.3:
                    beam = enemy.deploy_capture_beam()
                    if beam:
                        self.capture_beams.append(beam)

    def check_collisions(self):
        """Check for collisions"""
        if not self.player.active:
            return

        player_rect = self.player.get_rect()

        # Player bullets vs enemies
        for bullet in self.player.bullets[:]:
            bullet_rect = bullet.get_rect()

            for enemy in self.enemies[:]:
                if enemy.active and bullet_rect.colliderect(enemy.get_rect()):
                    # Hit enemy
                    if enemy.hit():
                        # Enemy destroyed
                        score = enemy.score_value
                        if enemy.state == 'diving':
                            score *= 2  # Bonus for hitting diving enemy

                        self.player.add_score(score)

                        # Check if boss had captured fighter
                        if enemy.enemy_type == ENEMY_BOSS and enemy.has_captured_fighter:
                            self.player.rescue_captured_ship()

                    bullet.active = False
                    break

        # Enemy bullets vs player
        for bullet in self.enemy_bullets[:]:
            if bullet.active and bullet.get_rect().colliderect(player_rect):
                self.player.hit()
                bullet.active = False
                self.explosions.append(Explosion(self.player.x, self.player.y, BLUE))

        # Enemies vs player (collision)
        for enemy in self.enemies[:]:
            if enemy.active and enemy.get_rect().colliderect(player_rect):
                self.player.hit()
                enemy.hit()
                self.explosions.append(Explosion(enemy.x, enemy.y, enemy.color))

        # Capture beams vs player
        for beam in self.capture_beams[:]:
            if beam.active and beam.get_rect().colliderect(player_rect):
                if not self.player.invulnerable and not self.player.is_captured:
                    # Player captured!
                    self.player.captured()
                    beam.captured_fighter = True

                    # Find the boss that shot the beam and give it the fighter
                    for enemy in self.enemies:
                        if enemy.enemy_type == ENEMY_BOSS and enemy.state == 'diving':
                            enemy.has_captured_fighter = True
                            break

                beam.active = False

    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)

        # Draw starfield
        self.starfield.draw(self.screen)

        if self.state == STATE_TITLE:
            self.draw_title()
        elif self.state == STATE_STAGE_START:
            self.draw_stage_start()
        elif self.state == STATE_PLAYING:
            self.draw_playing()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_title(self):
        """Draw title screen"""
        # Title
        title = self.large_font.render("GALAGA", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)

        # Instructions
        instructions = [
            "ARROW KEYS or A/D - Move",
            "SPACE or Z - Shoot",
            "",
            "Press SPACE to Start"
        ]

        y_offset = SCREEN_HEIGHT // 2
        for line in instructions:
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40

        # High score
        if self.high_score > 0:
            high_score_text = self.font.render(f"HIGH SCORE: {self.high_score}", True, YELLOW)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(high_score_text, high_score_rect)

    def draw_stage_start(self):
        """Draw stage start screen"""
        # Draw enemies entering
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw player
        if self.player:
            self.player.draw(self.screen)

        # Stage number
        stage_text = self.large_font.render(f"STAGE {self.stage}", True, CYAN)
        stage_rect = stage_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(stage_text, stage_rect)

        # Draw UI
        self.draw_ui()

    def draw_playing(self):
        """Draw main gameplay"""
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw player
        if self.player:
            self.player.draw(self.screen)

        # Draw enemy bullets
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)

        # Draw capture beams
        for beam in self.capture_beams:
            beam.draw(self.screen)

        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(self.screen)

        # Draw UI
        self.draw_ui()

    def draw_game_over(self):
        """Draw game over screen"""
        # Game Over text
        game_over = self.large_font.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over, game_over_rect)

        # Final score
        score_text = self.font.render(f"FINAL SCORE: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(score_text, score_rect)

        # Play again
        play_again = self.font.render("Press SPACE to Play Again", True, YELLOW)
        play_again_rect = play_again.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        self.screen.blit(play_again, play_again_rect)

    def draw_ui(self):
        """Draw UI elements"""
        # Score
        score_text = self.font.render(f"SCORE: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

        # High score
        high_score_text = self.font.render(f"HIGH: {self.high_score}", True, RED)
        self.screen.blit(high_score_text, (SCREEN_WIDTH - 250, 20))

        # Lives
        lives_text = self.font.render(f"LIVES: {self.player.lives}", True, CYAN)
        self.screen.blit(lives_text, (20, 60))

        # Stage
        stage_text = self.font.render(f"STAGE: {self.stage}", True, YELLOW)
        self.screen.blit(stage_text, (SCREEN_WIDTH - 250, 60))

    def run(self):
        """Main game loop"""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # Update
            self.update()

            # Draw
            self.draw()

            # Maintain frame rate
            self.clock.tick(FPS)

        pygame.quit()
