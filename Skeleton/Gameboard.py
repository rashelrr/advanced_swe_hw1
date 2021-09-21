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
            return True, ""
        else:
            return False, "Not your turn. Please wait your turn."

    def check_filled_column(self, column_num):

        if self.board[0][column_num - 1] == 0:
            return True, ""      
        else:
            return False, "Column is filled. Please choose a different column."

    def update_board(self):
        self.board


    def check_if_win(self):
        if ...:
            pass
            # modify self.board to reflect change...?
        else: 
            self.game_result = ""


            # call continue_game if no one won

            # return: p1, p2, or ""


    def continue_game(self, other_player):
        self.remaining_moves -= 1
        self.current_turn = other_player



    

'''
Add Helper functions as needed to handle moves and update board and turns
'''

    
