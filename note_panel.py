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

    def __init__(self, notes_wraper):
        wx.Panel.__init__(
            self, notes_wraper.tabs, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )

        self.notes_wraper = notes_wraper
        self.note_id = ""
        self.note = None
        self.modified = False

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
            wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.BORDER_NONE
        )
        self.text.SetBackgroundColour(notes_wraper.colour)
        self.text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL, False, "Roboto Mono"))

        sizer.Add(self.text, 1, wx.ALL|wx.EXPAND, 10)

        # sizer_btns = wx.BoxSizer(wx.HORIZONTAL)

        # self.button_save = wx.Button(self, wx.ID_ANY, "Save", wx.DefaultPosition, wx.DefaultSize, 0)
        # sizer_btns.Add(self.button_save, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        # self.button_new = wx.Button(self, wx.ID_ANY, "New", wx.DefaultPosition, wx.DefaultSize, 0)
        # sizer_btns.Add(self.button_new, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        # sizer.Add(sizer_btns, 0, wx.ALIGN_RIGHT, 5)

        # self.button_save.Bind(wx.EVT_BUTTON, self.cb_save_btn)
        # self.button_new.Bind(wx.EVT_BUTTON, self.cb_new)

        self.text.Bind(wx.EVT_TEXT, self.cb_text)
        self.text.Bind(wx.EVT_TEXT_ENTER, self.cb_text_enter)
        self.text.Bind(wx.EVT_KILL_FOCUS, self.cb_loose_focus)
        #EVT_KILL_FOCUS EVT_SET_FOCUS

        self.SetSizer(sizer)
        self.Layout()


    def load_note(self, note):
        """ load data from Note object """
        #self.text.SetValue(note.content)
        self.text.ChangeValue(note.content) # does not generate EVT_TEXT event
        self.note_id = note.note_id
        self.note = note


    def cb_text(self, event):
        """ on type textarea """
        print("typing...")
        self.note.content = self.text.GetValue()
        self.modified = True


    def cb_text_enter(self, event):
        """ on enter textarea """
        print("enter...")
        self.save_data()
        event.Skip(True)

    def cb_loose_focus(self, event):
        """ on loose focus """
        print("%s killing focus now..."%self.note.title)
        self.save_data()
        event.Skip(True)

    def cb_save_btn(self, event):
        """ save data button """
        self.save_data()


    def save_data(self):
        """ save data"""
        if self.modified:
            self.note.save_to_file()


    def cb_new(self, event):
        """ new note """
        self.notes_wraper.new_note_dialog()

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
