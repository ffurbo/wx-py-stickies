#!/usr/bin/env python
"""
main app
"""

import json
import wx
import wx.adv

from notes_frame_wraper import NotesFrameWrapper
from notes_data import Category
from notes_data import new_category
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
            #pos=self.load_window_position(), #wx.Point(100, 100),
            size=wx.Size(500, 300),
            style=0|wx.TAB_TRAVERSAL,
        )

        self.SetPosition(self.load_window_position())

        self.icon = wx.Icon('card.ico')

        self.SetIcon(self.icon)
        self.categories = []
        #self.local_categories_list


        with open('data/categories.json') as json_category_file:
            self.local_categories_list = json.load(json_category_file)


        for category_name in self.local_categories_list:
            category = Category(category_name)
            category.load_files()
            self.categories.append(category)

        self.category = self.categories[0]
        #self.category.load_files()
        #print(self.category.notes)

        self.category_wrappers = []

        for category in self.categories:
            wrapper = NotesFrameWrapper(self.icon, category)
            self.category_wrappers.append(wrapper)


        self.wrapper = self.category_wrappers[0]
        #= NotesFrameWrapper(self.icon, self.category)

        self.init_ui()


    def add_local_category_name(self, name):
        """ save category name to local file"""
        self.local_categories_list.append(name)

        try:
            file = open("data/categories.json", 'w')
            file.write(json.dumps(self.local_categories_list))
        except OSError as err:
            print("can't save data: {0}".format(err))
            return None
        else:
            file.close()

        # with open('data/categories.json') as json_category_file:
        #     self.local_categories_list = json.load(json_category_file)



    def init_ui(self):
        """Initialize user interface"""

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 254, 195))

        b_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button1 = wx.Button(self, wx.ID_ANY, "Test", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button1, 0, wx.ALL, 5)
        self.m_button2 = wx.Button(self, wx.ID_ANY, "Notes", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button2, 0, wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, "New ...", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button4, 0, wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, "Exit", wx.DefaultPosition, wx.DefaultSize, 0)
        b_sizer2.Add(self.m_button3, 0, wx.ALL, 5)

        self.m_button1.Bind(wx.EVT_BUTTON, self.cb_test)
        self.m_button2.Bind(wx.EVT_BUTTON, self.cb_note)
        self.m_button4.Bind(wx.EVT_BUTTON, self.cb_new_category_btn)
        self.m_button3.Bind(wx.EVT_BUTTON, self.cb_exit_btn)
        self.Bind(wx.EVT_CLOSE, self.cb_close_event)

        self.SetSizer(b_sizer2)
        self.Layout()




    def cb_test(self, event):
        """test event"""

    def cb_close_event(self, event):
        """ callback for EVT_CLOSE """
        self.kill_me()


    def cb_exit_btn(self, event):
        """Close the frame, terminating the application."""
        self.kill_me()

    def cb_new_note_btn(self, event):
        """Close the frame, terminating the application."""
        self.wrapper.new_note_dialog()

    def cb_new_category_btn(self, event):
        """Close the frame, terminating the application."""
        self.new_category_dialog()

    def new_category_dialog(self):
        """ new note """
        try:
            dialog = wx.TextEntryDialog(self, "Enter title of new category", caption="New category")
            if dialog.ShowModal() == wx.ID_OK:
                title = dialog.GetValue()
                print('You entered: %s'%title)
                category = new_category(title)
                if category is not None:
                    self.add_local_category_name(category.name)

                    category.load_files()
                    self.categories.append(category)

                    print("Category %s added"%category.name)
                #    self.category.add_note(note)
                #    self.add_note_page(note)

            else:
                print('You entered nothing')
        finally:
            dialog.Destroy()

    def cb_note(self, event):
        """Show note"""
        self.wrapper.frame.Show()
        self.wrapper.frame.Raise()


    def kill_me(self):
        """ close an app """
        #print("Bye bye...")
        #self.wrapper.frame.Destroy()
        for wrapper in self.category_wrappers:
            wrapper.frame.Destroy()
        self.Destroy()


    def __del__(self):
        pass



def main():
    """main function"""

    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
