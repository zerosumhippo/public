import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 203, 0)


class StartScreen:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.game_title = pygame.display.set_caption("Space Rock Protagonist")
        self.game_title_font = font = pygame.font.Font("assets/fonts/Astron Boy Video.otf", 100)
        self.instruct_font = pygame.font.SysFont("impact", 24)
        self.game_is_running = True

    def draw_start_screen(self):
        self.screen.fill(BLACK)
        title_text = self.game_title_font.render("Space Rock Protagonist", True, WHITE)
        instruction_text = self.instruct_font.render("Press any key to start", True, GREEN)

        title_rect = title_text.get_rect(center=(640, 160))
        instruction_rect = instruction_text.get_rect(center=(640, 360))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(instruction_text, instruction_rect)

        pygame.display.update()

    def start_screen_loop(self):
        in_start_screen = True
        while in_start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_start_screen = False
                    self.game_is_running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # If any key is pressed or mouse is clicked, move to the game
                    in_start_screen = False
                    print("Start the game!")
                    # Transition to the main game (for now, we can just print a message)
            self.draw_start_screen()
            pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS
