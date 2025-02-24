import pygame
import sys
from start_screen import StartScreen
import math

start_screen = StartScreen()
clock = pygame.time.Clock()
delta_time = 0
player_pos = pygame.Vector2(start_screen.screen.get_width() / 2, start_screen.screen.get_height() / 2)
# Define TIE Fighter points to form the shape of the spaceship
spaceship_points = [
    # Cockpit (center)
    (640, 200),  # Top of the cockpit
    (600, 300),  # Bottom left of the cockpit
    (680, 300),  # Bottom right of the cockpit
    (660, 240),  # Right side of the cockpit
    (620, 240),  # Left side of the cockpit

    # Left wing panel (outer edges)
    (520, 280),  # Top left of the left wing
    (450, 180),  # Left side of the left panel (outer)
    (450, 420),  # Left side of the left panel (bottom)
    (520, 420),  # Left bottom of the left wing

    # Right wing panel (outer edges)
    (760, 280),  # Top right of the right wing
    (830, 180),  # Right side of the right panel (outer)
    (830, 420),  # Right side of the right panel (bottom)
    (760, 420),  # Right bottom of the right wing
]
running = True

start_screen.start_screen_loop()

if not start_screen.is_running:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        start_screen.screen.fill("black")

        # pygame.cursors.Cursor()
        pygame.draw.circle(start_screen.screen, "red", player_pos, 40)
        # circle(surface, color, center, radius) make it look like tie interceptor with circle in middle
        # pygame.draw.polygon(start_screen.screen, "green", spaceship_points, width=0)
        # polygon(surface, color, points, width=0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_pos.y -= 300 * delta_time
        if keys[pygame.K_DOWN]:
            player_pos.y += 300 * delta_time
        if keys[pygame.K_LEFT]:
            player_pos.x -= 300 * delta_time
        if keys[pygame.K_RIGHT]:
            player_pos.x += 300 * delta_time

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for frame-rate independent physics.
        delta_time = clock.tick(60) / 1000

# if __name__ == "__main__":
#     main()