import pygame
import os
from frame import Frame, Button

class MenuFrame(Frame):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.logo_image = pygame.image.load(os.path.join('assets', 'icons', 'logo.png'))
        self.setup_buttons()

    def setup_buttons(self):
        self.add_button(Button("2 Players", 200, 150, self.start_2_players))
        self.add_button(Button("3 Players", 200, 250, self.start_3_players))
        self.add_button(Button("4 Players", 200, 350, self.start_4_players))
        self.add_button(Button("Quit", 200, 450, self.quit_game))
        self.add_button(Button("Red Border", 450, 150, self.set_color_red))
        self.add_button(Button("Green Border", 450, 250, self.set_color_green))
        self.add_button(Button("Blue Border", 450, 350, self.set_color_blue))
        self.add_button(Button("Rules", 450, 450, self.show_rules))

    def start_2_players(self):
        self.game.start_game(2)

    def start_3_players(self):
        self.game.start_game(3)

    def start_4_players(self):
        self.game.start_game(4)

    def show_rules(self):
    # Display the rules in the message box using BoxFrame
        rules = [
        "Astha Chamma Game Rules:",
        "1. Each player starts with four pawns.",
        "2. The objective is to move all pawns to the center of the board.",
        "3. Players roll four shells. It will result in 1, 2, 3, 4, or 8.",
        "   (If you roll 4 or 8, you get another turn).",
        "4. If a player's pawn lands on a space occupied by an opponent's",
        "   pawn, the opponent's pawn is sent back to the start.",
        "5. The first player to move all their pawns to the center wins."
        ]
        self.game.message_box(rules)  # Pass the rules to the message box

    def quit_game(self):
        self.game.running = False

    def set_color_red(self):
        self.game.set_border_color((255, 0, 0))

    def set_color_green(self):
        self.game.set_border_color((0, 255, 0))

    def set_color_blue(self):
        self.game.set_border_color((0, 0, 255))

    def draw(self, screen):
        super().draw(screen)
        self.draw_logo(screen)

    def draw_logo(self, screen):
        if self.logo_image:
            screen_width, screen_height = screen.get_size()
            logo_width, logo_height = self.logo_image.get_size()
            logo_x = (screen_width - logo_width) // 2
            logo_y = 50
            screen.blit(self.logo_image, (logo_x, logo_y))
