#!/usr/bin/env python3

import chess
import chess.pgn
import chess.svg

def load_database(filename):
    pgn_database = open("../data/lichess_db_standard_rated_2014-08.pgn")
    first_game = chess.pgn.read_game(pgn_database)
    board = chess.Board()
    board.push(chess.Move(chess.E2, chess.E4))
    print(board)
    # for move in list(first_game.mainline_moves()):
    #     board.push(move)
    #     print(board)
    #     print()



def parse_pgn(pgn_string):
    pass

if __name__ == '__main__':
    load_database('../data/lichess_db_standard_rated_2014-08.pgn')
