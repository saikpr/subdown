import  wx,os
import  wx.lib.filebrowsebutton as filebrowse
import Process as module2
class TestPanel(wx.Panel):
    def __init__(self, parent_frame, ID):
        wx.Panel.__init__(self, parent_frame, ID)
        

        self.fbbh = filebrowse.FileBrowseButton(
            self, -1, size=(450, -1),  changeCallback = self.fbbhCallback,  buttonText="Download Srt", labelText="Select File"
            )
            
        self.dbb = filebrowse.DirBrowseButton(
            self, -1, size=(450, -1), changeCallback = self.dbbCallback,  buttonText="Download Srt", labelText="Select Folder"
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
            module2.pushArgv([value,value])
            
            


    def dbbCallback(self, evt):
        value = evt.GetString()
        #print value
        #print "BOyaah"
        list_d=[value]
        self.parent_frame.Hide()
        for dirname, dirnames, filenames in os.walk(value):
            for filename in filenames:
                if filename.split('.')[-1].lower() in ["avi","mp4","mkv","mpg","mpeg","flv"]:
                    #print os.path.join(dirname, filename)
                    list_d.append(os.path.join(dirname, filename))
        print list_d
        module2.pushFolderArgv(list_d)
#----------------------------------------------------------------------
def runTest(frame, nb):
    win = TestPanel(nb, -1)
    return win





