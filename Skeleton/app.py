from flask import Flask, render_template, request, redirect, jsonify, make_response
from json import dump
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
    return render_template('player1_connect.html', status = 'Pick a Color.')


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
    p1_color = request.args.get('color')
    game.player1 = p1_color
    return render_template('player1_connect.html', status = p1_color)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():

    if game.player1 == "red":
        p2_color = "yellow"
    elif game.player1 == "yellow":
        p2_color = "red"
    else:
        p2_color = "Error"
        
    game.player2 = p2_color
    return render_template('p2Join.html', status = p2_color)
    


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
    # check if color has been selected, check if draw (remaining_moves is 0)
    if game.player1 == "":
        return jsonify(move=game.board, invalid = True, reason = "Player 1 must pick a color.", winner = game.game_result)
    elif game.remaining_moves == 0:
        return jsonify(move=game.board, invalid = True, reason = "End of game.", winner = game.game_result)
    else:
        attempted_move = request.get_json()
        column = attempted_move['column']
        column_num = int(column[-1])

        # check if move is valid
        valid_current_turn = game.check_current_turn('p1')
        valid_column = game.check_filled_column(column_num)

        if valid_current_turn is False:        
            return jsonify(move=game.board, invalid = True, reason = "Not your turn. Please wait your turn.", winner = game.game_result)
        elif valid_column is False:
            return jsonify(move=game.board, invalid = True, reason = "Column is filled. Please choose a different column.", winner = game.game_result)
        
        # update board with move
        game.update_board(column_num, game.player1)        

        '''
        # print board (debugging)
        print("the game board: ")
        for row in range(6):
            print(game.board[row])
        '''
        
        # check if won
        has_won = game.check_if_win(game.player1)   
        game.continue_game('p2')

        if has_won:
            game.remaining_moves = 0

        return jsonify(move=game.board, invalid = False, winner=game.game_result)  


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    # check if draw (remaining_moves is 0)
    if game.remaining_moves == 0:
        return jsonify(move=game.board, invalid = True, reason = "End of game.", winner = game.game_result)
    else: 
        attempted_move = request.get_json()
        column = attempted_move['column']
        column_num = int(column[-1])

        # check if move is valid
        valid_current_turn = game.check_current_turn('p2')
        valid_column = game.check_filled_column(column_num)

        if valid_current_turn is False:        
            return jsonify(move=game.board, invalid = True, reason = "Not your turn. Please wait your turn.", winner = game.game_result)
        elif valid_column is False:
            return jsonify(move=game.board, invalid = True, reason = "Column is filled. Please choose a different column.", winner = game.game_result)
      
        # update board with move
        game.update_board(column_num, game.player2)                    

        '''# print board (debugging)
        print("the game board: ")
        for row in range(6):
            print(game.board[row])
        '''

        # check if won
        has_won = game.check_if_win(game.player2)
        game.continue_game('p1')

        if has_won:
            game.remaining_moves = 0

        return jsonify(move=game.board, invalid = False, winner=game.game_result)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
