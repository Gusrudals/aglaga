#!/usr/bin/env python3
"""
GALAGA - Classic Arcade Game
Recreated in Python with Pygame

Based on the original Namco Galaga (1981)
"""

from game import Game


def main():
    """Main entry point"""
    print("=" * 50)
    print("GALAGA - Classic Arcade Game")
    print("=" * 50)
    print("\nControls:")
    print("  ARROW KEYS or A/D - Move left/right")
    print("  SPACE or Z - Shoot")
    print("  ESC - Quit")
    print("\nStarting game...")
    print("=" * 50)

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
