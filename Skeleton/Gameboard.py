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

    def set_p2_color(self):
        if self.player1 == "red":
            self.player2 = "yellow"
        elif self.player1 == "yellow":
            self.player2 = "red"
        else:
            self.player2 = "Error"

        return None

    def check_current_turn(self, current_player):
        return True if self.current_turn == current_player else False

    def check_filled_column(self, column_num):
        return True if self.board[0][column_num - 1] == 0 else False

    def update_board(self, column_num, color):
        column_index = column_num - 1
        largest_row_index = len(self.board) - 1
        
        for r in range(largest_row_index, -1, -1):
            if self.board[r][column_index] == 0:
                self.board[r][column_index] = color
                break
        
        return None

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
                if self.board[r][c] == color and self.board[r-1][c+1] == color and self.board[r-2][c+2] == color and self.board[r-3][c+3] == color:
                    self.game_result = self.current_turn
                    return True

        # check if \ diagonal win
        for c in range(num_cols - 3):
            for r in range(num_rows - 3):
                if self.board[r][c] == color and self.board[r+1][c+1] == color and self.board[r+2][c+2] == color and self.board[r+3][c+3] == color:
                    self.game_result = self.current_turn
                    return True

        return False

    def continue_game(self, other_player):
        self.remaining_moves -= 1
        self.current_turn = other_player
