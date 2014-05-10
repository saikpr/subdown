import os
from hashlib import md5
from urllib2 import Request , URLError
def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return md5(data).hexdigest()

def sub_db(path,opener):

    hash = get_hash(path)
    replace = [".avi",".mp4",".mkv",".mpg",".mpeg"]
    for content in replace:
        path = path.replace(content,"")
    
    if not os.path.exists(path+".srt"):
        headers = { 'User-Agent' : 'SubDB/1.0 (SubDown/0.1; http://github.com/sainyamkapoor/SubDown)' }
        url = "http://api.thesubdb.com/?action=download&hash="+hash+"&language=en"
        req = Request(url, '', headers)
        try:
            response = opener.open(req).read()
        except URLError as urler:
            
            try:
                k=urler.code
                print("[SubDown]: I am not able to find it\nManual Mode:ON\nPlease select the Best option as you feel like")
            except AttributeError:
                raw_input ("[SubDown]: Internet not working or maybe unable to find connection to primary server\nSuggestion:Try using it with Proxifier\nPress Enter to Exit")
                exit(0)
            return 0
        
        with open (path+".srt","wb") as subtitle:
            subtitle.write(response)
            return 1