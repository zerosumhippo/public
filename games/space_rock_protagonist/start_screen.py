import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 203, 0)
GAME_TITLE_TEXT = "Space Rock Protagonist"


class StartScreen:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.game_title = pygame.display.set_caption(GAME_TITLE_TEXT)
        self.game_title_font = pygame.font.Font("assets/fonts/Astron Boy Video.otf", 100)
        self.instruct_font = pygame.font.SysFont("impact", 24)
        self.is_running = True

    def fill_screen_black(self):
        self.screen.fill(BLACK)

    def draw_start_screen(self):
        self.fill_screen_black()
        title_text = self.game_title_font.render(GAME_TITLE_TEXT, True, WHITE)
        instruction_text = self.instruct_font.render("Press any key to start", True, GREEN)

        title_rect = title_text.get_rect(center=(640, 160))
        instruction_rect = instruction_text.get_rect(center=(640, 360))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(instruction_text, instruction_rect)

        pygame.display.update()

    def start_screen_loop(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # If any key is pressed or mouse is clicked, move to the game
                    self.is_running = False
                    self.fill_screen_black()
            self.draw_start_screen()
            pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS
