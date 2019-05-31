#!/usr/bin/env python
"""
main app
"""

import json
from shutil import copyfile
import os
from pathlib import Path
import sys
import wx
import wx.adv

# from notes_frame_wraper import NotesFrameWrapper
from notes_frame import NotesFrame
from notes_data import Category
from notes_data import new_category
from my_frame import MyFrame
from note_task_bar_icon import NoteTaskBarIcon


class App(wx.App):
    """app"""

    def __init__(self):
        wx.App.__init__(self)

        res = Resources()

        try:
            os.chdir(res.work_dir)
            print("Directory changed")
        except OSError:
            print("Can't change the Current Working Directory")

        self.frame = MainWindow(res)
        self.tbicon = NoteTaskBarIcon(self.frame)
        self.frame.Show(False)


class Resources:
    """ app resources """

    def __init__(self):

        self.work_dir = os.path.join(str(Path.home()), ".wx-py-stickies")
        self.app_dir = os.path.dirname(os.path.realpath(__file__))

        self.icon = wx.Icon(os.path.join(self.app_dir, 'card.ico'))

        self.check_dir(self.work_dir)
        self.check_dir(os.path.join(self.work_dir, "data"))
        self.check_dir(os.path.join(self.work_dir, "data", "categories"))

        self.check_file(self.work_dir, 'config.json')

        with open(os.path.join(self.work_dir, 'config.json')) as json_cfg_file:
            self.cfg = json.load(json_cfg_file)


    def check_dir(self, directory):
        """  create directory if not exist"""
        if not os.path.exists(directory):
            os.mkdir(directory)
            print("Directory ", directory, " Created ")
        else:
            print("Directory ", directory, " already exists")

    def check_file(self, path, filename):
        """ make sure file is copied from application dir to path """
        filepath = os.path.join(path, filename)

        if not os.path.exists(filepath):

            src_filepath = os.path.join(self.app_dir, filename)
            if not os.path.exists(src_filepath):
                sys.exit("%s file is missing"%src_filepath)

            self.check_dir(path)
            copyfile(src_filepath, filepath)
        else:
            print("File %s present "%filepath)


class MainWindow(MyFrame):
    """
    main frame
    """

    def __init__(self, res):
        MyFrame.__init__(
            self, None,
            id=wx.ID_ANY,
            title=res.cfg["title"],
            style=0|wx.TAB_TRAVERSAL|wx.DEFAULT_FRAME_STYLE,
        )

        self.res = res
        self.icon = res.icon
        self.SetPosition(self.load_window_position())
        self.SetSize(self.load_window_size())

        self.SetIcon(res.icon)
        self.categories = []

        file_name = 'data/categories.json'

        try:
            json_category_file = open(file_name, 'r')
            self.local_categories_list = json.load(json_category_file)
        except OSError as err:
            print("can't load property: {0}".format(err))
            self.local_categories_list = []
            self.categories_to_file()
        else:
            json_category_file.close()


        for category_name in self.local_categories_list:
            category = Category(category_name)
            category.load_files()
            self.categories.append(category)


        self.category_wrappers = []

        for category in self.categories:
            wrapper = NotesFrame(self.res, category)
            self.category_wrappers.append(wrapper)


        self.init_ui()
        for wrapper in self.category_wrappers:
            wrapper.Show(wrapper.pinned)


    def add_local_category_name(self, name):
        """ save category name to local file"""
        self.local_categories_list.append(name)
        self.categories_to_file()



    def categories_to_file(self):
        """  categories list to file """
        try:
            file = open("data/categories.json", 'w')
            file.write(json.dumps(self.local_categories_list))
        except OSError as err:
            print("can't save data: {0}".format(err))
        else:
            file.close()


    def init_ui(self):
        """Initialize user interface"""

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(*self.res.cfg["note_color"]))

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
        #self.kill_me()
        self.Show(False)


    def cb_exit_btn(self, event):
        """Close the frame, terminating the application."""
        self.kill_me()

    def cb_new_note_btn(self, event):
        """Close the frame, terminating the application."""
        #self.wrapper.new_note_dialog()

    def cb_new_category_btn(self, event):
        """Close the frame, terminating the application."""
        self.new_category_dialog()

    def new_category_dialog(self, parent=None):
        """ new note """
        try:
            dialog = wx.TextEntryDialog(parent, "Enter title of new category", caption="New category")
            if dialog.ShowModal() == wx.ID_OK:
                title = dialog.GetValue()
                print('You entered: %s'%title)
                category = new_category(title)
                if category is not None:
                    self.add_local_category_name(category.name)

                    category.load_files()
                    self.categories.append(category)
                    wrapper = NotesFrame(self.res, category)
                    self.category_wrappers.append(wrapper)
                    wrapper.Show()

                    print("Category %s added"%category.name)
                #    self.category.add_note(note)
                #    self.add_note_page(note)

            else:
                print('You entered nothing')
        finally:
            dialog.Destroy()

    def cb_note(self, event):
        """Show note"""
        #self.wrapper.frame.Show()
        #self.wrapper.frame.Raise()


    def kill_me(self):
        """ close an app """
        #print("Bye bye...")
        #self.wrapper.frame.Destroy()
        for wrapper in self.category_wrappers:
            wrapper.Destroy()
        self.Destroy()


    def __del__(self):
        pass



def main():
    """main function"""

    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
