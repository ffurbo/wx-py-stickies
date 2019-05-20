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
from note_task_bar_icon import NoteTaskBarIcon


class App(wx.App):
    """app"""

    def __init__(self):
        wx.App.__init__(self)

        with open('config.json') as json_cfg_file:
            cfg = json.load(json_cfg_file)

        self.frame = MainWindow(None, cfg)
        self.tbicon = NoteTaskBarIcon(self.frame)
        self.frame.Show()

class MainWindow(MyFrame):
    """
    main frame
    """

    def __init__(self, parent, cfg):
        MyFrame.__init__(
            self, parent,
            id=wx.ID_ANY,
            title=cfg["title"],
            pos=self.load_window_position(), #wx.Point(100, 100),
            size=wx.Size(500, 300),
            style=0|wx.TAB_TRAVERSAL,
        )

        self.icon = wx.Icon('card.ico')

        self.SetIcon(self.icon)
        self.init_ui()

        self.category = Category()
        self.category.load_files()

        self.wrapper = NotesFrameWrapper(self.icon, self.category)

        self.timer = wx.Timer(self)



    def init_ui(self):
        """Initialize user interface"""

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 254, 195))

        b_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button1 = wx.Button(self, wx.ID_ANY, "Test", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button1, 0, wx.ALL, 5)
        self.m_button2 = wx.Button(self, wx.ID_ANY, "Note", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button2, 0, wx.ALL, 5)
        self.m_button3 = wx.Button(self, wx.ID_ANY, "Exit", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button3, 0, wx.ALL, 5)

        self.m_button1.Bind(wx.EVT_BUTTON, self.cb_test)
        self.m_button2.Bind(wx.EVT_BUTTON, self.cb_note)
        self.m_button3.Bind(wx.EVT_BUTTON, self.cb_exit_btn)
        self.Bind(wx.EVT_MOVE, self.cb_move)
        self.Bind(wx.EVT_CLOSE, self.cb_close_event)

        self.Bind(wx.EVT_TIMER, self.cb_timer_event)

        self.SetSizer(b_sizer2)
        self.Layout()

        #self.Iconize(True)

    def cb_timer_event(self, event):
        """ timer test """
        print("timer...")
        position = self.GetPosition().Get()
        self.save_window_position(position)


    def cb_move(self, event):
        """Close the frame, terminating the application."""
        #print("move...")

        timer_running = self.timer.IsRunning
        print(timer_running)

        if not timer_running:
            self.timer.StartOnce(1000)
            print("Staring timer")

        #position = self.GetPosition().Get()
        #self.save_window_position(position)
        #print(position)

    def cb_test(self, event):
        """test event"""

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
        # finally:
        #     print("Function execution completed")


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

    def cb_close_event(self, event):
        """ callback for EVT_CLOSE """
        self.kill_me()

    def cb_exit_btn(self, event):
        """Close the frame, terminating the application."""
        self.kill_me()

    def cb_note(self, event):
        """Show note"""
        self.wrapper.frame.Show()
        self.wrapper.frame.Raise()

    def kill_me(self):
        """ close an app """
        print("Bye bye...")
        self.wrapper.frame.Destroy()
        self.Destroy()


    def __del__(self):
        pass



def main():
    """main function"""

    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
