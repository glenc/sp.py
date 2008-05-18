# applytheme.py
# 
# This script will apply the specified theme to all
# webs in the specified web application.  It will
# iterate through each site collection in the web
# application, then iterate through each web in the
# site collection applying the theme to that web

import sp

def apply_theme(url, theme, force=False):
	"""Applies the theme to all webs within the web application"""
	
	def do_work(web):
		if web.Theme != theme or force == True:
			print "Applying theme to", web.Url
			web.ApplyTheme(theme)
	
	# iterate over all sites, then all webs
	sp.enum_sites(url, 
		lambda s: 
			sp.enum_all_webs(s, do_work))



if __name__ == '__main__':
	import sys

	if len(sys.argv) == 1:
		print HELPSTRING
	else:
		apply_theme(sys.argv[1], sys.argv[2], False)



HELPSTRING = """
Apply Theme
This script will apply the specified theme to all webs in the
specified web application.

Usage:

	ipy applytheme.py http://myserver Petal

Arguments:

	url   - web application url
	theme - theme to apply

"""