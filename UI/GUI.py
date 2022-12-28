import inspect
import random

import wx
import wx.svg

import chess
import chess.svg

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import parameter


class Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Frame, self).__init__(parent, title=title, size=(parameter.WINDOW_WIDTH, parameter.WINDOW_HEIGHT))
        self.panel = Panel(self)

        # player_model init
        if True:
            self._1st_player_entry = None
            self._2nd_player_entry = None
            self.chess_display = None
            self.color_choice = None
            self.loop_num = None
            self.batch_size = None
            self.message = None

        # Sizer
        self.InitUI()
        self.Centre()

    def InitUI(self):
        p = self.panel

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        if True:
            board_png = wx.Image("UI/board.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            self.chess_display = wx.StaticBitmap(p, bitmap=board_png)
            main_sizer.Add(self.chess_display)

            control_box = wx.BoxSizer(wx.VERTICAL)
            _ = wx.StaticText(p, label="CHESS UI by lichtut:)")
            control_box.Add(_, 0, wx.CENTER, 1)

            model_1_box = wx.BoxSizer(wx.HORIZONTAL)
            if True:
                _ = wx.StaticText(p, label='1st player\'s model:     ')
                model_1_box.Add(_)
                self._1st_player_entry = wx.TextCtrl(p, size=(400, 23))
                model_1_box.Add(self._1st_player_entry)
                _ = wx.Button(p, label='Find file')
                _.Bind(wx.EVT_BUTTON,
                       lambda x:
                       self.set_1st_player_script(
                           self.OpenFile(x, title="Choose 1st player's model", filetype="Python 2 script|*.py")))
                model_1_box.Add(_)
                control_box.Add(model_1_box)

            model_2_box = wx.BoxSizer(wx.HORIZONTAL)
            if True:
                _ = wx.StaticText(p, label='2nd player\'s model:   ')
                model_2_box.Add(_)
                self._2nd_player_entry = wx.TextCtrl(p, size=(400, 23))
                model_2_box.Add(self._2nd_player_entry)
                _ = wx.Button(p, label='Find file')
                _.Bind(wx.EVT_BUTTON,
                       lambda x:
                       self.set_2nd_player_script(
                           self.OpenFile(x, title="Choose 2nd player's model", filetype="Python 2 script|*.py"))
                       )
                model_2_box.Add(_)
                control_box.Add(model_2_box)

            game_box = wx.BoxSizer(wx.HORIZONTAL)
            if True:
                _ = wx.StaticText(p, label='Player play as White: ')
                game_box.Add(_)
                self.color_choice = wx.Choice(p, choices=['1st model play as white', '2nd model play as white',
                                                          '1st model choose color', 'UI choose model to play as white'])
                self.color_choice.SetSelection(0)
                game_box.Add(self.color_choice)
                _ = wx.StaticText(p, label='Number of loop: ')
                game_box.Add(_)
                self.loop_num = wx.Choice(p, choices=['1', '5', '10', '50', '100', '500', '1000'])
                self.loop_num.SetSelection(0)
                game_box.Add(self.loop_num)
                _ = wx.StaticText(p, label=' x ')
                game_box.Add(_)
                self.batch_size = wx.Choice(p, choices=['1', '5', '10', '50', '100', '500', '1000'])
                self.batch_size.SetSelection(0)
                game_box.Add(self.batch_size)
                _ = wx.Button(p, label='Start')
                _.Bind(wx.EVT_BUTTON, self.Start)
                game_box.Add(_)

            control_box.Add(game_box)

            _ = wx.StaticText(p, label='Message: ')
            self.message = wx.StaticText(p)
            control_box.Add(_)
            control_box.Add(self.message)

            main_sizer.Add(control_box)
            p.SetSizer(main_sizer)

    def OpenFile(self, event, title="", filetype=""):
        fd = wx.FileDialog(self, title, wildcard=filetype)
        if fd.ShowModal() == wx.ID_OK:
            ret = fd.GetPath()
            fd.Destroy()
            return ret
        fd.Destroy()
        return None

    def set_1st_player_script(self, path):
        self._1st_player_entry.SetValue(path)

    def set_2nd_player_script(self, path):
        self._2nd_player_entry.SetValue(path)

    def Start(self, event):

        # ['1st model play as white', '2nd model play as white', '1st model choose color', 'UI choose model to play as white']
        color_choice = self.color_choice.GetSelection()
        loop_num = (1, 5, 10, 50, 100, 500, 1000)[self.loop_num.GetSelection()]
        batch_size = (1, 5, 10, 50, 100, 500, 1000)[self.batch_size.GetSelection()]

        class ModelUnavailableException(Exception):
            pass

        try:
            from importlib.machinery import SourceFileLoader
            _ = self._1st_player_entry.GetValue()
            _1st_model_module = SourceFileLoader(_[_.rfind('\\') + 1:-3], _).load_module()
            _ = self._2nd_player_entry.GetValue()
            _2nd_model_module = SourceFileLoader(_[_.rfind('\\') + 1:-3], _).load_module()

            if 'Model' not in [cls_name for cls_name, class_obj in inspect.getmembers(_1st_model_module) if inspect.isclass(class_obj)]:
                raise ModelUnavailableException()
            if 'Model' not in [cls_name for cls_name, class_obj in inspect.getmembers(_2nd_model_module) if inspect.isclass(class_obj)]:
                raise ModelUnavailableException()
        except ModelUnavailableException:
            self.message.SetLabel('Failed to find model')
            return
        except FileNotFoundError:
            self.message.SetLabel('Failed to find module')
            return
        except ImportError:
            self.message.SetLabel('Import Error')
            return

        for _1 in range(batch_size):
            pass

        for _1 in range(loop_num):
            for _2 in range(batch_size):
                board = chess.Board()
                model = [_1st_model_module.Model(), _2nd_model_module.Model()]

                model[0].model_init(None)
                model[1].model_init(None)
                first_player = None
                if color_choice == 0:
                    model[0].model_start('w')
                    model[1].model_start('b')
                    first_player = 0
                elif color_choice == 1:
                    model[0].model_start('b')
                    model[1].model_start('w')
                    first_player = 1
                elif color_choice == 2:
                    ret = model[0].model_start('')
                    if ret == 'w':
                        model[1].model_start('b')
                        first_player = 0
                    else:
                        model[1].model_start('w')
                        first_player = 1
                elif color_choice == 3:
                    ret = random.choice([['b', 'w', 1], ['w', 'b', 0]])
                    model[0].model_start(ret[0])
                    model[1].model_start(ret[1])
                    first_player = 0

                while True:
                    last_move = ''
                    try:
                        last_move = board.peek().uci()
                    except:
                        pass
                    outcome = board.outcome()
                    if outcome is None:
                        board.push_uci(model[0 if board.turn == chess.WHITE else 1].model_step(last_move))
                    else:
                        outcome = 0 if outcome.winner is None else 1 if outcome.winner == chess.WHITE else -1
                        model[0 if board.turn == chess.WHITE else 1].model_stop('', outcome)
                        model[1 if board.turn == chess.WHITE else 0].model_stop(last_move, outcome)
                        break
                    print(board)
                    svg_board = chess.svg.board(
                        board=board,
                        size=parameter.BOARD_SIZE
                    )
                    f = open("temp.svg", "w")
                    f.write(svg_board)
                    f.close()

                    rlg_board = svg2rlg("temp.svg")
                    renderPM.drawToFile(rlg_board, "temp.png", fmt="png")

                    png_board = wx.Image("temp.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                    self.chess_display.SetBitmap(png_board)
                self.message.SetLabel(str(board.outcome()))


class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent)
        self.frame = parent


class App(wx.App):
    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        self.frame = None

    def OnInit(self):
        self.frame = Frame(parent=None, title='Chess GUI by Lichtut')
        self.frame.Show()
        return True


test = App()
test.MainLoop()
