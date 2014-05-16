import wx
#import time
import sys, os
import  wx.lib.layoutf  as layoutf
from subdown_version import __version__
from About import MyAboutBox
import FileBrowseButton as module0
import ListCtrl as module1
import Process as module2
class Run_GUI(wx.App,):
    global testing
    def __init__(self, name,argv):
        self.name = name
        
        self.argv=argv
        wx.App.__init__(self, redirect=False)
        

    def OnInit(self):
        

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        #item = menu.Append(-1, "&File&Folder", "File&Folder")
        #self.Bind(wx.EVT_MENU, self.disp0, item)
        #item = menu.Append(-1, "&ListCtrl", "ListCtrl")
        #self.Bind(wx.EVT_MENU, self.disp1, item)
        #item = menu.Append(-1, "&Process", "Process")
        #self.Bind(wx.EVT_MENU, self.disp2, item)
        item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnExitApp, item)
        menuBar.Append(menu, "&File")
        frame0 = wx.Frame(None, -1, self.name,style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        frame0.CreateStatusBar()
        frame0.SetMenuBar(menuBar)
        frame0.Hide()
        frame0.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        #frame0.SetSize((400,400))
        about_menu = wx.Menu()
        item_about = about_menu.Append(-1, "&About SubDown", "About SubDown")
        self.Bind(wx.EVT_MENU, self.onAboutSubdown, item_about)
        menuBar.Append(about_menu, "&Help")
        self.win0 = module0.runTest(frame0, frame0,)
        self.dlg = MyAboutBox(None)
        
        
        menuBar2 = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "&File&Folder", "File&Folder")
        self.Bind(wx.EVT_MENU, self.disp0, item)
       # item = menu.Append(-1, "&ListCtrl", "ListCtrl")
        #self.Bind(wx.EVT_MENU, self.disp1, item)
        #item = menu.Append(-1, "&Process", "Process")
        #self.Bind(wx.EVT_MENU, self.disp2, item)
        item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnExitApp, item)
        menuBar2.Append(menu, "&File")
        frame2 = wx.Frame(None, -1, self.name, style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        frame2.CreateStatusBar()
        about_menu = wx.Menu()
        item_about = about_menu.Append(-1, "&About SubDown", "About SubDown")
        self.Bind(wx.EVT_MENU, self.onAboutSubdown, item_about)
        menuBar2.Append(about_menu, "&Help")
        frame2.SetMenuBar(menuBar2)
        frame2.Hide()
        #frame2.Show()
        frame2.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.win2 = module2.runTest(frame2, frame2,self.argv,self)
        #print self.argv
        
           
       # print testing
        self.frame0=frame0
        self.frame2=frame2
        if testing==0:
            #frame0.
            frame0.Show()
            #self.win0.SetFocus()
            #self.window = self.win0
            self.SetTopWindow(frame0)
            
            self.frame = frame0

        elif testing ==2 :
            #frame2.
            
            frame2.Show()
            
            #self.win2.SetFocus()
            #self.window = self.win2
            self.SetTopWindow(frame2)
            
            self.frame = frame2
        else :
            raise WrongTestingValue
                           
        return True

    def disp0(self,evt):
        
        testing=0
        #self.frame.Hide()
        self.frame=self.frame0
        self.frame.Show()
        #frame0. 
        self.SetTopWindow(self.frame)
    
    def disp2(self,evt):
        print "triggererers"
        testing=2
        #self.frame.Hide()
        self.frame=self.frame2
        #self.frame2.Show()
        #frame2.
        self.SetTopWindow(self.frame)

    def onAboutSubdown(self,evt):
        self.dlg.ShowModal()
        #self.dlg.Destroy()
    
    def OnExitApp(self, evt):
        self.frame.Close(True)
        raise SystemExit


    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()

#----------------------------------------------------------------------------


def main(argv):
    name="SubDown v"+__version__
    
    app = Run_GUI(name,argv)
    app.MainLoop()



if __name__ == "__main__":
    global testing
    testing=0
    if len(sys.argv)!=1:
        testing=2
    main(sys.argv)


