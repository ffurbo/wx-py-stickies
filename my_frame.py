""" extended frame """

import wx

class MyFrame(wx.Frame):
    """
    main extended frame
    """

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

    def toggle(self):
        """Toggle frame"""
        if self.IsShown():
            self.Show(False)
        else:
            self.Show(True)
