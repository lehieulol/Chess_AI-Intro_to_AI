import chess


class Model():

    def __init__(self):
        self.color = None
        self.board = chess.Board()

    def model_init(self, model_info):
        """
        called once when the model is initiated
        :param model_info:
        {
        _
        }
        :return: void
        """
        return

    def model_start(self, inp):
        self.board = chess.Board()
        print('model_start')
        print(inp)
        """
        called when decide who play as white
        :param inp:
        if 'b' or 'w': color you play with;
        else; return color you play with # skip this for most model except grading model
        :return:
        """
        if inp == '':
            return input('Choose your color: ')

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
        while True:
            try:
                inp = input('Enter your move in uci format: ')
                print(inp)
                self.board.push_uci(inp)
                break
            except:
                print('Invalid input')
        return inp

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
        return

    def model_message(self, inp):
        """
        used for debug
        :param inp:
        :return:
        """
        return
