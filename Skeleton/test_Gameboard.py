import unittest
from Gameboard import Gameboard


class Test_TestGameboard(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.gameboard = Gameboard()

    def tearDown(self):
        print('tearDown\n')
        self.gameboard = None

    def set_up_game(self, player1, player2, game_result, current_turn,
                    remaining_moves):
        # Sets up Gameboard fields
        self.gameboard.player1 = player1
        self.gameboard.player2 = player2
        self.gameboard.game_result = game_result
        self.gameboard.current_turn = current_turn
        self.gameboard.remaining_moves = remaining_moves

    def set_up_board(self, player1, player2, board, p1_coordinates,
                     p2_coordinates):
        # Sets up board
        for coordinate in p1_coordinates:
            r = coordinate[0]
            c = coordinate[1]
            board[r][c] = player1
        for coordinate in p2_coordinates:
            r = coordinate[0]
            c = coordinate[1]
            board[r][c] = player2

        return board

    def test_horizontal_win(self):
        # Checks if there is a winning move in horizontal direction

        # set up game
        p1_coordinates = [(5, 0), (5, 1), (5, 2)]
        p2_coordinates = [(4, 0), (4, 1), (4, 2)]
        self.set_up_game("red", "yellow", "", 'p1', 36)
        self.set_up_board("red", "yellow", self.gameboard.board,
                          p1_coordinates, p2_coordinates)
        column_num = 4

        # updates board with move
        self.gameboard.update_board(column_num, self.gameboard.player1)
        p1_coordinates.append((5, 3))
        expected_board = [[0 for x in range(7)] for y in range(6)]
        expected_board = self.set_up_board("red", "yellow", expected_board,
                                           p1_coordinates, p2_coordinates)

        # assert result board and expected board are equal
        self.assertEqual(self.gameboard.board, expected_board)

        # assert check_if_win is True
        won = self.gameboard.check_if_win(self.gameboard.player1)
        self.assertTrue(won)

        # assert winner is player1
        self.assertTrue(self.gameboard.game_result, 'p1')

    def test_vertical_win(self):
        # Checks if there is a winning move in vertical direction

        # set up game
        p1_coordinates = [(5, 1), (4, 1), (5, 2)]
        p2_coordinates = [(5, 3), (4, 3), (3, 3)]
        self.set_up_game("yellow", "red", "", 'p2', 36)
        self.set_up_board("yellow", "red", self.gameboard.board,
                          p1_coordinates, p2_coordinates)
        column_num = 4

        # updates board with move
        self.gameboard.update_board(column_num, self.gameboard.player2)
        p2_coordinates.append((2, 3))
        expected_board = [[0 for x in range(7)] for y in range(6)]
        expected_board = self.set_up_board("yellow", "red", expected_board,
                                           p1_coordinates, p2_coordinates)

        # assert result board and expected board are equal
        self.assertEqual(self.gameboard.board, expected_board)

        # assert check_if_win is True
        won = self.gameboard.check_if_win(self.gameboard.player2)
        self.assertTrue(won)

        # assert winner is player2
        self.assertTrue(self.gameboard.game_result, 'p2')

    def test_positive_diag_win(self):
        # Checks if winning move in the positive-sloped diagonal direction

        # set up game
        p1_coordinates = [(5, 0), (4, 1), (4, 2), (3, 2), (5, 4)]
        p2_coordinates = [(5, 1), (5, 2), (5, 3), (4, 3), (3, 3)]
        self.set_up_game("red", "yellow", "", 'p1', 32)
        self.set_up_board("red", "yellow", self.gameboard.board,
                          p1_coordinates, p2_coordinates)
        column_num = 4

        # updates board with move
        self.gameboard.update_board(column_num, self.gameboard.player1)
        p1_coordinates.append((2, 3))
        expected_board = [[0 for x in range(7)] for y in range(6)]
        expected_board = self.set_up_board("red", "yellow", expected_board,
                                           p1_coordinates, p2_coordinates)

        # assert result board and expected board are equal
        self.assertEqual(self.gameboard.board, expected_board)

        # assert check_if_win is True
        won = self.gameboard.check_if_win(self.gameboard.player1)
        self.assertTrue(won)

        # assert winner is player1
        self.assertTrue(self.gameboard.game_result, 'p1')

    def test_negative_diag_win(self):
        # Checks if winning move in the negative-sloped diagonal direction

        # set up game
        p1_coordinates = [(5, 3), (4, 3), (3, 4), (4, 5), (5, 6)]
        p2_coordinates = [(5, 2), (3, 3), (5, 4), (4, 4), (5, 5)]
        self.set_up_game("red", "yellow", "", 'p1', 32)
        self.set_up_board("red", "yellow", self.gameboard.board,
                          p1_coordinates, p2_coordinates)
        column_num = 4

        # updates board with move
        self.gameboard.update_board(column_num, self.gameboard.player1)
        p1_coordinates.append((2, 3))
        expected_board = [[0 for x in range(7)] for y in range(6)]
        expected_board = self.set_up_board("red", "yellow", expected_board,
                                           p1_coordinates, p2_coordinates)

        # assert result board and expected board are equal
        self.assertEqual(self.gameboard.board, expected_board)

        # assert check_if_win is True
        won = self.gameboard.check_if_win(self.gameboard.player1)
        self.assertTrue(won)

        # assert winner is player1
        self.assertTrue(self.gameboard.game_result, 'p1')

    '''def test_happy_move(self):
        # Checks if happy path for correct move

        self.gameboard.player1 = "red"
        self.gameboard.player2 = "yellow"
        self.gameboard.board = [[0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 'yellow', 0, 0, 0, 0],
                                [0, 0, 'red', 'red', 0, 0, 0]]
        self.gameboard.current_turn = 'p2'
        self.gameboard.remaining_moves = 39
        column_num = 3

        self.gameboard.update_board(column_num, self.gameboard.player2)
        expected_board = [[0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 'yellow', 0, 0, 0, 0],
                          [0, 0, 'yellow', 0, 0, 0, 0],
                          [0, 0, 'red', 'red', 0, 0, 0]]
        self.assertEqual(self.gameboard.board, expected_board) '''

if __name__ == '__main__':
    unittest.main()
