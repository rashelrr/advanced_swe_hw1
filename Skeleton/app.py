from flask import Flask, render_template, request, redirect, jsonify, make_response
from json import dumps
from Gameboard import Gameboard
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    db.clear()
    db.init_db()
    game.__init__()  # resets gameboard values
    return render_template('player1_connect.html', status='Pick a Color.')


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    move = db.getMove()
    if move is None:
        game.player1 = request.args.get('color')
    else:
        game.continue_game_with_last_move(move)

    return render_template('player1_connect.html', status=game.player1)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    move = db.getMove()
    if move is None:
        game.set_p2_color()
    else:
        game.continue_game_with_last_move(move)

    return render_template('p2Join.html', status=game.player2)


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move

'''


@app.route('/move1', methods=['POST'])
def p1_move():
    if game.check_p1_picked_color() is False:  # check if color selected
        return jsonify(move=game.board, invalid=True,
                       reason="P1 must pick a color.", winner=game.game_result)
    elif game.check_if_draw() is True:
        return jsonify(move=game.board, invalid=True, reason="Tie. No winner.",
                       winner=game.game_result)
    else:
        attempted_move = request.get_json()
        column = attempted_move['column']
        column_num = int(column[-1])

        # check if move is valid
        if game.check_current_turn('p1') is False:
            return jsonify(move=game.board, invalid=True,
                           reason="Not your turn. Please wait your turn.",
                           winner=game.game_result)
        elif game.check_filled_column(column_num) is False:
            return jsonify(move=game.board, invalid=True,
                           reason="Column is filled. Choose another column.",
                           winner=game.game_result)
        else:
            # update board with move
            can_update_board = game.update_board(column_num, game.player1)

            if can_update_board is True:
                game.check_if_win(game.player1)

                game.update_remaining_moves()
                move = (game.current_turn, dumps(game.board), game.game_result,
                        game.player1, game.player2, game.remaining_moves)
                db.add_move(move)
                game.update_current_turn()

                return jsonify(move=game.board, invalid=False,
                               winner=game.game_result)
            else:
                return jsonify(move=game.board, invalid=True,
                               reason="End of game.", winner=game.game_result)


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    if game.check_p1_picked_color() is False:  # check if color selected
        return jsonify(move=game.board, invalid=True,
                       reason="P1 must pick a color.", winner=game.game_result)
    elif game.check_if_draw() is True:
        return jsonify(move=game.board, invalid=True, reason="Tie. No winner.",
                       winner=game.game_result)
    else:
        attempted_move = request.get_json()
        column = attempted_move['column']
        column_num = int(column[-1])

        # check if move is valid
        if game.check_current_turn('p2') is False:
            return jsonify(move=game.board, invalid=True,
                           reason="Not your turn. Please wait your turn.",
                           winner=game.game_result)
        elif game.check_filled_column(column_num) is False:
            return jsonify(move=game.board, invalid=True,
                           reason="Column is filled. Choose another column.",
                           winner=game.game_result)
        else:
            # update board with move
            can_update_board = game.update_board(column_num, game.player2)

            if can_update_board is True:
                game.check_if_win(game.player2)

                game.update_remaining_moves()
                move = (game.current_turn, dumps(game.board), game.game_result,
                        game.player1, game.player2, game.remaining_moves)
                db.add_move(move)
                game.update_current_turn()

                return jsonify(move=game.board, invalid=False,
                               winner=game.game_result)
            else:
                return jsonify(move=game.board, invalid=True,
                               reason="End of game.", winner=game.game_result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
