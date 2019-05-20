""" module containing task bar icon class"""
import wx
import wx.adv


def create_menu_item(menu, label, func):
    """ helper for creating menu"""
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class NoteTaskBarIcon(wx.adv.TaskBarIcon):
    """ note task bar icon """

    def __init__(self, main_frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(main_frame.GetIcon(), "WX PyStickies")

        self.main_frame = main_frame

        menu = wx.Menu()
        create_menu_item(menu, 'Say Hello', self.cb_on_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.cb_on_exit)
        self.menu = menu

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.cb_taskbar_click)

    def CreatePopupMenu(self):
        """ create popup menu """

        return self.menu

    def cb_taskbar_click(self, event):
        """ left click on tray icon"""
        print("Taskbar click")
        self.main_frame.toggle()

    def cb_on_hello(self, event):
        """ hello """
        print('Hello, world!')

    def cb_on_exit(self, event):
        """ exit """
        #self.menu.Destroy()
        #self.menu = None

        self.main_frame.Close()
        self.Destroy()
        #wx.CallAfter(self.Destroy)
