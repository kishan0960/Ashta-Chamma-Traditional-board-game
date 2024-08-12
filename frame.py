import pygame

class Button:
    def __init__(self, text, x, y, action):
        self.text = text
        self.x = x
        self.y = y
        self.action = action
        self.rect = pygame.Rect(x, y, 200, 50)
        self.font = pygame.font.Font(None, 36)
        self.color = (0, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, (self.x + 10, self.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

class Frame:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((100, 100, 100))
        for button in self.buttons:
            button.draw(screen)
