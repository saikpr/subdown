
import sys
import  wx
import  wx.lib.mixins.listctrl  as  listmix



#---------------------------------------------------------------------------
#index1=1


#list_data[index1]=(("sdffsd","Dfsdfsdf","Fdsfdsf"))

#---------------------------------------------------------------------------

class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self,parent_frame,ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent_frame, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class TestListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self,parent, parent_frame,list_Data,session_token):
        wx.Panel.__init__(self, parent_frame, -1, style=wx.WANTS_CHARS)
        self.parent=parent
        self.list_data = list_Data
        tID = wx.NewId()
        self.session_token=session_token
        prompt = wx.StaticText(self, -1, '\nPlease Select The most Appropriate SRT file As Available from Opensubtiles\n\n')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(prompt, 0, wx.ALIGN_CENTER)
        #box1.Add(self.cmd, 1, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(prompt, 0, wx.ALIGN_CENTER)
        sizer.Add(box1, 0, wx.EXPAND|wx.ALL, 10)

        self.list = TestListCtrl(self, tID,
                                 style=wx.LC_REPORT 
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 #| wx.LC_SORT_ASCENDING
                                 | wx.LC_AUTOARRANGE
                                 | wx.LC_NO_HEADER
                                 | wx.LC_VRULES
                                 | wx.LC_HRULES
                                 | wx.LC_SINGLE_SEL
                                 )
        
        #self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.EXPAND)

        #self.PopulateList()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = self.list_data
        listmix.ColumnSorterMixin.__init__(self, 3)
        #self.SortListItems(0, True)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        #self.list.Bind(wx.EVT_LIST_COL_CLICK, self.doNothing)
        #self.list.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.doNothing)
        #EVT_LIST_COL_RIGHT_CLICK


    def newData(self,list_Data,session_token):
        self.list_data = list_Data
        self.session_token=session_token
        if len(self.list_data)==1:
            self.parent.downloadsubtitlefromopen(self.list_data[1][0],self.session_token)
        self.PopulateList()


    def PopulateList(self):
       
            # for normal, simple columns, you can add them like this:
        self.list.ClearAll()
        self.list.InsertColumn(0, "Title")
        #self.list.InsertColumn(1, "Title")
        self.list.InsertColumn(1, "PerCentage Match")
        #
        #print "\n\nInside Populate disk\n\n\n"
       # print self.list_data

        items = self.list_data.items()
        for key, data in items:
           # print data
            #print sys.maxint
           # print str(data[1])
            index = self.list.InsertStringItem(sys.maxint,str(data[1]))
            self.list.SetStringItem(index, 1,  str(data[2]))
            #self.list.SetStringItem(index, 2, str(data[0]))
            self.list.SetItemData(index, key)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        #self.list.SetColumnWidth(2, 100)

    def doNothing(self,event):
        event.Skip()


    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)



    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()


    def OnItemSelected(self, event):
        ##print event.GetItem().GetTextColour()
        self.currentItem = event.m_itemIndex
        #print self.currentItem
        

        if self.currentItem == 10:
            #self.log.WriteText("OnItemSelected: Veto'd selection\n")
            #event.Veto()  # doesn't work
            # this does
            self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

        event.Skip()
    def OnDoubleClick(self, event):
        #self.log.WriteText("OnDoubleClick item %s\n" % self.list.GetItemText(self.currentItem))
        #print "\n\n\n\n\n"
        #print "fgfd gdfgdf"
        #print self.list_data[self.currentItem+1][0]
        self.parent.downloadsubtitlefromopen(self.list_data[self.currentItem+1][0],self.session_token)
        #self.parent.killme=True
        event.Skip()

    
def runTest(parent,frame, nb,list_Data={},session_token=0):
    global win
    win = TestListCtrlPanel(parent,nb,list_Data,session_token)
    return win
def pushData(list_Data,session_token):
    global win
    win.newData(list_Data,session_token)

