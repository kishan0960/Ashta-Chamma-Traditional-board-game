import pygame
import os
from frame import Frame, Button

class BoxFrame(Frame):
    def __init__(self, game, message):
        super().__init__()
        self.game = game
        self.message = message
        self.font = pygame.font.SysFont(None, 24)  # Set font size
        self.image = pygame.image.load(os.path.join('assets', 'icons', 'movement.png'))  # Load the image
        self.setup_buttons()

    def setup_buttons(self):
        self.add_button(Button("Close", 600, 550, self.close_box))

    def close_box(self):
        self.game.back_to_menu()

    def draw(self, screen):
        super().draw(screen)
        self.draw_message_and_image(screen)

    def draw_message_and_image(self, screen):
        y = 50  # Starting y position for the text
        for line in self.message:
            if isinstance(line, str):  # Ensure the line is a string
                result_text = self.font.render(line, True, (0, 0, 0))
                screen.blit(result_text, (50, y))
                y += 30  # Spacing between lines

        # After drawing all text, draw the image
        if self.image:
            # Get screen dimensions
            screen_width, screen_height = screen.get_size()
            # Get image dimensions
            img_width, img_height = self.image.get_size()
            # Calculate position to center the image below the text
            img_x = (screen_width - img_width) // 2
            # Draw the image directly below the last line of text
            screen.blit(self.image, (img_x, y + 20))  # 20 pixels gap between text and image
