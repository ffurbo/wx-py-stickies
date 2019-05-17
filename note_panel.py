"""
note panel widget
"""

#from io import BytesIO

import wx.adv
import wx.xrc
import wx
#import pycurl

class NotePanel(wx.Panel):
    """
    Panel for single note
    """

    def __init__(self, parent, note_id=0):
        wx.Panel.__init__(
            self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )

        self.note_id = note_id
        self.note = None

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
            wx.TE_MULTILINE|wx.TE_PROCESS_ENTER
        )
        sizer.Add(self.text, 1, wx.ALL|wx.EXPAND, 5)

        self.button = wx.Button(
            self, wx.ID_ANY, "Save %d" % (note_id+1), wx.DefaultPosition, wx.DefaultSize, 0
        )
        sizer.Add(self.button, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.button.Bind(wx.EVT_BUTTON, self.cb_save)
        self.text.Bind(wx.EVT_TEXT, self.cb_text)
        self.text.Bind(wx.EVT_TEXT_ENTER, self.cb_text_enter)
        self.text.Bind(wx.EVT_KILL_FOCUS, self.cb_loose_focus)
        #EVT_KILL_FOCUS

        self.SetSizer(sizer)
        self.Layout()


    def load_note(self, note):
        """ load data from Note object """
        self.text.SetValue(note.content)
        self.note_id = note.note_id
        self.note = note


    def cb_text(self, event):
        """ on type textarea """
        print("typing...")
        self.note.content = self.text.GetValue()

        #self.note.save_to_file()

    def cb_text_enter(self, event):
        """ on enter textarea """
        print("enter...")
        #self.note.content = self.text.GetValue()
        self.note.save_to_file()
        event.Skip(True)

    def cb_loose_focus(self, event):
        """ on loose focus """
        print("loosing focus now...")
        self.note.save_to_file()
        event.Skip(True)

    def cb_save(self, event):
        """ save data """

        self.note.save_to_file()

        # buffer = BytesIO()
        # curl = pycurl.Curl()
        # curl.setopt(pycurl.URL, "")
        # curl.setopt(pycurl.VERBOSE, True)
        # curl.setopt(pycurl.WRITEDATA, buffer)

        # curl.perform()
        # curl.close()

        # body = buffer.getvalue()
        # print(body.decode('utf-8'))
        # self.text.SetValue(body.decode('utf-8'))

        #self.Close(True)
