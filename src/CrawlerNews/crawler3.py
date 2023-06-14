import requests
import trackers
import json

class Crawler:
    
    """
        The 'CrawlerNews' is module for get news some news web pages.

        Atributes:

            url - web page address (string)
            attrs - HTML tgas and attributes for get specific content from web pages.

        Functions:

            __init__ -> create object crawler;
            track -> get list news from web page;

    """

    def __init__(self, url=None, attrs=None):
        self.url = url
        self.data = None
        self.rs = requests.Session()

    def __get__(self):
        return {'url':self.url, 'data': self.data}
    
    def get(self, url=None):
        """
            get page content
        """
        
        if url != None:
            self.url = url

        self.data = self.rs.get(self.url)

    def track(self, func, *args):
        """
        Track get data content in data.
        Generic functions. 
        """

        return func( args )
    
    def toJSON(self, *args):
        return 0


if __name__=='__main__':
    print('MOdule Crawler News version 2.\n')
    c = Crawler('https://g1.globo.com')
    c.get()
    print(c.data.content.decode())