""" extended frame """

import wx

class MyFrame(wx.Frame):
    """
    main extended frame
    """

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.panel0 = None
        self.sizer1 = None

    def toggle(self):
        """Toggle frame"""
        if self.IsShown():
            self.Show(False)
        else:
            self.Show(True)

    def generate_starter(self):
        """ base from for loading xrc """
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        self.panel0 = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)

        self.panel0.SetSizer(self.sizer1)
        self.panel0.Layout()
        self.sizer1.Fit(self.panel0)
        sizer0.Add(self.panel0, 1, wx.EXPAND |wx.ALL, 0)

        self.SetSizer(sizer0)
        self.Layout()

        self.Centre(wx.BOTH)

    def get_sizer(self):
        """ get out sizer"""
        if self.sizer1 is not None:
            return self.sizer1

        return False
