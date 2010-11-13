#!/usr/bin/env python
from resources.lib.xbmcvideoplugin import XBMCVideoPlugin, urlread, parse_qs
from urllib import unquote_plus
from BeautifulSoup import BeautifulSoup as BS, SoupStrainer as SS
import re

class ClassicCinema(XBMCVideoPlugin):
    base_url = 'http://www.classiccinemaonline.com'
    genres_url = 'http://www.classiccinemaonline.com/1/index.php'

    def display_genres(self, url):
        src = urlread(url)
        #fix terrible html
        src = src.replace('</font color>', '</font>')
        src = src.replace(r'<ol class=\"latestnews \">', '<ol class="latestnews">')

        div_tag =  BS(src, parseOnlyThese=SS('div', {'id': 'rightcol'}))
        dirs = [{'name': a.span.string.replace('&amp;', '&'),
                 'url': self._urljoin(a['href']),
                 'mode': '1'}
                 for a in div_tag.find('div', {'class': 'moduletable'})('a')]
        print dirs

    def display_movies(self, url):
        pass

    def run(self, mode, url):
        #must pass default values for mode and url, mode is '0', url is ''
        mode_functions = {'0': self.display_genres,
                         '1': self.display_movies,
                         }
        mode_functions[mode](url)

    
if __name__ == '__main__':
    #if being run from the comman line, import sys, else it is already imported
    try:
        sys
    except NameError:
        import sys

    #parse command line parameters into a dictionary
    params = parse_qs(sys.argv[2])
    
    #create new app
    app = ClassicCinema(sys.argv[0], sys.argv[1])
    
    #run the app
    app.run(params.get('mode', '0'),
            unquote_plus(params.get('url', app.genres_url)))



