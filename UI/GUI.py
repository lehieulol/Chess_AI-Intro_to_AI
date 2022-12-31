import inspect
import random

import wx
import wx.svg

import chess
import chess.svg

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import parameter
from threading import Thread


class MMSS:
    def __init__(self, min, sec):
        self.sec = sec
        self.min = min

    def __str__(self):
        return "{:02d}:{:02d}".format(self.min, self.sec)

    def setTimer(self, minute, second):

        self.min = minute
        self.sec = second

    def countDown(self):
        if self.sec <= 0:
            if self.min == 0:
                return False
            self.sec = 59
            self.min -= 1
        else:
            self.sec -= 1
        return True


class Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Frame, self).__init__(parent, title=title, size=(parameter.WINDOW_WIDTH, parameter.WINDOW_HEIGHT))
        self.panel = Panel(self)

        # player_model init
        if True:
            self._1st_player_entry = None
            self._2nd_player_entry = None
            self.color_choice = None
            self.loop_num = None
            self.batch_size = None
            self.message = None
            self.chess_display = wx.StaticBitmap(self.panel)
            # self.board_panel = BoardPanel(self.panel)
            self.board_message = None
            self.running = False
            self._1st_model_timer = wx.StaticText(self.panel)
            self._2nd_model_timer = wx.StaticText(self.panel)

            self.timer = wx.Timer(self)
            self.counter = [MMSS(12, 0), MMSS(12, 0)]
            self.counting = [False, False]

            def _1(event):
                if self.counting[0]:
                    self.counter[0].countDown()
                self._1st_model_timer.SetLabel(str(self.counter[0]))
                if self.counting[1]:
                    self.counter[1].countDown()
                self._2nd_model_timer.SetLabel(str(self.counter[1]))

            self.Bind(wx.EVT_TIMER, _1, self.timer)
            self.timer.Start(1000)

        # Sizer
        self.InitUI()
        self.Centre()

    def InitUI(self):
        p = self.panel

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        if True:
            # main_sizer.Add(self.board_panel)
            main_sizer.Add(self.chess_display)

            png_board = wx.Image("temp.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            self.chess_display.SetBitmap(png_board)

            timer_box = wx.BoxSizer(wx.VERTICAL)
            font = wx.Font(40, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="",
                           encoding=wx.FONTENCODING_DEFAULT)
            self._1st_model_timer.SetFont(font)
            self._2nd_model_timer.SetFont(font)
            timer_box.Add(self._1st_model_timer)
            self._1st_model_timer.SetLabel("12:00")
            timer_box.AddSpacer(680)
            timer_box.Add(self._2nd_model_timer)
            self._2nd_model_timer.SetLabel("12:00")
            main_sizer.Add(timer_box)

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
                self.batch_size = wx.Choice(p, choices=['1', '5', '10', '50', '100'])
                self.batch_size.SetSelection(0)
                game_box.Add(self.batch_size)
                _ = wx.Button(p, label='Start')
                _.Bind(wx.EVT_BUTTON, self.ThreadStart)
                game_box.Add(_)

            control_box.Add(game_box)

            _ = wx.StaticText(p, label='Message: ')
            self.message = wx.StaticText(p)
            control_box.Add(_)
            control_box.Add(self.message)
            self.board_message = wx.StaticText(p)
            self.board_message.SetFont(
                wx.Font(20, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="",
                        encoding=wx.FONTENCODING_DEFAULT))
            control_box.Add(self.board_message)

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

    def ThreadStart(self, event):
        if self.running:
            self.message.SetLabel('Something is running, please waited before press \'Start\'')
            return
        thread_start = Thread(target=self.Start, args=(event,))
        thread_start.start()

    def Start(self, event):
        # get color_choice, loop_num, batch_size, _1st_model_module, _2nd_model_module
        try:
            # ['1st model play as white', '2nd model play as white', '2nd model choose color', 'UI choose model to play as white']
            color_choice = self.color_choice.GetSelection()
            loop_num = (1, 5, 10, 50, 100, 500, 1000)[self.loop_num.GetSelection()]
            batch_size = (1, 5, 10, 50, 100)[self.batch_size.GetSelection()]

            class ModelUnavailableException(Exception):
                pass

            from importlib.machinery import SourceFileLoader
            _ = self._1st_player_entry.GetValue()
            _1st_model_module = SourceFileLoader(_[_.rfind('\\') + 1:-3], _).load_module()
            _ = self._2nd_player_entry.GetValue()
            _2nd_model_module = SourceFileLoader(_[_.rfind('\\') + 1:-3], _).load_module()

            if 'Model' not in [cls_name for cls_name, class_obj in inspect.getmembers(_1st_model_module) if
                               inspect.isclass(class_obj)]:
                raise ModelUnavailableException()
            if 'Model' not in [cls_name for cls_name, class_obj in inspect.getmembers(_2nd_model_module) if
                               inspect.isclass(class_obj)]:
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

        self.running = True
        thread = []
        for _1 in range(batch_size):
            thread.append(Thread(target=self.GameStart,
                                 args=(_1st_model_module, _2nd_model_module, color_choice, loop_num, not _1,)))
            thread[_1].start()
        for _1 in range(batch_size):
            thread[_1].join()
        self.running = False
        self.timer.Stop()

    def GameStart(self, _1st_model_module, _2nd_model_module, color_choice, loop_num, display):
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
            ret = model[1].model_start('')
            if ret == 'w':
                model[0].model_start('b')
                first_player = 1
            else:
                model[0].model_start('w')
                first_player = 0
        elif color_choice == 3:
            ret = random.choice([['b', 'w', 1], ['w', 'b', 0]])
            model[0].model_start(ret[0])
            model[1].model_start(ret[1])
            first_player = 0

        if display:
            flipped = (first_player == 0)
            self.counter[0].setTimer(12, 0)
            self.counter[1].setTimer(12, 0)
        while True:
            last_move = ''
            try:
                last_move = board.peek().uci()
            except:
                pass
            outcome = board.outcome()
            if outcome is None:
                current_player = 0 if (board.turn == chess.WHITE and first_player == 0) else 1
                if display:
                    self.counting[current_player] = True
                board.push_uci(model[current_player].model_step(last_move))
                if display:
                    self.counting[current_player] = False
                    if str(self.counter[current_player]) == "00:00":
                        self.message.SetLabel("Player {%d} lose due to time up".format(current_player+1))
            else:
                outcome = 0 if outcome.winner is None else 1 if outcome.winner == chess.WHITE else -1
                model[0 if board.turn == chess.WHITE else 1].model_stop('', outcome)
                model[1 if board.turn == chess.WHITE else 0].model_stop(last_move, outcome)
                break
            if display:
                svg_board = chess.svg.board(
                    flipped=flipped,
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

                # self.board_message.SetLabel(str(board))
                # self.board_panel.SetImage(wx.svg.SVGimage.CreateFromFile("temp.svg"))
        if display:
            self.message.SetLabel(str(board.outcome()))

class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.frame = parent


class BoardPanel(wx.Panel):
    def __init__(self, parent):
        super(BoardPanel, self).__init__(parent, size=(parameter.BOARD_SIZE, parameter.BOARD_SIZE))
        self.img = wx.svg.SVGimage.CreateFromFile("temp.svg")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()

        dcdim = min(self.Size.width, self.Size.height)
        imgdim = min(self.img.width, self.img.height)
        scale = dcdim / imgdim
        width = int(self.img.width * scale)
        height = int(self.img.height * scale)

        ctx = wx.GraphicsContext.Create(dc)
        self.img.RenderToGC(ctx, scale)

    def SetImage(self, img):
        self.img = img
        self.Refresh()


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
