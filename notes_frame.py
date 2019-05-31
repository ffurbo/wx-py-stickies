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

    def __init__(self, res, category):
        MyFrame.__init__(
            self, None,
            id=wx.ID_ANY,
            title=category.name,
            #pos=self.load_window_position(), #wx.Point(100, 100),
            #size=wx.Size(500, 300),
            style=0|wx.TAB_TRAVERSAL|wx.DEFAULT_FRAME_STYLE|wx.FRAME_NO_TASKBAR,
        )

        self.SetPosition(self.load_window_position())
        self.SetSize(self.load_window_size())

        self.colour = wx.Colour(*res.cfg["note_color"])
        #self.icon = icon
        self.category = category
        #self.note = NoteWindow(None, icon)

        self.res = res
        self.frame = self
        self.tabs = None
        self.note_panels = []
        self.current_panel = None

        self.build_notes_frame()


    def build_notes_frame(self):
        """Build notes frame"""

        self.SetIcon(self.res.icon)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(self.colour)

        b_sizer_0 = wx.BoxSizer(wx.VERTICAL)
        self.tabs = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tabs.SetBackgroundColour(self.colour)

        b_sizer_0.Add(self.tabs, 1, wx.EXPAND |wx.ALL, 0)

        b_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.bottom_btn_1 = wx.Button(self, wx.ID_ANY, "Save", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer_1.Add(self.bottom_btn_1, 0, wx.ALL, 5)

        self.bottom_btn_2 = wx.Button(self, wx.ID_ANY, "New", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer_1.Add(self.bottom_btn_2, 0, wx.ALL, 5)

        self.pin_btn = wx.ToggleButton(self, wx.ID_ANY, "Pin", wx.DefaultPosition, wx.DefaultSize, 0)
        self.pin_btn.SetValue(self.pinned)
        b_sizer_1.Add(self.pin_btn, 0, wx.ALL, 5)

        b_sizer_0.Add(b_sizer_1, 0, wx.ALIGN_RIGHT, 10)

        self.SetSizer(b_sizer_0)
        self.Layout()

        for note in self.category.notes:
            self.add_note_page(note)

        self.Bind(wx.EVT_CLOSE, self.cb_close_event)
        self.tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.cb_change_page)
        self.bottom_btn_1.Bind(wx.EVT_BUTTON, self.cb_save)
        self.bottom_btn_2.Bind(wx.EVT_BUTTON, self.cb_new)
        self.pin_btn.Bind(wx.EVT_TOGGLEBUTTON, self.cb_pin_toggle)

    def cb_pin_toggle(self, event):
        """ pin or unpin frame """
        self.pinned = event.IsChecked()
        print(self.pinned)
        self.cfg["pinned"] = int(self.pinned)
        self.save_config()

    def cb_save(self, event):
        """ save current note """

    def cb_new(self, event):
        """ new note """
        self.new_note_dialog()

    def cb_change_page(self, event):
        """ change page event """
        if self.tabs:
            self.current_panel = self.tabs.GetCurrentPage()

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
