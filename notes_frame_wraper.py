"""
wrapper class for notes frame
"""

import wx
import wx.adv
import wx.xrc

from note_panel import NotePanel
from notes_data import new_note

class NotesFrameWrapper():
    """ wrapper """

    def __init__(self, icon, category):

        self.icon = icon
        self.category = category
        #self.note = NoteWindow(None, icon)

        self.res = None
        self.frame = None
        self.tabs = None
        self.note_panels = []

        self.build_notes_frame()


    def build_notes_frame(self):
        """Build notes frame"""

        self.res = wx.xrc.XmlResource('NotesFrame.xml')
        self.frame = self.res.LoadFrame(None, 'NotesFrame')
        self.frame.SetIcon(self.icon)
        self.frame.SetTitle(self.category.name)
        self.frame.Bind(wx.EVT_CLOSE, self.cb_close_event)

        self.tabs = wx.xrc.XRCCTRL(self.frame, 'm_notebook1')

        for note in self.category.notes:
            self.add_note_page(note)


    def cb_close_event(self, event):
        """ on close """
        self.frame.Show(False)
        #event.Skip(True)


    def add_note_page(self, note):
        """ add new tab """
        panel = NotePanel(self)
        panel.load_note(note)
        self.note_panels.append(panel)
        self.tabs.AddPage(panel, "%s" % (note.title), True)


    def new_note_dialog(self, event=None):
        """ new note """
        try:
            dialog = wx.TextEntryDialog(self.frame, "Enter title of new note", caption="New note")
            if dialog.ShowModal() == wx.ID_OK:
                title = dialog.GetValue()
                print('You entered: %s'%title)
                note = new_note(title)
                if note is not None:
                    self.category.add_note(note)
                    self.add_note_page(note)
            else:
                print('You entered nothing')
        finally:
            dialog.Destroy()
