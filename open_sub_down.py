from xmlrpclib import ServerProxy
from fuzzywuzzy import fuzz
from cStringIO import StringIO
from base64 import b64decode
from gzip import GzipFile
from operator import itemgetter
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

def open_sub(clean_path,filename,path):
    subtitlesids={}
    opensubtitleurl = "http://api.opensubtitles.org/xml-rpc"
    opensubtitleconnection = ServerProxy( opensubtitleurl )
    allpages = opensubtitleconnection.LogIn( '', '', 'en', 'PySubDown v1.0')
    session_token=allpages['token']
    replace = ["Watch" ,"youtube" ,"Youtube"]
    for content in replace:
        filename = filename.replace(content,"")
    filename = filename.replace("."," ")
    #file_hash=hashFile(path)
    
    #myquery_hash={'moviehash':file_hash, 'sublanguageid' : 'eng'}
    #subtitles_hash=opensubtitleconnection.SearchSubtitles( session_token, [myquery_hash], {'limit' : 100})
    #subdata= subtitles_hash['data']
    #if subtitles_hash['data']==False:
    myquery={'query' : filename, 'sublanguageid' : 'eng'}
    subtitles=opensubtitleconnection.SearchSubtitles( session_token, [myquery], {'limit' : 100})
    subdata=subtitles['data']
    i=0
    
    if subdata !=False:
        
        for di in subdata:
            di['fuzzylogic'] =fuzz.token_sort_ratio(filename,di['SubFileName'])
        subdata = sorted(subdata, key=itemgetter('fuzzylogic'),reverse=True)
        i=0
        print "Options:"
        for di in subdata:
            if i>10:
                break
            try :
                print str(i+1)+") :"+di['SubFileName']
            except UnicodeEncodeError:
                continue #add unicode support here
            subtitlesids[i]=di['IDSubtitleFile']
            i+=1
        inp=int(raw_input("\nEnter the one you would like to download:"))

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
        raw_input("[SubDown]: Sorry I am Unable to Find it anyplace i know of\nPress Enter to exit")


    logout=opensubtitleconnection.LogOut( session_token )