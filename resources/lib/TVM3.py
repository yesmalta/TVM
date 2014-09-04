import sys
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading, urllib2

site = 'http://www.tubegalore.com'

def get_list(body, mappings, title_fmt, link_fmt, thumb_fmt):
    for indx in range(0, len (mappings)-1):
        body = re.compile(mappings[indx],re.DOTALL).findall(body)[0]
        
    indx = indx + 1;
    if (mappings[indx] == '-'):
        match = body
    else:
        match = re.compile(mappings[indx],re.DOTALL).findall(body)
    
    output = []
    
    for element in match:
        link = link_fmt[:]
        title = title_fmt[:]
        thumb = thumb_fmt[:]
    
        if (True):
            for i in range (0, len(element)):
                #print('%%' + str(i) + '%%' == link_fmt)
                link = link.replace('%%' + str(i) + '%%', element[i])
                title = title.replace('%%' + str(i) + '%%', element[i])
                thumb = thumb.replace('%%' + str(i) + '%%', element[i])
        else:
            #print('%%' + str(i) + '%%' == link_fmt)
            link = link.replace('%%0%%', element)
            title = title.replace('%%0%%', element)
            thumb = thumb.replace('%%0%%', element)
                
            
        output.append((link, title, thumb))              
                                          
    return output

def resolve_url(url):

	if ("www.porntubevidz.com" in url):
		# Get the proper url of site
		sites = ""
		for (a,b) in re.compile("http(.*?)www.porntubevidz.com(.*)",re.DOTALL).findall(url):
			sites = urllib.unquote("http" + a + "www.porntubevidz.com" + b)
		
		# load the site
		response = urllib2.urlopen(sites)
		response = (response.read()).decode('UTF-8', "strict")
		response = response.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','').replace('&rarr;','')

		for url_string in re.compile("video_url: '(.+?)',",re.DOTALL).findall(response):
			url_string = url_string
			
		return url_string
	elif ("www.tnaflix.com" in url):
		sites = ""
		for (a,b) in re.compile("http(.*?)www.tnaflix.com(.*)",re.DOTALL).findall(url):
			sites = urllib.unquote("http" + a + "www.tnaflix.com" + b)
		
		# load the site
		response = urllib.urlopen(sites)
		response = (response.read()).decode('UTF-8', "strict")
		response = response.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','').replace('&rarr;','')
		
		for url_ID in re.compile("javascript: shareVideo\('(.*?)',",re.DOTALL).findall(response):
			url_ID = url_ID

		# Get the proper video info from 
		sites = "http://cdn-fck.tnaflix.com/tnaflix/" + url_ID + ".fid"
		
		response = urllib2.urlopen(sites)
		response = (response.read()).decode('UTF-8', "strict")
		response = response.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','').replace('&rarr;','')

		url_string = ""
		for url_string in re.compile("<videoLink>(.*?)1080p",re.DOTALL).findall(response):
			url_string = url_string + "1080p"
		
		if (url_string == ""):		
			for url_string in re.compile("<videoLink>(.*?)720p",re.DOTALL).findall(response):
				url_string = url_string + "720p"
			
		if (url_string == ""):		
			for url_string in re.compile("<videoLink>(.*?)360p",re.DOTALL).findall(response):
				url_string = url_string + "360p"
				
		if (url_string == ""):		
			for url_string in re.compile("<videoLink>(.*?)240p",re.DOTALL).findall(response):
				url_string = url_string + "240p"
				
		if (url_string == ""):		
			for url_string in re.compile("<videoLink>(.*?)tna<",re.DOTALL).findall(response):
				url_string = url_string + "tna"
		
		return url_string
	elif ("privatehomeclips" in url):
		
		# Get the proper url of site
		sites = ""
		for (a,b) in re.compile("http(.*?)privatehomeclips.com(.*)",re.DOTALL).findall(url):
			sites = urllib.unquote("http" + a + "privatehomeclips.com" + b)
		
		# load the site
		response = urllib.urlopen(sites)
		response = (response.read()).decode('UTF-8', "strict")
		response = response.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','').replace('&rarr;','')

		for url_string in re.compile("video_url: '(.+?)',",re.DOTALL).findall(response):
			url_string = url_string
		
		return url_string
	else:
		return "NAN"

def addNavMenu(ListInfo, mode, is_Folder):
	for (title_list, link_list, thumb_list) in ListInfo:
		if not(thumb_list == ""):
			li = xbmcgui.ListItem(title_list, iconImage=thumb_list, thumbnailImage=thumb_list)
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?' + "url=" + urllib2.quote(link_list) + "&mode=" + str(mode), listitem=li, isFolder=is_Folder, totalItems=1)
		else:
			li = xbmcgui.ListItem(title_list, iconImage="", thumbnailImage="",)
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?' + "url=" + urllib2.quote(link_list) + "&mode=" + str(mode), listitem=li, isFolder=is_Folder, totalItems=1)
	xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))

# The Main Plugin Starts HERE

class Main:

    def __init__(self, args_map):
        self.args_map = args_map

    def run(self):
		
		if 'mode' not in self.args_map:
			# Home page
			response = urllib2.urlopen(site)
			response = (response.read()).decode('UTF-8', "strict")
			response = response.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','').replace('&rarr;','')

			list = get_list(response, ['<h2>Porn Categories</h2>(.*)', '<a href=\"(.*?)\" target="_blank">([^<>]*?)</a>(.*?)<br />'], "http://www.tubegalore.com%%0%%", "%%1%% %%2%%", "")
			addNavMenu(list, 2, True)
		else:
			if (self.args_map['mode'] == '2'):
				# open the search result 
				# Get search ID
				#list = [(self.args_map['url'],"",""),("title2","","")]
				for (kwid, c) in re.compile("&kwid=([0-9]+?)&c=([0-9]+?)",re.DOTALL).findall(self.args_map['url']):
					ID = kwid + "-" + c
					sites = "http://www.tubegalore.com/-tube/" + ID + "/page0/"
					response = urllib2.urlopen(sites)
					
					response = (response.read()).decode('UTF-8', "strict")
					response = response.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','').replace('&rarr;','')
					
					list = get_list(response, ['Next Page</a>(.*)<h2>Categories</h2>', 'span=2><a href=\"(.*?)\" target="_blank">([^<]*?)</a>.*?class="thumb" target="_blank">.*?src=\"(.*?)\"'], "%%0%%", "%%1%%", "%%2%%")
					addNavMenu(list, 3, False)
				
			elif (self.args_map['mode'] == '3'):
				# Resolve URL
				#stream_url = "http://www.html5videoplayer.net/videos/toystory.mp4"
				stream_url = resolve_url(self.args_map['url'])		
				
				#list = [(stream_url,"",""), ("title2","","")]
				#addNavMenu(list, 4, True)
				
				#infoL={'Title': 'title_here', 'Plot': '', 'Genre': '', 'originaltitle': ''}
				
				# play with bookmark
				#stream_url=stream_url.replace(' ','%20')
				from resources.universal import playbackengine
				player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id='', video_type='', title=self.args_map['url'].replace(':::','?').replace('::','&'), season='', episode='', year='',img='',infolabels='', watchedCallbackwithParams='',imdb_id='')
				player.KeepAlive()