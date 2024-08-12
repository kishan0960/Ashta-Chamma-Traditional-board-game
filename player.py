path_dict={ (0, 2) : [(0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (2, 1), (1, 1), (1, 2), (2, 2)],
        (2, 0) : [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (2, 1), (2, 2)],
        (4, 2) : [(4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (2, 2)],
        (2, 4) : [(2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (3, 3), (3, 2), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (2, 2)]}


class Player:
    def __init__(self, player_id, start_position):
        self.player_id = player_id
        self.start_position = start_position
        self.pawns = []
        self.positions = [0, 0, 0, 0]  # Each pawn's position index in the path

        # Define the board path in a counterclockwise direction starting from (0, 2)
        self.board_path = path_dict[start_position]


    def move_pawn(self, pawn_index, steps):
        """
        Moves the specified pawn by the number of steps along the board path.
        The movement starts from the player's starting position and follows a counterclockwise path.
        """
        # Find the starting index on the path based on the player's start position
        #start_index = self.board_path.index(self.start_position)



        # Update the pawn's position index
        self.positions[pawn_index] = self.positions[pawn_index]+steps

        # Return the new position on the board
        return self.board_path[self.positions[pawn_index]]
    #return number of pawns
    def get_pawn_count(self, cell):
        count=0
        for position in self.positions:
            if self.board_path[position]==cell:
                count +=1
        return count

    def kill_pawns(self, cell):
        count=0
        for i,position in enumerate(self.positions):
            if self.board_path[position]==cell:
                self.positions[i]=0
                count +=1
        return count


    def set_positions(self,index,cell,shift_array,top_left_corner):
        for i,position in enumerate(self.positions):
            if self.board_path[position] == cell:
                self.pawns[i]=(shift_array[index][0]+top_left_corner[0],shift_array[index][1]+top_left_corner[1])
                index+=1
        return index

    def move_exists(self, numsteps):
        for i, pawn in enumerate(self.positions):
            if pawn + numsteps < len(self.board_path):
                return True
        return False

    def is_winner(self):
        """

        :return: True if all player pawns at destination cell
        """
        result = 0
        for pawn in self.positions:
            if len(self.board_path) - 1 == pawn:
                result += 1
        return result == len(self.positions)






