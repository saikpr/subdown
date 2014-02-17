
"""Proxy settings"""
proxy_url=''
username=''
password=''


"""Code begins"""
import os
import hashlib
import urllib2
import sys
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
        except urllib2.HTTPError:
            print("shit happened")
            exit(0)
        with open (path+".srt","wb") as subtitle:
            subtitle.write(response)

path = sys.argv[1]
sub_downloader(path)
