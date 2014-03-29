"""
Subtitle-Downloader v1.0
Name:Sainyam Kapoor
Use:Used to Download subtitles from subdb and opensubtitles.org

"""
"""Proxy settings"""
proxy_url=''
username=''
password=''


"""Code begins"""
import struct,os,hashlib,urllib2,sys,xmlrpclib
from fuzzywuzzy import fuzz,process
from cStringIO import StringIO
from base64 import b64decode
from gzip import GzipFile
from operator import itemgetter
if proxy_url is '':
    proxy_str=''
    proxy_dict={}
elif username is not '':
    proxy_str='http://'+username+':'+password+'@'+proxy_url
    proxy_dict={'http':proxy_str}
else:
    proxy_str='http://'+proxy_url
    proxy_dict={'http':proxy_str}

proxy = urllib2.ProxyHandler(proxy_dict)
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)
def hashFile(name): 
      try: 
                 
                longlongformat = 'q'  # long long 
                bytesize = struct.calcsize(longlongformat) 
                    
                f = open(name, "rb") 
                    
                filesize = os.path.getsize(name) 
                hash = filesize 
                    
                if filesize < 65536 * 2: 
                       return "SizeError" 
                 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                         
    
                f.seek(max(0,filesize-65536),0) 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF 
                 
                f.close() 
                returnedhash =  "%016x" % hash 
                return returnedhash 
    
      except(IOError): 
                return "IOError"
def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

def sub_downloader(path):

    hash = get_hash(path)
    replace = [".avi",".mp4",".mkv",".mpg",".mpeg"]
    for content in replace:
        path = path.replace(content,"")
    if not os.path.exists(path+".srt"):
        headers = { 'User-Agent' : 'SubDB/1.0 (SubDown/0.1; http://github.com/sainyamkapoor/SubDown)' }
        url = "http://api.thesubdb.com/?action=download&hash="+hash+"&language=en"
        req = urllib2.Request(url, '', headers)
        try:
            response = opener.open(req).read()
        except urllib2.URLError as urler:
            
            try:
                print("[SubDown]:Not found At Primary Location, Trying Secondary Location")
            except AttributeError:
                print "[SubDown]:Internet not working or maybe unable to find  connection to primary server"
            return 0
        
        with open (path+".srt","wb") as subtitle:
            subtitle.write(response)
            return 1
def alt_downloader(clean_path,filename,path):
    subtitlesids={}
    opensubtitleurl = "http://api.opensubtitles.org/xml-rpc"
    opensubtitleconnection = xmlrpclib.ServerProxy( opensubtitleurl )
    allpages = opensubtitleconnection.LogIn( '', '', 'en', 'PySubDown v1.0')
    session_token=allpages['token']
    replace = ["Watch"]
    for content in replace:
        filename = filename.replace(content,"")
    filename = filename.replace("."," ")
    file_hash=hashFile(path)
    print file_hash
    myquery_hash={'moviehash':file_hash, 'sublanguageid' : 'eng'}
    subtitles_hash=opensubtitleconnection.SearchSubtitles( session_token, [myquery_hash], {'limit' : 100})
    subdata= subtitles_hash['data']
    if subtitles_hash['data']==False:
        myquery={'query' : filename, 'sublanguageid' : 'eng'}
        subtitles=opensubtitleconnection.SearchSubtitles( session_token, [myquery], {'limit' : 100})
        subdata=subtitles['data']
    i=0
    
    if subdata !=False:
        print type(subdata)

        for di in subdata:
            di['fuzzylogic'] =fuzz.token_sort_ratio(filename,di['SubFileName'])
        subdata = sorted(subdata, key=itemgetter('fuzzylogic'),reverse=True)
        i=0
        for di in subdata:
            if i>10:
                break
            print str(i+1)+") :"+di['SubFileName']
            subtitlesids[i]=di['IDSubtitleFile']
            i+=1
        inp=int(raw_input("Enter the one you would like to download:"))

        subdo=opensubtitleconnection.DownloadSubtitles(session_token, [subtitlesids[inp-1]] )
        # this is the variable with your file's contents    
        k= subdo['data']
        k1 = k[0]
        gzipped_data=k1['data'] 

        # we now decode the file's content from the string and unzip it
        orig_file_desc = GzipFile(mode='r',fileobj=StringIO(b64decode(gzipped_data)))

        # get the original's file content to a variable
        orig_file_cont = orig_file_desc.read()

        # and close the file descriptor
        orig_file_desc.close()
        file2=open(clean_path+".srt",'wb')
        file2.write(str(orig_file_cont))
        file2.close()
    else:
        raw_input("[SubDown]:Sorry I am Unable to Find it anyplace i know of\nPress Enter to exit")


    logout=opensubtitleconnection.LogOut( session_token )
if __name__=='__main__': 
    path = sys.argv[1]
    filename=path.split('\\')[-1]

    replace = [".avi",".mp4",".mkv",".mpg",".mpeg"]
    for content in replace:
        filename = filename.replace(content,"")
        clean_path = path.replace(content,"")
    print "[SubDown]:Trying to Download " +filename
    if os.path.exists(clean_path+".srt"):
        ans=str(raw_input("Looks Like the SRT file exist\nWould You like To delete that file and Download a new one? :"))
        ans=ans.lower()
        if ans=='y' or ans=='yes':
            os.remove(clean_path+".srt")
        else :
            exit(0)
    if not sub_downloader(path):
        alt_downloader(clean_path,filename,path)