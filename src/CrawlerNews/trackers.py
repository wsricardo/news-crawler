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



def trackerBand( contentHTML ):
    """
        News for web page Band
        Site: 'https://www.band.uol.com.br/'
    """

    result = [ ]
    soup = BeautifulSoup( contentHTML )

    # Primeiro acesso tag main (bloco principal que contêm conteúdos como as noticias principais e seus links.
    # Tag 'main' e class=[home container]. (variável band_main_home)
    main_home  = soup.find_all('main', 'html.parser')

    # Capturando html do bloco maior em main que contêm as noticias.
    soup_band = BeautifulSoup( str( main_home ), 'html.parser' )

    # Este block ( tag:section, class:hardnews) filho da tag main contem dois blocos de noticias a serem tratados insoladamente.
    bmainhardnews = soup_band.find_all('section', 'hardnews')
    soup_blocknews = BeautifulSoup( str( bmainhardnews[0] ), 'html.parser' )
    bn1 = soup_blocknews.find_all( 'div', class_='hardnews__highlight' )

        
    soup_links_news = BeautifulSoup(str( bn1 ), 'html.parser') 
    bn1_link_news = soup_links_news.find_all( 'a'  )#, class_= [ 'link image','related', 'link']  ) 
    bn2 = soup_blocknews.find_all( 'div', class_='cards' )

    soup2bn2 = BeautifulSoup( str( bn2[0] ), 'html.parser' ) 
    bn2_cards_links = soup2bn2.find_all( 'a' )
        
    # Lista de links de notícias no bloco {tag: div, class_: 'hardnews__highlight' } do HTML.
    for i in bn1_link_news:
        result.append( { 'title': i.text, 'href': i['href'] } )
        #print('\n> ', i.text +'\n | '+i['href'])
            
    for i in bn2_cards_links:
        result.append( { 'title' : i['title'], 'href':  i['href'] } )
        #print('\n> ', i['title'] +'\n | '+i['href'])
        
    return result


def trackerBBC( contentHTML ):
    bbc_news_lists = []
    url = 'https://www.bbc.com/portuguese'
    url_bbc_base = 'https://www.bbc.com/'

    soup = BeautifulSoup( contentHTML, 'html.parser' )
    bbc_sections = soup.find_all( 'section', class_='bbc-iinl4t' )

    for section_news in bbc_sections:
        for news in section_news.select( 'a' ):
            if news[ 'href' ].find( 'topic' ) != -1:
                pass
            else:
                if news[ 'href' ].find( 'https' ) != -1:
                    bbc_news_lists.extend( [ { 'title': news.text, 'href': news[ 'href' ] } ])
                else:
                    bbc_news_lists.extend( [ { 'title': news.text, 'href': url_bbc_base+news['href'] } ] )

    return bbc_news_lists
   
def trackerCNN( contentHTML ):
    """
    Get news from page CNN Brasil.
    Corrigir obter lista news.
    """
    cnn_list_news = [ ]
    url = 'https://www.cnnbrasil.com.br/'

    soup = BeautifulSoup( contentHTML, 'html.parser' )
    cnn_nw_data = soup.find_all( 'section' )

    aux = None

    for news in cnn_nw_data:
        aux = news.find( 'a' )

        try:

            aux = aux.attrs
            cnn_list_news.extend( [
                {
                    'title': aux[ 'title' ],
                    'href': aux[ 'href' ]
                }
            ])

        except:
            pass

    return cnn_list_news 

def trackerFolhaSP():
    return None

def builderJSONContent(url ):
    return None