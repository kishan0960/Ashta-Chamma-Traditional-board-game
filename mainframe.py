import os

import pygame
from frame import Frame, Button
from player import Player
import random

class MainFrame(Frame):
    def __init__(self, game, num_players,border_color):
        super().__init__()
        self.border_color =border_color
        cell_size=100
        half_width=12.5
        place4=[(cell_size / 4 - half_width, cell_size / 4 - half_width),
                             ( 3 * cell_size / 4 - half_width, cell_size / 4 - half_width),
                             (cell_size / 4 - half_width, 3 * cell_size / 4 - half_width),
                             (3 * cell_size / 4 - half_width, 3 * cell_size / 4 - half_width)]
        place16=[(0,0),(25,0),(50,0),(75,0),(0,25),(25,25),(50,25),(75,25),(0,50),(25,50),(50,50),(75,50),(0,75),(25,75),(50,75),(75,75)]

        self.shift_array = [[], [(cell_size / 2 - half_width, cell_size / 2 - half_width)],
                            place4,
                            place4,
                            place4,
                            [(cell_size / 4 - half_width, cell_size / 4 - half_width),
                             (3 * cell_size / 4 - half_width, cell_size / 4 - half_width),
                             (cell_size / 4 - half_width, 3 * cell_size / 4 - half_width),
                             (3 * cell_size / 4 - half_width, 3 * cell_size / 4 - half_width),
                             (cell_size / 2 - half_width, cell_size / 2 - half_width)],
                            [(cell_size / 6 - half_width, cell_size / 6 - half_width),
                             (2 * cell_size / 5 - half_width, cell_size / 6 - half_width),
                             (3 * cell_size / 6 - half_width, cell_size / 6 - half_width),
                             (cell_size / 6 - half_width, 4 * cell_size / 6 - half_width),
                             (2 * cell_size / 5 - half_width, 4 * cell_size / 6 - half_width),
                             (3 * cell_size / 6 - half_width, 4 * cell_size / 6 - half_width)],
                            place16,place16,place16,place16,place16,place16,place16,place16,
                            place16, place16, place16, place16, place16, place16, place16, place16,
                            place16, place16, place16, place16, place16, place16, place16, place16,
                            place16, place16, place16, place16, place16, place16, place16, place16]

        #
        print(self.shift_array)

        self.game = game
        self.num_players = num_players
        self.cell_size = 100
        self.board_origin = (50, 50)
        self.board_size = self.cell_size * 5
        self.border_color = self.game.border_color
        self.shell_images = []
        self.pawn_images = []
        self.cross_image = None
        self.current_shell_index = 0
        self.rolling = False
        self.roll_result = [None, None, None, None]
        self.current_player_index = 0
        self.result_value = None
        self.selected_pawn_index = None
        self.turn_stage = "roll"
        self.setup_game()
        self.setup_buttons()
        self.load_shell_images()
        self.load_pawn_images()
        self.load_cross_image()


    def setup_game(self):
        if self.num_players == 2:
            start_positions = [(0, 2), (4, 2)]
        else:
            start_positions = [(0, 2), (2, 0), (4, 2), (2, 4)]

        self.players = [
            Player(i, start_positions[i]) for i in range(self.num_players)
        ]
        self.place_pawns()

    def setup_buttons(self):
        button=Button("Roll Shell", 550, 150, self.roll_shell)
        button.color=self.border_color
        self.add_button(button)
        button = Button("Exit", 550, 450, self.exit_game)
        button.color = self.border_color
        self.add_button(button)
        button = Button("Back", 550, 550, self.back_to_menu)
        button.color = self.border_color
        self.add_button(button)

    def load_shell_images(self):
        for i in range(2):
            image = pygame.image.load(f'assets/animations/shell{i}.png')
            scaled_image = pygame.transform.scale(image, (50, 50))
            self.shell_images.append(scaled_image)

    def load_pawn_images(self):
        for i in range(4):
            image = pygame.image.load(f'assets/icons/{i}.png')
            scaled_image = pygame.transform.scale(image, (25, 25))
            self.pawn_images.append(scaled_image)

    def load_cross_image(self):
        image = pygame.image.load('assets/icons/cross.png')
        self.cross_image = pygame.transform.scale(image, (self.cell_size, self.cell_size))

    def place_pawns(self):
        if self.num_players == 2:
            safehouses = [(0, 2), (4, 2)]
        else:
            safehouses = [(0, 2), (2, 0), (4, 2), (2, 4)]
        
        pawn_offsets = [(12.5, 12.5), (62.5, 12.5), (12.5, 62.5), (62.5, 62.5)]

        for i, player in enumerate(self.players):
            player.pawns = [(self.board_origin[0] + (safehouses[i][1] * self.cell_size) + offset[0],
                             self.board_origin[1] + (safehouses[i][0] * self.cell_size) + offset[1])
                            for offset in pawn_offsets]
            player.positions = [0] * 4  # Reset positions

    def roll_shell(self):
        if self.turn_stage == "roll":
            self.rolling = True
            self.current_shell_index = 0
            self.roll_result = [None, None, None, None]
            self.turn_stage = "move"

    def update(self):
        if self.rolling:
            self.current_shell_index = (self.current_shell_index + 1) % len(self.shell_images)
            if self.current_shell_index == 0:
                self.rolling = False
                self.roll_result = [random.choice(self.shell_images) for _ in range(4)]
                self.result_value = self.calculate_roll_result()
                if not  self.players[self.current_player_index].move_exists(self.result_value):
                    self.switch_turn()
                    self.rolling = True


                #self.result_value = len(self.players[0].board_path)-1 #used to test winning

    def calculate_roll_result(self):
        face_up_count = sum(1 for img in self.roll_result if img == self.shell_images[1])
        if face_up_count == 0:
            return 8
        return face_up_count
    def is_safe(self,position):
        return not (not (position[0] % 2==1 or position[1]  % 2==1) and (position[0] ==2 or position[1]==2))

    def move_pawn(self, steps):
        if self.selected_pawn_index is not None:
            player = self.players[self.current_player_index]
            pawn_index = self.selected_pawn_index
            if player.positions[pawn_index]+steps>=len(player.board_path):
                return
            new_position = player.move_pawn(pawn_index, steps)
            # place pawn in cell
            killed=False
            if self.is_safe(new_position):
                killed=self.kill_pawns(new_position)

            self.allign_pawns(new_position)
            #player.pawns[pawn_index] = (self.board_origin[0] + new_position[1] * self.cell_size,
            #                            self.board_origin[1] + new_position[0] * self.cell_size)
            self.selected_pawn_index = None
            self.turn_stage = "roll"
            if not killed:
                if not (steps==8 or steps==4):
                    self.switch_turn()

    def allign_pawns(self,new_position):
        count = 0
        for player in self.players:
            count += player.get_pawn_count(new_position)
        index = 0
        top_left_corner = (self.board_origin[0] + new_position[1] * self.cell_size,
                           self.board_origin[1] + new_position[0] * self.cell_size)
        for player in self.players:
            index = player.set_positions(index, new_position, self.shift_array[count], top_left_corner)

    def kill_pawns(self,position):
        for i,player in enumerate(self.players):
            if i!=self.current_player_index and player.kill_pawns(position)>0 :
                self.allign_pawns(player.board_path[0])
                return True
        return False



    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.draw_board(screen)
        for button in self.buttons:
            button.draw(screen)
        self.draw_shells(screen)
        self.draw_pawns(screen)
        self.draw_current_player(screen)

    def draw_board(self, screen):
        for row in range(5):
            for col in range(5):
                rect = pygame.Rect(
                    self.board_origin[0] + col * self.cell_size,
                    self.board_origin[1] + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, self.border_color, rect, 1)
        self.draw_safehouses(screen)

    def draw_safehouses(self, screen):
        safehouses = [(0, 2), (2, 0), (4, 2), (2, 4), (2,2)]
        for (row, col) in safehouses:
            screen.blit(self.cross_image, (self.board_origin[0] + col * self.cell_size,
                                           self.board_origin[1] + row * self.cell_size))

    def draw_shells(self, screen):
        shell_positions = [(550, 250), (600, 250), (650, 250), (700, 250)]
        if self.rolling:
            shell_image = self.shell_images[self.current_shell_index]
            for pos in shell_positions:
                screen.blit(shell_image, pos)
        else:
            for i, pos in enumerate(shell_positions):
                if self.roll_result[i] is not None:
                    screen.blit(self.roll_result[i], pos)
        if self.result_value is not None and self.turn_stage != "roll":
            font = pygame.font.SysFont(None, 36)
            result_text = font.render(f"Player ", True, (0, 0, 0))
            screen.blit(result_text, (550, 350))
            pawn_image = self.pawn_images[self.current_player_index]
            screen.blit(pawn_image, (630, 350))
            result_text_contd = font.render(f" rolled {self.result_value}", True, (0, 0, 0))
            screen.blit(result_text_contd, (660, 350))

    def draw_pawns(self, screen):
        for player in self.players:
            pawn_image = self.pawn_images[player.player_id]
            for pos in player.pawns:
                #need to check position
                screen.blit(pawn_image, pos)

    def draw_current_player(self, screen):
        pawn_image = self.pawn_images[self.current_player_index]
        screen.blit(pawn_image, (50, 10))
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Player {self.current_player_index + 1}'s turn - Roll the Dice", True, (0, 0, 0))
        screen.blit(text, (90, 10))

    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players
        if self.current_player_index == 0:
            winners = []
            winners_indexes = []
            for i, winner in enumerate(self.players):
                if winner.is_winner():
                    winners.append(winner)
                    winners_indexes.append(i + 1)
            if len(winners) > 0:
                if len(winners) == len(self.players):
                    self.message = ["Game over! Tie"]
                elif len(winners) == 1:
                    self.message = ["Winner is Player " + str(winners_indexes[0])]
                else:
                    self.message = ["Winners list " + str(winners_indexes)]
                self.game.message_box(self.message)

    def set_border_color(self, color):
        self.border_color = color

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            pos = pygame.mouse.get_pos()
            self.check_pawn_click(pos)

    def check_pawn_click(self, pos):
        if self.turn_stage == "move":
            for i, player in enumerate(self.players):
                for j, pawn_pos in enumerate(player.pawns):
                    pawn_rect = pygame.Rect(pawn_pos[0], pawn_pos[1], 25, 25)
                    if pawn_rect.collidepoint(pos):
                        if i == self.current_player_index:
                            self.selected_pawn_index = j
                            self.move_pawn(self.result_value)
                            return

    def exit_game(self):
        exit(-1)

    def back_to_menu(self):
        self.game.back_to_menu()
