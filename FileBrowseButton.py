import  wx
import  wx.lib.filebrowsebutton as filebrowse
import Process as module2
class TestPanel(wx.Panel):
    def __init__(self, parent_frame, ID):
        wx.Panel.__init__(self, parent_frame, ID)
        

        self.fbbh = filebrowse.FileBrowseButton(
            self, -1, size=(450, -1),  changeCallback = self.fbbhCallback
            )
            
        self.dbb = filebrowse.DirBrowseButton(
            self, -1, size=(450, -1), changeCallback = self.dbbCallback
            )

        #self.fbbh.callCallback = True
        #self.fbbh.SetHistory([], 4)
        self.parent_frame=parent_frame
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.fbbh, 0, wx.ALL, 5)
        sizer.Add(self.dbb, 0, wx.ALL, 5)
        box = wx.BoxSizer()
        box.Add(sizer, 0, wx.ALL, 20)
        self.SetSizer(box)


    def fbbhCallback(self, evt):
        if hasattr(self, 'fbbh'):
            value = evt.GetString()
            if not value:
                return
            #self.log.write('FileBrowseButtonWithHistory: %s\n' % value)
            self.parent_frame.Hide()
            print "dfd"+str(value)
            #module2=__import__('Process')
            module2.pushArgvs([value])
            
            


    def dbbCallback(self, evt):
        #self.log.write('DirBrowseButton: %s\n' % evt.GetString())
        print "dgdfgdfg"


#----------------------------------------------------------------------
def runTest(frame, nb):
    win = TestPanel(nb, -1)
    return win





