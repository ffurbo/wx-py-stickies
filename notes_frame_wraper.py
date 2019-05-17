"""
wrapper class for notes frame
"""

import wx
import wx.adv
import wx.xrc

from note_panel import NotePanel

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
        self.frame.Bind(wx.EVT_CLOSE, self.cb_close)

        self.tabs = wx.xrc.XRCCTRL(self.frame, 'm_notebook1')

        for note in self.category.notes:
            self.add_note_page(note)


    def cb_close(self, event):
        """ on close """
        self.frame.Show(False)

    def add_note_page(self, note):
        """ add new tab """
        panel = NotePanel(self.tabs)
        panel.load_note(note)
        self.note_panels.append(panel)
        self.tabs.AddPage(panel, "%d. %s" % (note.note_id, note.title), True)
