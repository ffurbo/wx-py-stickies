"""
Category notes frame
"""

import wx
import wx.adv
import wx.xrc

from note_panel import NotePanel
from notes_data import new_note
from my_frame import MyFrame


class NotesFrame(MyFrame):
    """
    notes category frame
    """

    def __init__(self, icon, category):
        MyFrame.__init__(
            self, None,
            id=wx.ID_ANY,
            title=category.name,
            #pos=self.load_window_position(), #wx.Point(100, 100),
            size=wx.Size(500, 300),
            style=0|wx.TAB_TRAVERSAL|wx.DEFAULT_FRAME_STYLE,
        )

        self.SetPosition(self.load_window_position())

        self.colour = wx.Colour(255, 255, 217)
        self.icon = icon
        self.category = category
        #self.note = NoteWindow(None, icon)

        self.frame = self
        self.tabs = None
        self.note_panels = []

        self.build_notes_frame()


    def build_notes_frame(self):
        """Build notes frame"""

        self.SetIcon(self.icon)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(self.colour)

        b_sizer_0 = wx.BoxSizer(wx.VERTICAL)
        self.tabs = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tabs.SetBackgroundColour(self.colour)

        b_sizer_0.Add(self.tabs, 1, wx.EXPAND |wx.ALL, 0)

        self.SetSizer(b_sizer_0)
        self.Layout()

        for note in self.category.notes:
            self.add_note_page(note)


        self.frame.Bind(wx.EVT_CLOSE, self.cb_close_event)


    def add_note_page(self, note):
        """ add new tab """
        panel = NotePanel(self)
        panel.load_note(note)
        self.note_panels.append(panel)
        self.tabs.AddPage(panel, "%s" % (note.title), True)


    def new_note_dialog(self):
        """ new note """
        try:
            dialog = wx.TextEntryDialog(self, "Enter title of new note", caption="New note")
            if dialog.ShowModal() == wx.ID_OK:
                title = dialog.GetValue()
                print('You entered: %s'%title)
                note = new_note(title, self.category)
                if note is not None:
                    self.category.add_note(note)
                    self.add_note_page(note)
            else:
                print('You entered nothing')
        finally:
            dialog.Destroy()

    def cb_close_event(self, event):
        """ on close """
        self.Show(False)
        #event.Skip(True)
