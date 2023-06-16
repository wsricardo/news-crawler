import requests
from bs4 import BeautifulSoup
import random

class CrawlerNews:
    """
        The 'CrawlerNews' is module for get news some news web pages.
        Atributes:
            url - web page address (string)
            attrs - HTML tgas and attributes for get specific content from web pages.

        Functions:

            __init__ -> create object crawler;

            bnRequest -> request for url of web page;

            trackNews -> tracker for news content in web pages;

            trackNewsHTMLFile -> Using local HTML file to get content. File saved in local machine;

            __trackNewsG1 -> private method for get news from site G1/Globo;

            __trackNewsBBC -> private method for get news from site BBC Brasil;

            __trackNewsCNN -> private method for get news from site CNN Brasil;

            trackLinks -> get list news from web page;


    """
    def __init__(self, url=None, attrs=dict() ):
        """
            __init__ -> create object crawler;
        """

        self.url = url 
        self.attrs = attrs

        self.portais = ['G1', 'BBC', 'CNN']
        self.agnews_calls = {
            'g1': self.__trackNewsG1,
            'cnn': self.__trackNewsCNN,
            'bbc': self.__trackNewsBBC,
            'band': self.__trackBandNews
        }

        self.data = None
        self.news = None

    def bnRequest(self, url=None ):
        """
            bnRequest -> request for url of web page;
        """
        if url == None:
            url = self.url

        self.url = url
        return requests.get(url).content.decode()
        
    def trackNews(self, url= None, tag=None, attrs=None):
        """
            trackNews -> tracker for news content in web pages;
        """
        #if url != None:
        #    self.url = url
        
        
        
        if url==None:
            return {'G1': self.__trackNewsG1(), 
                    'CNN': self.__trackNewsCNN(), 
                    'BBC': self.__trackNewsBBC(),
                     'Band': self.__trackBandNews() }
        else:
            aux_link_url = url.split('.')

        if url.find('g1') != -1:
            return self.__trackNewsG1()
        
        elif  url.find('cnn') != -1:
            return self.__trackNewsCNN()

        elif  url.find('bbc') != -1:
            return self.__trackNewsBBC()
        
        elif url.find('band') != -1:
            print('band get\n')
            return self.__trackBandNews()

        else:
            return self.trackLinks()

     
    def trackNewsHTMLFile(self, html_content_file, source=None):
        """
            trackNewsHTMLFile -> Using local HTML file to get content. File saved in local machine;
        """
        if source.lower() == 'g1':
            return self.__trackNewsG1(html_content_file)

        elif source.lower() == 'cnnbrasil':
            return self.__trackNewsCNN( html_content_file )

        elif source.lower() == 'bbc':
            return self.__trackNewsBBC( html_content_file )

        else:
            return None 

    def __trackNewsG1(self, data=None):
        """
            __trackNewsG1 -> private method for get news from site G1/Globo;
        """

        dnews = []
        self.url = 'https://g1.globo.com'
        if data == None and self.url != None:
            data = requests.get(self.url).content.decode()

        elif self.url == None and data == None :
            print("Add data or url.")

        soup = BeautifulSoup(data, 'html.parser')

        cwn = soup.find_all('div', class_='bastian-page')
        
        for i in cwn[0].children:
            for news in i:
               
                dnews.append( { 'title': news.a.text, 'href': news.a['href'] } )
        
        return dnews


    def __trackNewsBBC(self, data=None):
        """
            __trackNewsBBC -> private method for get news from site BBC Brasil;
        """
        bbc_news_lists = []
        self.url = 'https://www.bbc.com/portuguese'
        url_bbc_base = 'https://www.bbc.com'

        if data == None and self.url != None:
            data = requests.get(self.url).content

        elif self.url == None and data == None :
            print("Add data or url.")


        bbc_soup = BeautifulSoup(data, 'html.parser')
        bbc_sections = bbc_soup.find_all('section', class_='bbc-iinl4t')

        for section_news in bbc_sections:
            for news in section_news.select( 'a' ):
                if news['href'].find('topic') != -1:
                    pass
                else :
                    if news['href'].find('https') != -1:
                        bbc_news_lists.extend( [ { 'title': news.text, 'href': news['href'] } ] )
                    else:
                        bbc_news_lists.extend( [ { 'title': news.text, 'href': url_bbc_base+news['href'] } ] )
        
        return bbc_news_lists

    def __trackNewsCNN(self, data = None):
        """
            __trackNewsCNN -> private method for get news from site CNN Brasil;
        """
        cnn_list_news = []
        self.url = 'https://www.cnnbrasil.com.br/'
        if data == None and self.url != None:
            data = requests.get(self.url).content.decode()

        elif self.url == None and data == None :
            print("Add data or url.")

        cnn_soup = BeautifulSoup(data, 'html.parser')
        cnn_nw_data = cnn_soup.find_all('section')

        aux = None

        for news in cnn_nw_data:
            aux = news.find('a')

            try:
                
                aux = aux.attrs
                cnn_list_news.extend( [ 
                    {
                        'title': aux['title'],
                        'href': aux['href']
                    }
                ])

            except:
                pass

        return cnn_list_news

    # Type list of dictionary
    ListDict = list[ dict ]

    def __trackBandNews(self, data = None) -> ListDict:
        """
        data: str [dados] text html
        return list of news with fields 'Title of news' and 'url' for news.
        l = [
        {'title': 'string', 'href': link},
        ...
        ]
        """
        # Lista de notícias
        result = []
        url: str = None

        if data == None:
            url = 'https://www.band.uol.com.br/'

            # Conteúdo do site.
            data = requests.get( url ).content

        # Obtendo conteúdo html
        #band_data = requests.get(url_band).content
        soup_band = BeautifulSoup(data, 'html.parser')
        
        # Primeiro acesso tag main (bloco principal que contêm conteúdos como as noticias principais e seus links.
        # Tag 'main' e class=[home container]. (variável band_main_home)
        band_main_home = soup_band.find_all('main', class_='home')
        
        # Capturando html do bloco maior em main que contêm as noticias.
        soup_band2 = BeautifulSoup( str( band_main_home ) , 'html.parser')
        
        # Este block ( tag:section, class:hardnews) filho da tag main contem dois blocos de noticias a serem tratados insoladamente.
        bmainhardnews = soup_band2.find_all('section', 'hardnews')
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


    def trackLinks(self, url=None, data=None):
        """
            trackLinks -> get list news from web page;
        """
        page_list_links = [] 
        if url == None and data != None:
            soup = BeautifulSoup(data, 'html.parser')
            links = soup.find_all( 'a' )

        elif url != None:
            try:
                data = requests.get( url ).content.decode()
                links = BeautifulSoup( data, 'html.parser').find_all('a')

            except:
                print('Error in url request.')
        else:
            print('Data or url miss.')
            return None
        print('links ', links)
        for i in links:
            try:
                page_list_links.extend( [
                    {
                        'text': i.text or i.content,
                        'href': i['href']
                    }
                ])
            except:
                pass

        return page_list_links
