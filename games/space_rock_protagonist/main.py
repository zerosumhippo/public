import pygame
import sys
from start_screen import StartScreen
import math

BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
WHITE = (255, 255, 255)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

SCREEN_HEIGHT = 720

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

        # top_cockpit_polygon
        pygame.draw.polygon(start_screen.screen, GRAY, [(375, 250), (425, 250), (440, 275), (360, 275)])
        # middle square
        pygame.draw.rect(start_screen.screen, GRAY, (361, 276, 79, 24))
        # bottom_cockpit_polygon
        pygame.draw.polygon(start_screen.screen, GRAY, [(375, 325), (425, 325), (440, 300), (360, 300)])

        # Draw the left wing (polygon)
        pygame.draw.polygon(start_screen.screen, DARK_GRAY, [(360, 275), (300, 200), (300, 350), (360, 300)])

        # Draw the right wing (polygon)
        pygame.draw.polygon(start_screen.screen, DARK_GRAY, [(440, 275), (500, 200), (500, 350), (440, 300)])

        # Draw the cockpit (small circle in the middle)
        pygame.draw.circle(start_screen.screen, BLUE, (401, 290), 16)

        # Top - Draw the wing struts (lines connecting the body and wings)
        pygame.draw.line(start_screen.screen, GRAY, (375, 250), (300, 200), 3)
        pygame.draw.line(start_screen.screen, GRAY, (425, 250), (500, 200), 3)

        # Top - Draw the diagonal crossbars inside the wings
        pygame.draw.line(start_screen.screen, WHITE, (360, 275), (300, 200), 3)
        pygame.draw.line(start_screen.screen, WHITE, (440, 275), (500, 200), 3)

        # Bottom - Draw the wing struts (lines connecting the body and wings)
        # pygame.draw.line(start_screen.screen, GRAY, (375, 325), (300, 225), 3)
        # pygame.draw.line(start_screen.screen, GRAY, (425, 325), (500, 225), 3)

        # Draw the inner shape inside the wings (triangular details)
        pygame.draw.polygon(start_screen.screen, RED, [(300, 200), (315, 240), (300, 240)])
        pygame.draw.polygon(start_screen.screen, RED, [(500, 200), (485, 240), (500, 240)])

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