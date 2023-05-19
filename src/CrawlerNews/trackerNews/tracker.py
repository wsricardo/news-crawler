"""
News web page list.
Crawler function for which page.
"""

portal_list = {
    
}

class Tracker:
    """
        Trancker for news.
        Argments:
            data - web page html content (string format)
            args - extra parameters for get specified content from web page ( tags, attributes).
    """

    def __init__(self, data, **args):
        self.data = data
        self.args = args

    def __repr__(self):
        return f"{self.data}, {self.args}"
    
    def trackmain(self):
        """
        Get content webpage for list tags/attribute for specified contents.
        """
        result = None

        return result