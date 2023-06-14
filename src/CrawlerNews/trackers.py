# Tracker read urls datas
# Functions for get data from web page
# Register tracker for page.
from bs4 import BeautifulSoup


"""
Tracker read urls for get data from web page.
"""


pages = {
        '0': ('Globo/G1', 'https://g1.globo.com' ),
        '1': ( 'BBC Brazil','https://www.bbc.com/portuguese' ),
        '2': ( 'CNN Brazil', 'https://www.cnnbrasil.com.br/' ),
        '3': ( 'Band', 'https://www.band.uol.com.br' ),
}
params = {}
attrs = {}
    
def trackerG1( contentHTML ):
    """
        News for web page G1/Globo
        Site:  https://g1.globo.com

        contentHTML - html of web page (text format, string )
    """

    url = 'https://g1.globo.com'

    soup = BeautifulSoup(contentHTML, 'html.parser')

    news_block = soup.find_all('div', class_='bastian-page')

    for i in news_block[0].children:
        for news in i:
            yield { 'title': news.a.text, 'href': news.a['href'] }



def trackerBand():

    return None

def trackerBBC():
    return None

def trackerCNN():
    return None

def trackerFolhaSP():
    return None

def builderJSONContent(url ):
    return None