import unittest
import db


class Test_TestDb(unittest.TestCase):

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')

    def test_valid_add_move(self):
        # Checks a valid move was added to database
        db.init_db()

        board = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 'red', 0, 0, 0, 0]]
        board = str(board)
        move = ('p1', board, '', 'red', 'yellow', 40)

        db.add_move(move)

        db_last_move = db.getMove()
        actual_last_move = ('p1', board, '', 'red', 'yellow', 40)

        # Assert that tuple received is same as expected tuple
        self.assertTupleEqual(db_last_move, actual_last_move)
        db.clear()

    def test_invalid_getMove_empty(self):
        # Checks an invalid move - get move from an empty database

        db.init_db()
        move = db.getMove()

        # Assert that getMove() returns None when database is empty
        self.assertEqual(move, None)
        db.clear()

    def test_invalid_getMove_dne(self):
        # Checks an invalid move - get move from a database
        # that does not exist (dne)

        move = db.getMove()

        # Assert that getMove() returns None when database dne
        self.assertEqual(move, None)
