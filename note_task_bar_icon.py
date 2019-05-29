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

        # menu = wx.Menu()
        # create_menu_item(menu, 'Say Hello', self.cb_on_hello)
        # menu.AppendSeparator()
        # create_menu_item(menu, 'Exit', self.cb_on_exit)
        # self.menu = menu

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.cb_taskbar_click)

    def CreatePopupMenu(self):
        """ create popup menu """

        print(self.main_frame.categories)

        menu = wx.Menu()

        for cat_wrapper in self.main_frame.category_wrappers:
            create_menu_item(menu, cat_wrapper.category.name, lambda event, frame=cat_wrapper.frame: self.cb_show_frame(event, frame))

        #create_menu_item(menu, 'Say Hello', self.cb_on_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.cb_on_exit)
        return menu

    def cb_taskbar_click(self, event):
        """ left click on tray icon"""
        print("Taskbar click")
        self.main_frame.toggle()

    def cb_multi_hello(self, name):
        """ return call back function """

        def cb_function(event):
            print("Hello %s!"%name)

        return cb_function


    def cb_show_frame(self, event, frame):
        """ hello """
        frame.Show()
        frame.Raise()


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
