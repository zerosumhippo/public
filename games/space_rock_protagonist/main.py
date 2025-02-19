import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
delta_time = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

pygame.display.set_caption("Space Rock Protagonist")
# Set up fonts
font = pygame.font.SysFont("Arial", 48)
small_font = pygame.font.SysFont("Arial", 24)
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_start_screen():
    screen.fill(BLACK)  # Fill the screen with a black color
    title_text = font.render("My Game", True, WHITE)
    instruction_text = small_font.render("Press any key to start", True, WHITE)

    # Position the text on the screen
    title_rect = title_text.get_rect(center=(400, 200))
    instruction_rect = instruction_text.get_rect(center=(400, 400))

    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)

    pygame.display.update()


running = True

# start screen
while running:
    in_start_screen = True

    while in_start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_start_screen = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # If any key is pressed or mouse is clicked, move to the game
                in_start_screen = False

        # Draw the start screen
        draw_start_screen()
        pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS

    # Transition to the main game (for now, we can just print a message)
    print("Start the game!")
    # Here you could add code to initialize the main game logic

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