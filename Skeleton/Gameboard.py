import db


class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    '''
    Add Helper functions as needed to handle moves and update board and turns
    '''

    def continue_game_with_last_move(self, move):
        # Resets game values with last move saved in database
        if move[0] == 'p1':
            self.current_turn = 'p2'
        else:
            self.current_turn = 'p1'

        self.game_result = move[2]
        self.player1 = move[3]
        self.player2 = move[4]
        self.remaining_moves = move[5]

        # reformats string board and converts into 1D array
        str_board = move[1]
        str_board = str_board.replace('[', '')
        str_board = str_board.replace(']', '')
        str_board = str_board.replace("'", '')
        board_lst = str_board.split(', ')

        # convert numerical strings to ints
        for i, x in enumerate(board_lst):
            if x == "red" or x == "yellow":
                continue
            else:
                board_lst[i] = int(x)

        # convert to 2D array
        board_2d_lst = []
        for i in range(len(board_lst)):
            if i % 7 == 0:
                board_2d_lst.append(board_lst[i: i + 7])

        self.board = board_2d_lst

    def set_p2_color(self):
        if self.player1 == "red":
            self.player2 = "yellow"
        elif self.player1 == "yellow":
            self.player2 = "red"
        else:
            self.player2 = "Error"

    def check_p1_picked_color(self):
        return False if self.player1 == "" else True

    def check_current_turn(self, current_player):
        return True if self.current_turn == current_player else False

    def check_filled_column(self, column_num):
        return True if self.board[0][column_num - 1] == 0 else False

    def update_board(self, column_num, color):

        can_update_board = False  # winner already declared

        if self.game_result == "" and self.remaining_moves > 0:
            # no winner declared
            can_update_board = True
            column_index = column_num - 1
            largest_row_index = len(self.board) - 1

            for r in range(largest_row_index, -1, -1):
                if self.board[r][column_index] == 0:
                    self.board[r][column_index] = color
                    break

        return can_update_board

    def check_if_draw(self):
        return True if self.remaining_moves == 0 else False

    def check_if_win(self, color):
        num_rows = len(self.board)
        num_cols = len(self.board[0])
        check_up_to_row = len(self.board) - 4 + 1
        check_up_to_column = len(self.board[0]) - 4 + 1

        # check horizontal win (check each row)
        for row in self.board:
            for c in range(check_up_to_column):
                if row[c:c+4] == [color, color, color, color]:
                    self.game_result = self.current_turn
                    return True

        # check vertical win (check each column)
        for c in range(num_cols):
            for r in range(check_up_to_row):
                pot_col = [row[c] for row in self.board][r:r+4]
                if pot_col == [color, color, color, color]:
                    self.game_result = self.current_turn
                    return True

        # check if / diagonal win
        for c in range(num_cols - 3):
            for r in range(3, num_rows):
                if (self.board[r][c] == color and
                        self.board[r-1][c+1] == color and
                        self.board[r-2][c+2] == color and
                        self.board[r-3][c+3] == color):
                    self.game_result = self.current_turn
                    return True

        # check if \ diagonal win
        for c in range(num_cols - 3):
            for r in range(num_rows - 3):
                if (self.board[r][c] == color and
                        self.board[r+1][c+1] == color and
                        self.board[r+2][c+2] == color and
                        self.board[r+3][c+3] == color):
                    self.game_result = self.current_turn
                    return True

        # at this point, either a tie or nothing
        return False

    def update_remaining_moves(self):
        self.remaining_moves -= 1

    def update_current_turn(self):
        if self.current_turn == 'p1':
            self.current_turn = 'p2'
        else:
            self.current_turn = 'p1'
