import chess

class Model():
    """
    Required methods:
    model_init, model_start, model_step, model_stop, model_message
    """

    def __init__(self):
        self.color = None
        self.board = chess.Board()
        self.para = 0.99
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
        if self.color == 1:
            best_move = self.AlphaBetaMax(-100000000, 100000000, self.depth)['move']
        else:
            best_move = self.AlphaBetaMin(-100000000, 100000000, self.depth)['move']
        self.board.push_uci(best_move)
        return best_move

    def AlphaBetaMin(self, alpha, beta, depthleft):
        if depthleft == 0:
            return {'value': -self.ValueFunction(), 'move': None}
        all_legal_move = list(self.board.generate_legal_moves())
        best_move = None
        for move in all_legal_move:
            self.board.push(move)
            score = self.AlphaBetaMax(alpha, beta, depthleft - 1)['value']
            self.board.pop()
            if score <= alpha:
                return {'value': alpha, 'move': best_move}
            if score < beta:
                beta = score
                best_move = move.uci()
        return {'value': beta, 'move': best_move}

    def AlphaBetaMax(self, alpha, beta, depthleft):
        if depthleft == 0:
            return {'value': self.ValueFunction(), 'move': None}
        all_legal_move = list(self.board.generate_legal_moves())
        best_move = None
        for move in all_legal_move:
            self.board.push(move)
            score = self.AlphaBetaMin(alpha, beta, depthleft - 1)['value']
            self.board.pop()
            if score >= beta:
                return {'value': beta, 'move': best_move}
            if score > alpha:
                alpha = score
                best_move = move.uci()
        return {'value': alpha, 'move': best_move}

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

    def model_message(self, inp):
        """
        used for debug
        :param inp:
        :return:
        """
        pass

    def ValueFunction(self):
        if self.board.outcome() is not None:
            winner = 0 if self.board.outcome() is None else 1 if self.board.outcome() == chess.WHITE else -1
            return winner * 1000000
        else:
            fen = self.board.board_fen()
            fen = fen
            val = {'Q': 9,
                   'R': 3.5,
                   'B': 3.2,
                   'N': 3,
                   'P': 1,
                   'q': -9,
                   'r': -3.5,
                   'b': -3.2,
                   'n': -3,
                   'p': -1}
            value = 0
            for i in fen:
                value += val[i] if i in val else 0
            return float(value)
