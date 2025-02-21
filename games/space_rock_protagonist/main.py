import pygame
import sys
from start_screen import StartScreen

start_screen = StartScreen()
clock = pygame.time.Clock()
delta_time = 0
player_pos = pygame.Vector2(start_screen.screen.get_width() / 2, start_screen.screen.get_height() / 2)


start_screen.start_screen_loop()

# game screen
# while running:
#     # poll for events
#     for event in pygame.event.get():
#         # pygame.QUIT event means the user clicked X to close your window
#         if event.type == pygame.QUIT:
#             running = False
#
#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("black")
#
#     # pygame.cursors.Cursor()
#     pygame.draw.circle(screen, "green", player_pos, 40)
#
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_UP]:
#         player_pos.y -= 300 * delta_time
#     if keys[pygame.K_DOWN]:
#         player_pos.y += 300 * delta_time
#     if keys[pygame.K_LEFT]:
#         player_pos.x -= 300 * delta_time
#     if keys[pygame.K_RIGHT]:
#         player_pos.x += 300 * delta_time
#
#     # flip() the display to put your work on screen
#     pygame.display.flip()
#
#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for frame-rate independent physics.
#     delta_time = clock.tick(60) / 1000

# if __name__ == "__main__":
#     main()