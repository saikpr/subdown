from subdown_version import __version__
introstr="""


  _________       ___.    ________                            
 /   _____/ __ __ \_ |__  \______ \    ____  __  _  __  ____  
 \_____  \ |  |  \ | __ \  |    |  \  /  _ \ \ \/ \/ / /    \ 
 /        \|  |  / | \_\ \ |    `   \(  <_> ) \     / |   |  \ 
/_______  /|____/  |___  //_______  / \____/   \/\_/  |___|  /
        \/             \/         \/                       \/  v"""+__version__+"""
                            BY

  _________        .__                                 
 /   _____/_____   |__|  ____   ___.__._____     _____  
 \_____  \ \__  \  |  | /    \ <   |  |\__  \   /     \ 
 /        \ / __ \_|  ||   |  \ \___  | / __ \_|  Y Y  \ 
/_______  /(____  /|__||___|  / / ____|(____  /|__|_|  /
        \/      \/          \/  \/          \/       \/ 
Visit Me at : https://sainyamkapoor.github.io
For more info Regarding this app Visit : http://sainyamkapoor.github.io/SubDown

"""

"""Code begins"""

from os import path, remove
from urllib2 import ProxyHandler,HTTPBasicAuthHandler, build_opener, HTTPHandler, install_opener
from sys import argv
from sub_db_down import sub_db
from open_sub_down import open_sub
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

if __name__=='__main__': 
    try:
        arg_path = argv[1]
        filename=arg_path.split('\\')[-1]
    except IndexError :
        raw_input("No arguments Passed \n Press Enter to exit")
        arg_path=None
    replace = [".avi",".mp4",".mkv",".mpg",".mpeg"]
    clean_path=arg_path
    print introstr
    for content in replace:
        filename = filename.replace(content,'')
        clean_path = clean_path.replace(content,"")
    print "[SubDown]: Trying to Download " +filename
    if path.exists(clean_path+".srt"):
        ans=str(raw_input("Looks Like the SRT file exist\nWould You like To delete that file and Download a new one? :"))
        ans=ans.lower()
        if ans=='y' or ans=='yes':
            remove(clean_path+".srt")
        else :
            exit(0)
    if sub_db(arg_path,opener)==0:
        open_sub(clean_path,filename,arg_path)
