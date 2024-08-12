import pygame
import sys
import os
from menuframe import MenuFrame
from mainframe import MainFrame
from boxframe import BoxFrame

class Game:
    def __init__(self):
        pygame.init()
        # Set the window title
        pygame.display.set_caption("Ashta Chamma Board game")

        # Set the window icon
        icon = pygame.image.load(os.path.join('assets', 'icons', 'game_icon.jpg'))
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.border_color = (0, 0, 0)  # Default border color
        self.menu_frame = MenuFrame(self)
        self.frame = self.menu_frame

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.frame.handle_event(event)
            self.frame.update()
            self.frame.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def start_game(self, num_players):
        self.frame = MainFrame(self, num_players, self.border_color)

    def back_to_menu(self):
        self.frame = MenuFrame(self)

    def message_box(self, message):
        self.frame = BoxFrame(self, message)

    def set_border_color(self, color):
        self.border_color = color
        if isinstance(self.frame, MainFrame):
            self.frame.set_border_color(color)

if __name__ == "__main__":
    game = Game()
    game.run()
