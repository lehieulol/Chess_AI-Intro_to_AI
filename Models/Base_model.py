from abc import ABCMeta, abstractmethod


class BaseModel:
    """
    Required methods:
    model_init, model_start, model_step, model_stop, model_message
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        print("pass")

    @abstractmethod
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

    @abstractmethod
    def model_start(self, inp):
        """
        called when decide who play as white
        :param inp:
        if 'b' or 'w': color you play with;
        else; return color you play with # skip this for most model except grading model
        :return:
        """
        pass

    @abstractmethod
    def model_step(self, move):
        """
        called after your opponent play a move
        :param move:
        if first to move: move = ''
        opponent move; format: san
        :return:
        your move
        """
        pass

    @abstractmethod
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

    @abstractmethod
    def model_message(self, input):
        """
        used for debug
        :param input:
        :return:
        """
        pass
