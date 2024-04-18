from os import system


class TicTacToe:
    """Text based tic-tac-toe game."""

    def __init__(self):
        self.game_board_list = []
        self.row_delimiter = "|"
        self.game_board_row = ""
        self.game_on = True
        self.input_error = "\nPlease select a number between 1 and 9.\n"
        self.turn_number = 1
        self.game_piece_index_list = [n for n in range(0, 17, 2)]
        """Defines the indices of the X's and O's in self.game_board_list."""

    def create_game_board(self):
        for i in range(1, 10):
            row_value = f" {i} "
            self.game_board_list.append(row_value)
            if i % 3 != 0:
                self.game_board_list.append(self.row_delimiter)
            if i % 3 == 0 and i < 9:
                self.game_board_list.append("___________\n")
        for i in range(1, 18):
            if i % 6 != 0:
                self.game_board_row += self.game_board_list[i - 1]
            if i % 6 == 0:
                print(self.game_board_row)
                print(self.game_board_list[i - 1])
                self.game_board_row = ""
            if i == 17:
                print(self.game_board_row)
                self.game_board_row = ""

    def game_piece_placement(self, game_piece):
        """The expected input for game_piece is either "X" or "O"."""
        if game_piece == "X":
            player_number = 1
        else:
            player_number = 2
        game_piece_input = input(f"Player {player_number} is {game_piece}. Please provide a number between 1 and 9 to "
                                 f"place your {game_piece}: ")
        try:
            int(game_piece_input)
        except ValueError:
            return self.input_error
        else:
            if int(game_piece_input) not in range(1, 10):
                return self.input_error
            else:
                for item in self.game_board_list:
                    if f"{game_piece_input}" == item.strip():
                        item_index = self.game_board_list.index(item)
                        self.game_board_list[item_index] = f" {game_piece} "
                system('cls')
                self.turn_number += 1

    def check_score(self):
        for n in self.game_piece_index_list:
            if n == 2 or n == 8 or n == 14:
                if self.game_board_list[n-2] == self.game_board_list[n] == self.game_board_list[n+2]:
                    print(f"\n{self.game_board_list[n].strip()} wins!")
                    self.game_on = False
            if n == 6 or n == 8 or n == 10:
                if self.game_board_list[n-6] == self.game_board_list[n] == self.game_board_list[n+6]:
                    print(f"\n{self.game_board_list[n].strip()} wins!")
                    self.game_on = False
            if n == 0 or n == 8 or n == 16:
                if self.game_board_list[n-8] == self.game_board_list[n] == self.game_board_list[n+8]:
                    print(f"\n{self.game_board_list[n].strip()} wins!")
                    self.game_on = False
            if n == 4 or n == 8 or n == 12:
                if self.game_board_list[n-4] == self.game_board_list[n] == self.game_board_list[n+4]:
                    print(f"\n{self.game_board_list[n].strip()} wins!")
                    self.game_on = False

    def play_tic_tac_toe(self):
        self.create_game_board()
        while self.game_on:
            if self.turn_number % 2 != 0:
                if self.game_piece_placement(game_piece="X") == self.input_error:
                    print(self.input_error)
            else:
                if self.game_piece_placement(game_piece="O") == self.input_error:
                    print(self.input_error)
            self.create_game_board()
            self.check_score()
