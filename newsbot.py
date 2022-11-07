import requests
from bs4 import BeautifulSoup 

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
        
    def trackNews(self, tag=None, attrs=None):

        aux_link_url = self.url.split('.')
        

        if [ l.find('g1') for l in aux_link_url ] != [-1, -1, -1]:
            return self.__trackNewsG1()
        
        elif  [ l.find('cnn') for l in aux_link_url ] != [-1, -1, -1]:
            return self.__trackNewsCNN()

        elif  [ l.find('bbc') for l in aux_link_url ] != [-1, -1, -1]:
            return self.__trackNewsBBC()

        else:
            return self.trackLinks()

     
    def trackNewsHTMLFile(self, html_content_file, source=None):
        
        if source.lower() == 'g1':
            return self.__trackNewsG1(html_content_file)

        elif source.lower() == 'cnn':
            return self.__trackNewsCNN( html_content_file )

        elif source.lower() == 'bbc':
            return self.__trackNewsBBC( html_content_file )

        else:
            return None 

    def __trackNewsG1(self, data):

        dnews = []
        #data = requests.get(self.url)
        soup = BeautifulSoup(data, 'html.parser')

        cwn = soup.find_all('div', class_='bastian-page')
        #print( cwn[0] )
        for i in cwn[0]:
            for news in i:
               # print(news.a.text)
                dnews.append( { 'title': news.a.text, 'href': news.a['href'] } )
        
        return dnews


    def __trackNewsBBC(self, data):
        bbc_list_news = []
        url_bbc_base = 'https://www.bbc.com'

        bbc_soup = BeautifulSoup(data, 'html.parser')
        bbc_sections = bbc_soup.find_all('section', class_='bbc-iinl4t')

        for sections_news in bbc_sections:
            for news in section_news.select( 'a' ):
                if news['href'].find[ 'topic' ] != -1:
                    bbc_list_news.extend( [
                        {
                            'title': news.text,
                            'href': news['href']
                        }
                    ])
                    
                else:
                    bbc_list_news.extend( [
                        {
                            'title': news.text,
                            'href': url_bbc_base+news['href']
                        }
                    ])
        return bbc_list_news

    def __trackNewsCNN(self, data):
        cnn_list_news = []

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
            except:
                print('Error in url request.')
        else:
            print('Data or url miss.')
            return None

        for i in links:
            page_list_links.extend( [
                {
                    'text': i.text,
                    'href': i['href']
                }
            ])

        return page_list_links

if __name__ == "__main__":
    
    with open('data.html', 'r') as fl:
        data = fl.read()
        fl.close()
    
    bot = NewsBot(data)
    a = bot.trackNewsHTMLFile(data, 'g1')
    print( a )
    for i in a :
        print(f'\n\n{i["title"]}\n{i["href"]}')