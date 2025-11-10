"""
Formation system for Galaga
Manages enemy formation and entry patterns
"""
import pygame
import math
from constants import *
from enemy import Enemy


class Formation:
    """Manages enemy formation"""
    def __init__(self):
        self.enemies = []
        self.formation_positions = []
        self.setup_formation_grid()

    def setup_formation_grid(self):
        """Setup the classic Galaga formation grid"""
        # Classic Galaga formation:
        # Row 1-2: Boss Galaga (4 each row)
        # Row 3-4: Butterfly (8 each row)
        # Row 5-6: Bee (10 each row)

        self.formation_positions = []

        # Boss Galaga - Top 2 rows (4 per row)
        for row in range(2):
            for col in range(4):
                x = FORMATION_START_X + col * FORMATION_SPACING_X * 1.8
                y = FORMATION_TOP_Y + row * FORMATION_SPACING_Y
                self.formation_positions.append({
                    'x': x,
                    'y': y,
                    'type': ENEMY_BOSS,
                    'occupied': False,
                    'enemy': None
                })

        # Butterfly - Middle 2 rows (8 per row)
        for row in range(2, 4):
            for col in range(8):
                x = FORMATION_START_X - 60 + col * FORMATION_SPACING_X * 1.1
                y = FORMATION_TOP_Y + row * FORMATION_SPACING_Y
                self.formation_positions.append({
                    'x': x,
                    'y': y,
                    'type': ENEMY_BUTTERFLY,
                    'occupied': False,
                    'enemy': None
                })

        # Bee - Bottom 2 rows (10 per row)
        for row in range(4, 6):
            for col in range(10):
                x = FORMATION_START_X - 100 + col * FORMATION_SPACING_X
                y = FORMATION_TOP_Y + row * FORMATION_SPACING_Y
                self.formation_positions.append({
                    'x': x,
                    'y': y,
                    'type': ENEMY_BEE,
                    'occupied': False,
                    'enemy': None
                })

    def create_stage_enemies(self, stage_number):
        """Create enemies for a stage with entry animation"""
        self.enemies = []

        # Create entry sequence
        entry_sequence = []
        entry_delay = 0

        # Enemies enter in groups
        for i, pos in enumerate(self.formation_positions):
            enemy = Enemy(SCREEN_WIDTH // 2, -50, pos['type'])
            enemy.formation_x = pos['x']
            enemy.formation_y = pos['y']

            # Create entry path
            enemy.path = self.create_entry_path(
                enemy.x, enemy.y,
                pos['x'], pos['y'],
                i % 4  # Entry pattern variation
            )
            enemy.path_index = 0
            enemy.state = 'entering'

            entry_sequence.append({
                'enemy': enemy,
                'delay': entry_delay,
                'spawned': False
            })

            # Stagger entry timing
            if i % 4 == 3:
                entry_delay += 30  # Delay between groups

            pos['occupied'] = True
            pos['enemy'] = enemy

        return entry_sequence

    def create_entry_path(self, start_x, start_y, end_x, end_y, pattern):
        """Create entry path for enemy"""
        path = []

        # Different entry patterns based on position
        steps = 40

        if pattern == 0:
            # Loop from left
            for i in range(steps):
                t = i / steps
                angle = t * math.pi * 1.5
                x = start_x - math.cos(angle) * 200 + (end_x - start_x) * t
                y = start_y + i * 5
                path.append((x, y))

        elif pattern == 1:
            # Loop from right
            for i in range(steps):
                t = i / steps
                angle = t * math.pi * 1.5
                x = start_x + math.cos(angle) * 200 + (end_x - start_x) * t
                y = start_y + i * 5
                path.append((x, y))

        elif pattern == 2:
            # Spiral entry
            for i in range(steps):
                t = i / steps
                angle = t * math.pi * 3
                radius = 150 * (1 - t)
                x = start_x + math.sin(angle) * radius + (end_x - start_x) * t
                y = start_y + i * 5
                path.append((x, y))

        else:
            # Simple curved entry
            for i in range(steps):
                t = i / steps
                x = start_x + (end_x - start_x) * t + math.sin(t * math.pi) * 100
                y = start_y + i * 5
                path.append((x, y))

        # Final position
        path.append((end_x, end_y))

        return path

    def get_random_enemy_for_dive(self):
        """Select a random enemy from formation to dive"""
        import random

        available_enemies = [
            pos['enemy'] for pos in self.formation_positions
            if pos['occupied'] and pos['enemy'] and pos['enemy'].in_formation
        ]

        if available_enemies:
            return random.choice(available_enemies)
        return None

    def get_enemies_in_formation(self):
        """Get count of enemies still in formation"""
        return sum(1 for pos in self.formation_positions
                  if pos['occupied'] and pos['enemy'] and pos['enemy'].in_formation)

    def remove_enemy(self, enemy):
        """Remove enemy from formation"""
        for pos in self.formation_positions:
            if pos['enemy'] == enemy:
                pos['occupied'] = False
                pos['enemy'] = None
                break

    def is_formation_empty(self):
        """Check if all enemies are destroyed"""
        return all(not pos['occupied'] or not pos['enemy'] or not pos['enemy'].active
                  for pos in self.formation_positions)

    def update_formation_sway(self, offset_x):
        """Update formation sway offset"""
        for pos in self.formation_positions:
            if pos['occupied'] and pos['enemy']:
                pos['enemy'].formation_x = pos['x'] + offset_x
