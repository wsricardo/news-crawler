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

    def bnRequest(self, url=self.url ):

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

     
    def trackNewsHTMLFile(self, html_content_file, source=''):
        
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


    def __trackNewsBBC(self):

        return None

    def __trackNewsCNN(self):

        return None

    def trackLinks(self):

        return []

if __name__ == "__main__":
    
    with open('data.html', 'r') as fl:
        data = fl.read()
        fl.close()
    
    bot = NewsBot(data)
    a = bot.trackNewsHTMLFile(data, 'g1')
    print( a )