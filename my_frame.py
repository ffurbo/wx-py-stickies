""" extended frame """

import json
import wx

class MyFrame(wx.Frame):
    """
    main extended frame
    """

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        self.move_timer_handler = wx.EvtHandler()
        self.size_timer_handler = wx.EvtHandler()
        self.move_timer = wx.Timer(self.move_timer_handler)
        self.size_timer = wx.Timer(self.size_timer_handler)
        self.Bind(wx.EVT_MOVE, self.cb_move)
        self.Bind(wx.EVT_SIZE, self.cb_size)
        self.move_timer_handler.Bind(wx.EVT_TIMER, self.cb_move_timer_event)
        self.size_timer_handler.Bind(wx.EVT_TIMER, self.cb_size_timer_event)

        self.cfg_file_name = 'data/%s_window_cfg.json'%(self.GetLabel())

        cfg = self.load_config()
        if cfg is not None:
            self.cfg = cfg
        else:
            self.cfg = {
                "position": [100, 100],
                "size": [500, 300],
                "pinned": 0
            }
            self.save_config()

        self.pinned = bool(self.cfg["pinned"])


    def get_config(self):
        """ get current config dict """
        result = {
            "position": self.GetPosition().Get(),
            "size": self.GetSize().Get(),
            "pinned": True
        }
        return result


    def save_config(self):
        """ save config to file """
        data = json.dumps(self.cfg)

        try:
            file = open(self.cfg_file_name, 'w')
            file.write(data)
        except OSError as err:
            print("can't save property: {0}".format(err))
        else:
            file.close()

    def load_config(self):
        """ load config from file """

        try:
            file = open(self.cfg_file_name, 'r')
            str_data = file.read()
        except OSError as err:
            print("can't load property: {0}".format(err))
            return None  #wx.DefaultPosition
        else:
            file.close()
            #print("position loaded")
            data = json.loads(str_data)
            return data #wx.Point(*position)


    def cb_move(self, event):
        """ call back for frame move """
        if not self.move_timer.IsRunning():
            self.move_timer.StartOnce(2000)

    def cb_size(self, event):
        """ call back for frame resize """
        if not self.size_timer.IsRunning():
            self.size_timer.StartOnce(2000)
        event.Skip(True)

    def cb_move_timer_event(self, event):
        """ move debounced action """
        self.save_window_position(self.GetPosition().Get())

    def cb_size_timer_event(self, event):
        """ resize debounced action """
        print("Window resized...")
        self.save_window_size(self.GetSize().Get())

        #self.save_window_position(self.GetPosition().Get())

    def save_window_position(self, position):
        """ save window position """
        #self.save_xy(position, 'window_position')
        self.cfg["position"] = position
        self.save_config()

    def save_window_size(self, size):
        """ save window position """
        #self.save_xy(size, 'window_size')
        self.cfg["size"] = size
        self.save_config()

    def load_window_position(self):
        """ load window position """

        self.load_config()
        return self.cfg['position']

        # xy = self.load_xy('window_position')
        # if xy is not None:
        #     return wx.Point(*xy)
        # else:
        #     return wx.DefaultPosition

    def load_window_size(self):
        """ load window position """

        self.load_config()
        return self.cfg['size']

        # xy = self.load_xy('window_size')
        # if xy is not None:
        #     return wx.Size(*xy)
        # else:
        #     return wx.Size(500, 300)


    def save_xy(self, position, prop):
        """ save xy tuple to file """
        str_position = json.dumps(position)
        file_name = 'data/%s_%s.json'%(self.GetLabel(), prop)

        try:
            file = open(file_name, 'w')
            file.write(str_position)
        except OSError as err:
            print("can't save property: {0}".format(err))
        else:
            file.close()
            #print("position saved")

    def load_xy(self, prop):
        """ load xy from file """
        file_name = 'data/%s_%s.json'%(self.GetLabel(), prop)

        try:
            file = open(file_name, 'r')
            str_position = file.read()
        except OSError as err:
            print("can't load property: {0}".format(err))
            return None  #wx.DefaultPosition
        else:
            file.close()
            #print("position loaded")
            position = tuple(json.loads(str_position))
            return position #wx.Point(*position)


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
