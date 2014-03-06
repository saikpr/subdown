import xmlrpclib
from cStringIO import StringIO
from base64 import b64decode
from gzip import GzipFile

subtitlesids={}
opensubtitleurl = "http://api.opensubtitles.org/xml-rpc"
opensubtitleconnection = xmlrpclib.ServerProxy( opensubtitleurl )
allpages = opensubtitleconnection.LogIn( '', '', 'en', 'OS Test User Agent')
print allpages
session_token=allpages['token']
myquery={'query' : 'Nasha (2013) Hindi DvDRip 720p 5.1 x264 MaNuDiL SilverRG', 'sublanguageid' : 'all'}
subtitles=opensubtitleconnection.SearchSubtitles( session_token, [myquery], {'limit' : 10})
file2=open('ip','w')
file2.write(str(subtitles))
file2.close()
subdata=subtitles['data']
i=0
for di in subdata:
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
file2=open('ip2','w')
file2.write(str(orig_file_cont))


logout=opensubtitleconnection.LogOut( session_token )


""",{'moviehash' : '18379ac9af039390', 'moviebytesize' : 366876694}
   {'imdbid' : '1129442', 'sublanguageid' : 'eng'},
   {'query' : 'Cocktail (2012) BRRip 720p X264 Ac3 5.1 Audio Channel {{Niliv}} -=-  {{{TMRG}}}', 'sublanguageid' : 'all'},
   {'moviehash' : '18379ac9af039390', 'moviebytesize' : 366876694},"""