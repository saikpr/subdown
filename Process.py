import  wx
import os
import threading
from hashlib import md5
from urllib2 import Request , URLError
from urllib2 import ProxyHandler,HTTPBasicAuthHandler, build_opener, HTTPHandler, install_opener
import ListCtrl as module1
from xmlrpclib import ServerProxy
from fuzzywuzzy import fuzz
from cStringIO import StringIO
from base64 import b64decode
from gzip import GzipFile
import time
from operator import itemgetter
from subdown_version import __version__
proxy_url=''
username=''
password=''
if proxy_url is '':
    proxy_str=''
    proxy_dict={}
elif username is not '':
    proxy_str='http://'+username+':'+password+'@'+proxy_url
    proxy_dict={'http':proxy_str}
else:
    proxy_str='http://'+proxy_url
    proxy_dict={'http':proxy_str}

proxy = ProxyHandler(proxy_dict)
auth = HTTPBasicAuthHandler()
opener = build_opener(proxy, auth, HTTPHandler)
install_opener(opener)
def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return md5(data).hexdigest()
#----------------------------------------------------------------------
class SubNoTFOUND(Exception):
    pass
class subdubThread(threading.Thread):
     global opener
     def __init__(self,hash_data,parent,path,alt_thread):
         threading.Thread.__init__(self)
         self.hash_data=hash_data
         self.parent=parent
         self.out=parent.out
         self.Strtbtn=parent.Strtbtn
         self.sndBtn=parent.sndBtn
         self.path=path
         self.alt_thread=alt_thread
         #self.argvs=argvs
     def run(self):
        headers = { 'User-Agent' : 'SubDB/1.0 (SubDown/0.1; http://github.com/sainyamkapoor/SubDown)' }
        url = "http://api.thesubdb.com/?action=download&hash="+self.hash_data+"&language=en"
        req = Request(url, '', headers)
        try:
            response = opener.open(req).read()
            with open (self.path+".srt","wb") as subtitle:
                subtitle.write(response)
            self.out.AppendText("[subdb]:Downloaded!\n\n")
            try:
                self.parent.argvs=self.parent.argvs[1:]
                self.parent.path=self.parent.argvs[0]

                
                self.parent.startdown(None)
            except IndexError:
                self.Strtbtn.Enable(False)
                self.sndBtn.Enable(True)
                self.out.AppendText("\n[SubDown]:Completed!\n\n************************************************\n")
            #return 0
        except URLError as urler:
            
            try:
                k=urler.code
                self.out.AppendText("[opensub]:Trying Alternative Site now!\n")
                self.alt_thread.start()
            except AttributeError:
                self.out.AppendText ("\n[SubDown]:Jim I am Sorry, I am unable to find any internet connection. :( :(\nJim You might want to use Subdown Along with proxifier(If know what it is)\nPress Done to Exit")
                self.Strtbtn.Enable(False)
                self.sndBtn.Enable(True)
            

class openSubThread(threading.Thread):
     global opener
     def __init__(self,clean_path,filename,path,out,opensubtitleconnection,frame1,parent):
         threading.Thread.__init__(self)
         self.clean_path=clean_path
         self.filename=filename
         self.path=path
         self.out=out
         self.frame1=frame1
         self.parent=parent
         self.opensubtitleconnection=opensubtitleconnection
     def run(self):
        
        #module1=__import__('ListCtrl')
        
        
        
        allpages = self.opensubtitleconnection.LogIn( '', '', 'en', 'PySubDown '+__version__)
        self.session_token=allpages['token']
        replace = ["Watch" ,"youtube" ,"Youtube"]
        for content in replace:
            self.filename = self.filename.replace(content,"")
        self.filename = self.filename.replace("."," ")
        #file_hash=hashFile(path)
        
        #myquery_hash={'moviehash':file_hash, 'sublanguageid' : 'eng'}
        #subtitles_hash=self.opensubtitleconnection.SearchSubtitles( self.session_token, [myquery_hash], {'limit' : 100})
        #subdata= subtitles_hash['data']
        #if subtitles_hash['data']==False:
        myquery={'query' : self.filename, 'sublanguageid' : 'eng'}
        subtitles=self.opensubtitleconnection.SearchSubtitles( self.session_token, [myquery], {'limit' : 100})
        subdata=subtitles['data']
        
        list_Data={}
        if subdata !=False:
            
            for di in subdata:
                di['fuzzylogic'] =fuzz.token_sort_ratio(self.filename,di['SubFileName'])
                
            subdata = sorted(subdata, key=itemgetter('fuzzylogic'),reverse=True)
            #print subdata[0]
            i=1
            #self.out.AppendText("\nChoose the most appropriate  from List")
            for di in subdata:
                if i>10:
                    break
                try :
                    list_Data[i]=(di['IDSubtitleFile'],di['SubFileName'],di['fuzzylogic'])
                    i+=1
                except UnicodeEncodeError:
                    continue #add unicode support here
                
            #print list_Data
            
            if len(list_Data)==1:
                self.out.AppendText("[opensub]:Downloading the Most Appropriate SRT automatically.\n ")
            self.frame1.Show()
            

            module1.pushData(list_Data,self.session_token)
            #win1.SetFocus()
            #self.app.SetTopWindow(self.frame1)
            
        else:
            ##say sorry can't find it
            self.out.AppendText("[SubDown]:Jim I am Sorry, I am unable to find it. :( :(\n\n ")#inp=int(raw_input("\nEnter the one you would like to download:"))
            try:
                self.parent.argvs=self.parent.argvs[1:]
                self.parent.path=self.parent.argvs[0]

                
                self.parent.startdown(None)
            except IndexError:
                self.parentStrtbtn.Enable(False)
                self.parentsndBtn.Enable(True)
                self.out.AppendText("\n[SubDown]:Completed\n\n************************************************\n")

