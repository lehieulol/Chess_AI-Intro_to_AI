from random import shuffle

import chess
import tensorflow as tf
from tensorflow import keras
import numpy as np


class Model:
    """
    Required methods:
    model_init, model_start, model_step, model_stop, model_message
    """

    def __init__(self):
        self.color = None
        self.board = chess.Board()
        self.discount = 0.99
        self.depth = 4

    deep_net = None

    @staticmethod
    def InitModel():
        inputs = [tf.keras.layers.Input(shape=(64,)),
                  tf.keras.layers.Input(shape=(4,))]
        castle = [tf.keras.layers.Dense(64, activation=tf.nn.leaky_relu)(inputs[1]), ]
        layers_num = 8
        hidden_board = []
        merge = []
        dropout = [inputs[0]]
        for _ in range(layers_num):
            merge.append(tf.keras.layers.Concatenate(axis=1)([dropout[-1], castle[-1]]))
            hidden_board.append(tf.keras.layers.Dense(64)(merge[-1]))
            dropout.append(tf.keras.layers.Dropout(0.2)(hidden_board[-1]))
            castle.append(tf.keras.layers.Dense())
        reduce = [tf.keras.layers.Dense(16)(dropout[-1])]
        reduce.append(tf.keras.layers.Dense(8)(reduce[0]))
        reduce.append(tf.keras.layers.Dense(1)(reduce[1]))

        Model.deep_net = tf.keras.models.Model(inputs=inputs, outputs=reduce[-1])
        print(Model.deep_net.summary())

    @staticmethod
    def Train(x,y):
        pass

    def model_init(self, model_info):
        """
        called once when the model is initiated
        :param model_info:
        {
        _
        }
        :return: void
        """
        if Model.deep_net is None:
            try:
                Model.deep_net = keras.models.load_model("Models/Monte_Carlo_Tree_Search/model_save")
            except:
                Model.InitModel()

    def model_start(self, inp):
        """
        called when decide who play as white
        :param inp:
        if 'b' or 'w': color you play with;
        else; return color you play with # skip this for most model except grading model
        :return:
        """
        self.board = chess.Board()
        if inp == 'w':
            self.color = 1
        else:
            self.color = -1

    def AlphaBeta(self, alpha, beta, depthleft, isMax):
        if depthleft == 0 or self.board.is_game_over():
            return self.ValueFunction(), None
        all_legal_move = list(self.board.generate_legal_moves())
        shuffle(all_legal_move)
        best_score = float('-inf') if isMax else float('inf')
        best_move = None
        for move in all_legal_move:
            self.board.push(move)
            child_score, child_move = self.AlphaBeta(alpha, beta, depthleft - 1, not isMax)
            child_score *= self.discount
            if depthleft == self.depth:
                print(self.color, 'move:', move, 'score:', child_score, 'current best move:', best_move,
                      'current best score:', best_score)
            self.board.pop()
            if isMax and best_score < child_score:
                best_score = child_score
                best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            elif (not isMax) and best_score > child_score:
                best_score = child_score
                best_move = move
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
        return best_score, best_move

    def PrepBoard(self):
        inputs = [[],
                  [self.board.has_kingside_castling_rights(chess.WHITE),
                   self.board.has_queenside_castling_rights(chess.WHITE),
                   self.board.has_kingside_castling_rights(chess.BLACK),
                   self.board.has_queenside_castling_rights(chess.BLACK)]]
        board = str(self.board)
        trans = {'.': 0,
                 '\n': None,
                 'Q': 9/9,
                 'K': 7/9,
                 'R': 5/9,
                 'B': 3.5/9,
                 'N': 3/9,
                 'P': 1/9,
                 'q': -9/9,
                 'k': -7/9,
                 'r': -5/9,
                 'b': -3.5/9,
                 'n': -3/9,
                 'p': -1/9}
        for i in board:
            if trans[i] is not None:
                inputs[0].append(trans[i])
        return inputs


    def ValueFunction(self):
        self.board.__str__().replace('.')
        return Model.deep_net()

    def model_step(self, move):
        """
        called after your opponent play a move
        :param move:
        if first to move: move = ''
        opponent move; format: san
        :return:
        your move
        """
        if move != '':
            before = self.PrepBoard()
            self.board.push_uci(move)
            Model.Train(before, self.ValueFunction()*self.discount)
        score, best_move = self.AlphaBeta(float('-inf'), float('inf'), self.depth, self.color == 1)
        best_move = best_move.uci()
        print(self.color, 'choose:', best_move, 'have score:', score)
        self.board.push_uci(best_move)
        return best_move

    def model_stop(self, move, result):
        """
        called when the match end
        :param move:
        opponent move, '' if the match end after your move
        :param result:
        -1/0/1 for black win/draw/white win
        :return:
        void
        """
        if move != '':
            before = self.PrepBoard()
            self.board.push_uci(move)
            Model.Train(before, self.ValueFunction()*self.discount)


    @staticmethod
    def model_message(inp):
        """
        used for debug
        :param inp:
        :return:
        """
        if inp == 'last batch is done':
            Model.deep_net.save("Models/Monte_Carlo_Tree_Search/model_save")


