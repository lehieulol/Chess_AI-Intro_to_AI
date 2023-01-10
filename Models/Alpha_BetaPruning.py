import chess
from random import shuffle
from UI import parameter

class Model():
    """
    Required methods:
    model_init, model_start, model_step, model_stop, model_message
    """

    def __init__(self):
        self.color = None
        self.board = chess.Board()
        self.discount = 0.99
        self.depth = 5

    def model_init(self, model_info):
        """
        called once when the model is initiated
        :param model_info:
        {
        _
        }
        :return: void
        """
        pass

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
            self.board.push_uci(move)
        score, best_move = self.AlphaBeta(float('-inf'), float('inf'), self.depth, self.color == 1)
        best_move = best_move.uci()
        print(self.color, 'choose:', best_move, 'have score:', score)
        self.board.push_uci(best_move)
        return best_move

    def AlphaBeta(self, alpha, beta, depthleft, isMax):
        if depthleft == 0 or self.board.is_game_over():
            return self.ValueFunction(), None
        all_legal_move = list(self.board.generate_legal_moves())
        shuffle(all_legal_move)
        best_score = float('-inf') if isMax else float('inf')
        best_move = None
        for move in all_legal_move:
            self.board.push(move)
            child_score, child_move = self.AlphaBeta(alpha, beta, depthleft-1, not isMax)
            child_score *= self.discount
            if depthleft == self.depth:
                print(self.color, 'move:', move, 'score:', child_score, 'current best move:', best_move, 'current best score:', best_score)
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
        pass

    @staticmethod
    def model_message(inp):
        """
        used for debug
        :param inp:
        :return:
        """
        pass

    def ValueFunction(self):
        if self.board.is_game_over():
            winner = 0 if self.board.outcome().winner is None else 1 if self.board.outcome().winner == chess.WHITE else -1
            return winner * 1000000
        else:
            fen = self.board.board_fen()
            fen = fen
            val = {'Q': 9,
                   'R': 5,
                   'B': 3.2,
                   'N': 3,
                   'P': 1,
                   'q': -9,
                   'r': -5,
                   'b': -3.2,
                   'n': -3,
                   'p': -1}
            value = 0
            for i in fen:
                value += val[i] if i in val else 0
            return float(value)
