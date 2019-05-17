#!/usr/bin/env python
"""
main app
"""

import json
import wx
import wx.adv

from notes_frame_wraper import NotesFrameWrapper
from notes_data import Category
from my_frame import MyFrame


class App(wx.App):
    """app"""

    def __init__(self):
        wx.App.__init__(self)

        with open('config.json') as json_cfg_file:
            cfg = json.load(json_cfg_file)

        self.icon = wx.Icon('card.ico')
        self.tbicon = wx.adv.TaskBarIcon()
        self.tbicon.SetIcon(self.icon, cfg['title'])

        def cb_taskbar_click(event):
            """ left click on tray icon"""
            print("Taskbar click")
            self.frame.toggle()


        self.tbicon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, cb_taskbar_click)

        #frame = NoteWindow(None, self.icon)
        self.frame = MainWindow(None, self.icon, cfg)
        self.frame.Show()

class MainWindow(MyFrame):
    """
    main frame
    """

    def __init__(self, parent, icon, cfg):
        MyFrame.__init__(
            self, parent,
            id=wx.ID_ANY,
            title=cfg["title"],
            pos=self.load_window_position(), #wx.Point(100, 100),
            size=wx.Size(500, 300),
            style=0|wx.TAB_TRAVERSAL,

        )

        #point = self.load_window_position()
        #print("loaded point: [%s]"%(json.dumps(point.Get())))

        self.SetIcon(icon)
        self.init_ui()
        self.icon = icon

        self.category = Category()
        self.category.load_files()

        self.wrapper = NotesFrameWrapper(icon, self.category)


    def init_ui(self):
        """Initialize user interface"""

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 254, 195))

        b_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button1 = wx.Button(
            self, wx.ID_ANY, "Test", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button1, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(
            self, wx.ID_ANY, "Note", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button2, 0, wx.ALL, 5)

        self.m_button3 = wx.Button(
            self, wx.ID_ANY, "Exit", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button3, 0, wx.ALL, 5)

        self.m_button1.Bind(wx.EVT_BUTTON, self.cb_test)
        self.m_button2.Bind(wx.EVT_BUTTON, self.cb_note)
        self.m_button3.Bind(wx.EVT_BUTTON, self.cb_exit)
        self.Bind(wx.EVT_MOVE, self.cb_move)

        self.SetSizer(b_sizer2)
        self.Layout()

        #self.Iconize(True)

    def cb_move(self, event):
        """Close the frame, terminating the application."""
        print("move...")
        position = self.GetPosition().Get()
        #print(json.dumps(self.GetPosition().Get()))
        self.save_window_position(position)
        print(position)

    def cb_test(self, event):
        """Close the frame, terminating the application."""
        #print(self.GetScreenPosition().Get())
        self.save_window_position(self.GetPosition().Get())


    def save_window_position(self, position):
        """ save position tuple to file """
        str_position = json.dumps(position)
        file_name = 'data/main_window_position.json'

        try:
            file = open(file_name, 'w')
            file.write(str_position)
        except OSError as err:
            print("can't save window position: {0}".format(err))
        else:
            file.close()
            print("position saved")
        finally:
            print("Function execution completed")


    def load_window_position(self):
        """ load window position from file """
        file_name = 'data/main_window_position.json'

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



    def cb_exit(self, event):
        """Close the frame, terminating the application."""
        self.wrapper.frame.Destroy()
        self.Close(True)

    def cb_note(self, event):
        """Show note"""
        self.wrapper.frame.Show()
        self.wrapper.frame.Raise()

    # def toggle(self):
    #     """Toggle frame"""
    #     if self.IsShown():
    #         self.Show(False)
    #     else:
    #         self.Show(True)

    def __del__(self):
        pass



def main():
    """main function"""

    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
