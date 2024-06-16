from bs4 import BeautifulSoup

def tracker( htmlcontent: str ): -> list[dict]:
    """
    Track página da "Folha de São Paulo"
    """
    fsp_editoriais = ( 
            ('Em Cima Da Hora', 'https://feeds.folha.uol.com.br/emcimadahora/rss091.xml'),
            ('Opinião', 'https://feeds.folha.uol.com.br/opiniao/rss091.xml' ) ,
            ( 'Política', 'https://feeds.folha.uol.com.br/poder/rss091.xml') ,
            ('Mundo', 'https://feeds.folha.uol.com.br/mundo/rss091.xml'),
            ('Mercado','https://feeds.folha.uol.com.br/mercado/rss091.xml'),
            ('Cotidiano','https://feeds.folha.uol.com.br/cotidiano/rss091.xml'),
            ('Educação', 'https://feeds.folha.uol.com.br/educacao/rss091.xml'),
            ('Equilíbrio', 'https://feeds.folha.uol.com.br/equilibrio/rss091.xml'),
            ('Esporte','https://feeds.folha.uol.com.br/esporte/rss091.xml'),
            ('Ilustrada', 'https://feeds.folha.uol.com.br/ilustrada/rss091.xml'),
            ('Ilustríssima','https://feeds.folha.uol.com.br/ilustrissima/rss091.xml'),
            ('Ciência','https://feeds.folha.uol.com.br/ciencia/rss091.xml'),
            ('Ambiente','https://feeds.folha.uol.com.br/ambiente/rss091.xml'),
            ('Tec','https://feeds.folha.uol.com.br/tec/rss091.xml'),
            ('Comida','https://feeds.folha.uol.com.br/comida/rss091.xml'),
            ('Saúde','https://feeds.folha.uol.com.br/equilibrioesaude/rss091.xml'),
            ('Folhinha','https://feeds.folha.uol.com.br/folhinha/rss091.xml'),
            ('Turismo','https://feeds.folha.uol.com.br/turismo/rss091.xml'),
        )

    fsp_feeds =  ( 
            { 'Editorial': j[0], 'FeedData': fp.parse( j[1] ) } 
                for j in fsp_editoriais  
        )  

    # Lista de editoriais com suas respectivas listas de notícias. Para cada editorial extraido um lista de notícias.
    fsp_news_list = (
            { 
                'Editorial': i[ 'Editorial' ],
                'Noticias': ( { 
                    'Title': j.title,
                    'Summary': j.summary,
                    'href': j['link'].split('*')[1]
            }  for j in i[ 'FeedData' ].entries )
            } for i in fsp_feeds 
    )

    return  fsp_news_list 
    

def trackFolhaSP( htmlcontent ) -> list[dict]:
    """
    Concatenat Editorials news.
    """
    fsp = tracker( htmlcontent )
    
    folhasp = []
    for i in fsp:
        for j in i['Noticias']:
            folhasp.append (
                {
                    'Title': j['Title'],
                    'Sumary': j['Summary'],
                    'Editorial': i['Editorial'],
                    'href': j['href']
                }
            )
    