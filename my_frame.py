""" extended frame """

import json
import time
import wx

class MyFrame(wx.Frame):
    """
    main extended frame
    """

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        self.timer_handler = wx.EvtHandler()
        #self.move_timer = wx.Timer(self)
        self.move_timer = wx.Timer(self.timer_handler)

        self.Bind(wx.EVT_MOVE, self.cb_move)

        #self.Bind(wx.EVT_TIMER, self.cb_move_timer_event)
        self.timer_handler.Bind(wx.EVT_TIMER, self.cb_move_timer_event)

        # self.panel0 = None
        # self.sizer1 = None

    def cb_move(self, event):
        """ call back for frame move """

        if not self.move_timer.IsRunning():
            self.move_timer.StartOnce(2000)

        #print(time.time_ns())
        print(int(time.time()))


    def cb_move_timer_event(self, event):
        """ timer test """
        self.save_window_position(self.GetPosition().Get())


    def save_window_position(self, position):
        """ save position tuple to file """
        str_position = json.dumps(position)
        file_name = 'data/%s_window_position.json'%self.GetLabel()

        try:
            file = open(file_name, 'w')
            file.write(str_position)
        except OSError as err:
            print("can't save window position: {0}".format(err))
        else:
            file.close()
            print("position saved")


    def load_window_position(self):
        """ load window position from file """
        file_name = 'data/%s_window_position.json'%self.GetLabel()

        try:
            file = open(file_name, 'r')
            str_position = file.read()
        except OSError as err:
            print("can't load window position: {0}".format(err))
            return wx.DefaultPosition
        else:
            file.close()
            print("position loaded")
            position = tuple(json.loads(str_position))
            return wx.Point(*position)


    def toggle(self):
        """Toggle frame"""
        if self.IsShown():
            self.Show(False)
        else:
            self.Show(True)


    # def generate_starter(self):
    #     """ base from for loading xrc """
    #     sizer0 = wx.BoxSizer(wx.VERTICAL)
    #     self.panel0 = wx.Panel(
    #         self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
    #     )
    #     self.sizer1 = wx.BoxSizer(wx.VERTICAL)

    #     self.panel0.SetSizer(self.sizer1)
    #     self.panel0.Layout()
    #     self.sizer1.Fit(self.panel0)
    #     sizer0.Add(self.panel0, 1, wx.EXPAND |wx.ALL, 0)

    #     self.SetSizer(sizer0)
    #     self.Layout()

    #     self.Centre(wx.BOTH)

    # def get_sizer(self):
    #     """ get out sizer"""
    #     if self.sizer1 is not None:
    #         return self.sizer1

    #     return False
