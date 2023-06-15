import requests
import trackers
import json
import pandas as pd

class Crawler:
    
    """
        The 'CrawlerNews' is module for get news some news web pages.

        Atributes:

            url - web page address (string)
            attrs - HTML tgas and attributes for get specific content from web pages.
            rs -> create object for Session in request
            attr -> extra attributes
            args -> arguments list
            kwargs -> argument list in dictionary. Example: { 'name' : 'value'} .
            _text -> text html
            tracker -> Load module with functions for tracker sites.
            

        Functions:

            __init__ -> create object crawler;
            get -> get html from web page; parameter 'url'.
            track -> get list news from web page, generic functions;
            toJSON -> return json for content lists
            cleandataframe -> clean content in dataframe, recovery news
            save -> Save list news to json
            text -> html from page (text format string). Property.
            dataframe -> DataFrame with list news | ttitle | href | fields.

    """
    

    def __init__(self, url=None, attrs=None, *args, **kwargs):

        self.url = url
        self.data = None
        self.rs = requests.Session()
        self.attrs = attrs
        self.args = args
        self.kwargs = kwargs
        self._text = ''
        self.tracker = trackers
    
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

    def cleandataframe(self, df):
        """
            Clean DataFrame with list news.
        """
        return df
    
    def save(self, jsonfile):
        """
            Save list news in file json.
        """
        
    @property
    def text(self):
        """
        HTML content of page.
        """
        return self.data.text if self.data != None else self.rs.get(self.url).text
    
    @property
    def dataframe(self):
        """
        Return a dataframe with table news.
        """
        df = None
        
        return df
        
        
if __name__=='__main__':
    print('Module Crawler News version 2.\n')
    c = Crawler('https://g1.globo.com')
    c.get()
    print(c.data.content.decode())