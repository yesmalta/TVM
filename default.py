"""
	This plugin has been programmed by Dr Ing. Jeffrey J. Micallef and Dr Ing. Brian W. Micallef
"""
import sys
import resources.lib.plugin as plugin
#import resources.lib.settings as settings
import resources.lib.model.arguments as arguments

import sys
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading

if __name__ == "__main__":
    plugin.init()
    #settings.init()
    import resources.lib.TVM3 as TVM3

    args_map = arguments.parse_arguments(sys.argv[2])
    TVM3.Main(args_map=args_map).run()

sys.modules.clear()
