import requests
from bs4 import BeautifulSoup
import random

class NewsBot:
    def __init__(self, url=None, attrs=dict() ):

        self.url = url 
        self.attrs = attrs
        

        self.agnews_calls = {
            'g1': self.__trackNewsG1,
            'cnn': self.__trackNewsCNN,
            'bbc': self.__trackNewsBBC
        }

    def bnRequest(self, url=None ):
        if url == None:
            url = self.url

        return requests.get(url).content.decode()
        
    def trackNews(self, url= None, tag=None, attrs=None):
        
        #if url != None:
        #    self.url = url
        
        aux_link_url = url.split('.')
        
        

        if url.find('g1') != -1:
            return self.__trackNewsG1()
        
        elif  url.find('cnn') != -1:
            return self.__trackNewsCNN()

        elif  url.find('bbc') != -1:
            return self.__trackNewsBBC()

        else:
            return self.trackLinks()

     
    def trackNewsHTMLFile(self, html_content_file, source=None):
        
        if source.lower() == 'g1':
            return self.__trackNewsG1(html_content_file)

        elif source.lower() == 'cnnbrasil':
            return self.__trackNewsCNN( html_content_file )

        elif source.lower() == 'bbc':
            return self.__trackNewsBBC( html_content_file )

        else:
            return None 

    def __trackNewsG1(self, data=None):

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

    def trackLinks(self, url=None, data=None):
        page_list_links = [] 
        if url == None and data != None:
            soup = BeautifulSoup(data, 'html.parser')
            links = soup.find_all( 'a' )

        elif url != None:
            try:
                data = requests.get( url ).content.decode()
                links =BeautifulSoup( data, 'html.parser').find_all('a')

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

def create_list_news(name='out.txt', number_news_per_page = 2, withLinks=True):
    import datetime
    import json

    urls = { 'g1': 'https://g1.globo.com',
        'bbc': 'https://www.bbc.com/portuguese', 
        'cnnbrasil': 'https://www.cnnbrasil.com.br/'
    }

    url_name_replace = {'g1': 'G1/Globo', 'bbc': 'BBC Brasil', 'cnnbrasil': 'CNN Brasil'  }

    d = NewsBot()
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
    print(news)
    """if withLinks:
        for i in news:

            j = [ s for s in i.keys()][0]
          
            out += f"Portal de Notícias { url_name_replace[j] }\n"
            for k in i[j]:
                out += k['title'] + '.'  + '\n' + k['href'] + '\n'
            out += '\n\n'
    else:
        for i in news:

            j = [ s for s in i.keys()][0]

            out += f"Portal de Notícias { url_name_replace[j] }\n"
			
            for k in i[j]:
                out += k['title'] + '.' + '\n'

            out += '\n\n'
    """

    date = datetime.date.today()
    date = str( date.day ) + '-' + str( date.month ) + '-' + str( date.year )

    with open(name+'-'+date+'.json', "w") as fl:
        fl.write( json.dumps( news, ensure_ascii=False, indent=4 ) )
        print('save')

if __name__ == "__main__":
    create_list_news("Noticias", 0, True)

    """with open('data.html', 'r') as fl:
        data = fl.read()
        fl.close()
    
    bot = NewsBot(data)
    a = bot.trackNewsHTMLFile(data, 'g1')
    print( a )
    for i in a :
        print(f'\n\n{i["title"]}\n{i["href"]}')
    with open('links.txt', 'w') as fl:
        fl.write( '\n'.join( [ str( i['text'] ) + ' , ' + str( i['href'] )  for i in bot.trackLinks('https://www.band.uol.com.br') ] ) )
        fl.close()
    """