def clean(df):
    import pandas as pd

    # Remove lines specified to link of Twitter
    v = [ 'Política',
        'Pop',
        'Economia',
        'Internacional',
        'Viagem & Gastronomia',
        'Nacional',
        'Saúde',
        'Esportes',
        'CNN Plural',
        'Ciência e Tecnologia',
        'Mercado',
        'Facebook',
        'Twitter',
        'Youtube',
        'YouTube',
        'Instagram' 
    ]

    for i in v:
        df = df.drop( index=df.index[ df['title'] == i ] )
    df = df.drop_duplicates( ignore_index=True ) 

    return df.to_json(orient='records')

def create_list_news(name='out.txt', number_news_per_page = 2, withLinks=True):
    """
        Create list of news from Crawler.
    """
    import datetime
    import json

    urls = { 
        'g1': 'https://g1.globo.com',
        'bbc': 'https://www.bbc.com/portuguese', 
        'cnnbrasil': 'https://www.cnnbrasil.com.br/',
        'band': 'https://www.band.uol.com.br/'
    }

    url_name_replace = { 'g1': 'G1/Globo', 'bbc': 'BBC Brasil', 'cnnbrasil': 'CNN Brasil', 'band': 'Band'  }

    d = CrawlerNews()
    news = []
    keys = urls.keys()
    print(keys)

    if number_news_per_page == 0:
        for i in keys:
            news.extend( d.trackNews( url=urls[i] ) )
    
    elif number_news_per_page > 0:
        for i in keys:
            print('keys',i)
            news.extend( [ { i: random.choices( d.trackNews( url=urls[i] ), k = number_news_per_page ) } ] )

    out = ''
    j = ''
    news = [ 
        { 
        key.replace( 'titulo', 'title' ): value for key, value in i.items() } for i in news 
        ]
    
    news = [ 
        {
            key.replace('url', 'href'):value for key, value in i.items()
        } for i in news
        
    ]
    #print(news)
    import pandas as pd

    df = pd.DataFrame( news )
    print(df)
    news = json.loads( clean(df) )
    
    date = datetime.date.today()
    date = str( date.day ) + '-' + str( date.month ) + '-' + str( date.year )

    with open('/home/opc/news-crawler/datanews/'+ name+'-'+date+'.json', "w") as fl:
        fl.write( json.dumps( news, ensure_ascii=False, indent=4 ) )
        print('save')

if __name__ == "__main__":
    create_list_news("Noticias", 0, True)

