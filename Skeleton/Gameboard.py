import db

class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    
    #  'col#' where col# can be col1 - col7
    # update your backend board to match the frontend board (self.board)
    # invalid: 
       # - user tried to insert into a filled column 
       # - make a move when it wasn't their turn


    def check_current_turn(self, current_player):
        if self.current_turn == current_player:
            return True
        return False

    def check_filled_column(self, column_num):
        if self.board[0][column_num - 1] == 0:
            return True  
        return False

    def update_board(self, column_num, curr_player_num):
        column_index = column_num - 1
        largest_row_index = len(self.board) - 1
        
        for r in range(largest_row_index, -1, -1):
            if self.board[r][column_index] == 0:
                self.board[r][column_index] = curr_player_num
                break
        
        return None

    def check_if_win(self, curr_player_num, ):
        pass
        # check if four 1's in a row

        # check horizontal win (check each row)


        
        


    def continue_game(self, other_player):
        self.remaining_moves -= 1
        self.current_turn = other_player



'''
Add Helper functions as needed to handle moves and update board and turns
'''