class TestPanel(wx.Panel):
    
    def __init__(self, parent_frame, ID,argvs,app):
        
        wx.Panel.__init__(self, parent_frame, ID)
        
        #self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)
        self.app=app
        self.parent_frame=parent_frame
        if argvs==None:
            self.path=''
        else:
            self.path=argvs[1]
            self.argvs=argvs[2:]
        #buttons and text
        prompt = wx.StaticText(self, -1, 'File Name:')
        
        self.cmd = wx.TextCtrl(self, -1, self.path,style=wx.TE_READONLY)
        self.out = wx.TextCtrl(self, -1, '',style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
        self.sndBtn = wx.Button(self, -1, 'Done')
        self.Strtbtn = wx.Button(self, -1, 'Start')
        self.sndBtn.Enable(False)

        self.Bind(wx.EVT_BUTTON, self.OnSendText, self.sndBtn)
        if  argvs==None:
            
            self.Strtbtn.Enable(False)
        else:
            self.Bind(wx.EVT_BUTTON, self.startdown, self.Strtbtn)
            self.Strtbtn.Enable(True)
        #layout
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(prompt, 0, wx.ALIGN_CENTER)
        box1.Add(self.cmd, 1, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(self.Strtbtn, 0, wx.LEFT, 5)
        box2.Add(self.sndBtn, 0, wx.RIGHT, 5)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box1, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.out, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(box2, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        frame1 = wx.Frame(None, -1, "List", style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        self.frame1=frame1
        self.frame1.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.frame1.Hide()
        win1 = module1.runTest(self,self.app, self.frame1)
        #self.startdown(None)
    
    def pushArgv(self,argvs):
        self.path=argvs[0]
        self.argvs=[]
        #print "fsdfds"
        #print argvs
        self.cmd.SetLabel(self.path)
        self.startdown(None)
        self.parent_frame.Show()
    def pushFolderArgv(self,list_d):
        
        #print "fsdfds"
        #print argvs
        self.cmd.SetLabel(list_d[0])
        self.parent_frame.Show()
        #print "I raeachsf here"
        self.path=list_d[1]
        self.argvs=list_d[1:]
        self.startdown(None)
        

    def startdown(self,evt):
        #code start
        #print evt
        self.out.AppendText("[SubDown]:Trying to Download Subtitles for \n"+self.path.split("\\")[-1]+'.\n')
        hash_data = get_hash(self.path)
        filename=self.path.split('\\')[-1]
        replace = [".avi",".mp4",".mkv",".mpg",".mpeg"]
        clean_path=self.path
        self.clean_path=clean_path
        for content in replace:
            filename = filename.replace(content,'')
            clean_path = clean_path.replace(content,"")
        
        opensubtitleurl = "http://api.opensubtitles.org/xml-rpc"
        self.opensubtitleconnection = ServerProxy( opensubtitleurl )
        
        alt_thread=openSubThread(clean_path,filename,self.path,self.out,self.opensubtitleconnection,self.frame1,self)
        thread=subdubThread(hash_data,self,clean_path,alt_thread)
        thread.start()
    def downloadsubtitlefromopen(self,IDSubtitleFile,session_token):
        self.frame1.Hide()
        #print "Download" + str(IDSubtitleFile)
        #print session_token
        subdo=self.opensubtitleconnection.DownloadSubtitles(session_token, [IDSubtitleFile] )
        # this is the variable with your file's contents    
        #print subdo
        k= subdo['data']
        #print k
        k1 = k[0]
        gzipped_data=k1['data'] 

        # we now decode the file's content from the string and unzip it
        orig_file_desc = GzipFile(mode='r',fileobj=StringIO(b64decode(gzipped_data)))

        # get the original's file content to a variable
        orig_file_cont = orig_file_desc.read()

        # and close the file descriptor
        orig_file_desc.close()
        file2=open(self.clean_path+".srt",'wb')
        file2.write(str(orig_file_cont))
        file2.close()
    
        #self.Strtbtn.Enable(False)
        #self.sndBtn.Enable(True)
        
        self.out.AppendText("[opensub]:Downloaded!\n\n")

        logout=self.opensubtitleconnection.LogOut( session_token )
        try:
            self.argvs=self.argvs[1:]
            self.path=self.argvs[0]

            
            self.startdown(None)
        except IndexError:
            self.Strtbtn.Enable(False)
            self.sndBtn.Enable(True)
            self.out.AppendText("\n[SubDown]:Completed!\n****************************************\n")
        

    def OnSendText(self, evt):
        #text = self.inp.GetValue()
        #self.inp.SetValue('')
        #self.process.GetOutputStream().write(text + 'dgdfgfdgfdgdg\n')
        #self.inp.SetFocus()
        raise SystemExit
  
    def OnCloseFrame(self, evt):
        
        evt.Skip()
        raise SystemExit

#----------------------------------------------------------------------

def runTest(frame, nb,argvs,app):
    global win
    if len(argvs)==1:
        print "I have no arguments to run"
        win = TestPanel(nb, -1,None,app)
        return win
    win = TestPanel(nb, -1,argvs,app)
    return win
def pushArgv(argvs):
    global win
    #print "I have Got following "+str(argvs)
    win.pushArgv(argvs)

def pushFolderArgv(list_d):
    global win
    #print "I have Got following "+str(list_d)
    win.pushFolderArgv(list_d)