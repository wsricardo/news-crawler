# Crawler Noticias do G1

Capturando noticias do portal G1 da Globo

Estudo projeto de construção de um bot crawler para extrair e indexar noticias de sites.

É recomendavel baixar uma única vez o html do site para reduzir a necessidade de acessar o site várias vezes para cada processamento reduzindo tempo e custo computacionais para máquina local e servidor.

Usamos módulo _Requests_ para baixar o html da página a ser processada e com módulo _BeautifulSoup_ processamos o conteúdo html buscando por conteúdos especificos. Ao inspecionar o código HTML verificamos em quais blocos estão as principais noticias - em geral em tags como "section", "h1"/"h2"/"h3" e "a" - considerando o seletor css que especifica cada bloco de interesse afim de refinar a busca e garantir que serão extraindos os trechos relevantes.

Sites com boas práticas de HTML/CSS tendem a serem mais faceis de serem processados e indexados por mecanismos de buscas facilitando os usuários em encontrar seus conteúdos em pesquisas aumentando assim o engajamento em suas plataformas contribuindo para seu melhor desenvolvimento.

Neste presente momento o projeto está considerando três portais de notícias que são _BBC Brasil_, _CNN Brasil_ e _G1/Globo_. 

Créditos e direitos reservados às referentes plataformas mencionadas.

(Obs.: Conteúdo livre com fins informativos e de divulgação. )


## Módulos

Abaixo _import_ dos módulos que contém os recursos usados.

* BeautifulSoup
* Requests
* re (regular expression)
* crawlernewsg1 (acessa site e extrai lista de principais noticias na página principal do site)
* IPython.core.display -> display, HTML (renderiza conteúdos html )


```python
from bs4 import BeautifulSoup
import requests
import re
from crawlernewsg1 import *
import random

# Render html content
from IPython.core.display import display, HTML
```

## Modelagem Portal G1

Funções básicas. Especifincando "selector css" classe 'bastian-page'  para tags div.


```python
# Baixando html do portal de noticia para processamento e salvando em disco.
url = 'https://g1.globo.com'
attr = {'class': 'bastian-page'}
data = g1_(requests.get( url ).content, 'div', attr)
dw = requests.get('https://g1.globo.com/').content
with open('tmp/data', 'w') as fl:
    fl.write( dw.decode() )
    
```


```python
class G1:
    def __init__(self, size_news=10, include_details = False):
        self.size_news = size_news
        self.include_details = include_detais
        self.url = 'https://g1.globo.com/'
        self.hdata = ''
        self.htag = 'div'
        self.attr={'class': '_b', 'id':''}
        self.dnews = []
        self.soup = ''
        
    def g1_():
        pass
        
        
```


```python
dw, cwn = g1_( dw, 'div', attr)
```


```python
print(dw[0]['url'])
news1 = requests.get( dw[0]['url'] ).content

#print(news1)
soup = BeautifulSoup(news1, 'html.parser')

# Extração do título da notícia.
cwn2 = soup.find_all( 'p', {'class': 'content-text__container'} )
cwn_title = soup.find_all( 'h1', {'class': 'content-head__title'} )
print("\n")

print( dw[0].keys() )
#print(f"\n <b>{dw[0]['titulo']}</b>\n\n Page: {dw[0]['url']}")
display(HTML( f"""\n <b>{dw[0]['titulo']}</b>\n\n<br><br> Page: <a href="{dw[0]['url']}"> G1/Globo """))



```


```python
#soup1 = BeautifulSoup
dw


```

Ao abrir link da noticia pesquisar pela tag *'p'* com atributos **class** com valor **"content-text__container** definir o tamanho para caso extrair só parte do corpo do texto.


Retornando uma lista dos itens encontrados (como visto acima no código) pegamos estes itens e os concatenamos exibintido o texto no corpo da noticia. (_Como visto abaixo_)


```python
# Display news 
#news = '<h1 style="font-size: 28px; padding: 12px; text-align: center; margin: 0 auto;">Notícia Do Dia </h1><br>'
#news += ''.join([  str(i) for i in cwn ] )
#display( HTML( news ))

```

Cada "_evt" (_css selector_ class) class css em "bastian-page" refere-se a uma noticia na lista central de noticias.
Dentro de cada "_evt" haverá "bastian-feed-item" e neste o feed-post. 

**feed-post-body** _contêm_  ( 'feed-post-link', 'feed-post-body-title', 'feed-post-body-resumo')

**bastian-feed-item** _contem_ um feed-post-body referindo-se a cada item (noticia)


Para link da noticia (quando acessando a noticia)

**content-head__title** em tag 'h1' (Título da noticia)

**content-head__subtitle** em tag 'h2' (subtitulo/resumo da noticia)

**content-text__container** corpo do texto da noticia css-selector, tag 'p' (pegar só a primeira referente ao primeiro paragrafo da noticia)


```python
#text_news = '\n '.join([i.text for i in cwn ])
#print(text_news)
#help( cwn[0] )
#dir(cwn[0])

#dir(cwn[0])
#print('bastian-feed-item', cwn[0].contents[0].select( ".bastian-feed-item") )

nw = cwn[0].contents[0].select('._evt')
print( nw[3].contents )
nw2 = cwn[0].contents[0].select('.bastian-feed-item')
print('Número de noticias %s'%len(nw2) )


#( nw2[0].select('.feed-post-body-title')[0].text, nw2[0].select('.feed-post-body-resumo' )[0].text , nw2[0].select('.feed-post-link')[0]['href'] )

#l = [ i.text for i in  [ j.select('.feed-post') for j in cwn[0].contents[0].select('.bastian-feed-item') ] ]
#l[0]
#nw2[1].select('.feed-post-body-title')[0].text
#nw2[1].select('.feed-post-body-resumo' )[0].text
#nw2[1].select('.feed-post-link')
nws = [  {'titulo': i.select('.feed-post-body-title'), 
'resumo': i.select('.feed-post-body-resumo' ) ,
'url': i.select('.feed-post-link') } for i in nw2 ]

#nws

url_key = 'url'
href_key = 'href'
template = f"""
< div style="padding: 2px; border: 1px solid gray; background: whitesmoke;"> 
{url} 
</div>
"""

# '<h3 style="padding: 4px;">'+ k['titulo'][0].text + f'<a href="" style="padding: 2px;" >{k["url"][0]["href"]}' for k in nws  
#p = ''.join([ "<h3>" + k['titulo'][0].text + "</h3>" + "<br>" + [ str( k['resumo'][0].text ) if ( len(k['resumo']) !=  0 ) else "" ][0] + '<br>' + k['url'][0]['href'] for  k in nws ])
p = ' '.join( 
    [ 
       f'<h3 style="padding: 2px;"> {k["titulo"][0].text}</h3>' + f'<a href="{k[url_key][0][href_key]}" style="padding: 1px; margin: 0;" >Leia mais</a>' for k in nws  
       
    ]
)

#print( p )
display(( HTML( p )) )

#[ 1 if 2 > 3 else 0]
```


```python
news2 = '<h1 style="padding: 12px;">Notícias</h1>'
news2 += '<br><br>'.join( [ '<br>'.join( [ str( i['titulo'] ) , str( i[ 'url' ]  ) ] ) for i in dw ] )
display( HTML( news2 ))
```


```python
import pyespeak
import subprocess
```


```python

nws_data = [
     requests.get( i['url'][0]['href'])  for i in nws 
]
```


```python
print(f'Número de noticias capturadas: {len(nws_data)}' )

```


```python
#BeautifulSoup(nws_data.content, 'html.parser').find()[0]
#BeautifulSoup(nws_data.content, 'html.parser').find()[0]
#BeautifulSoup(nws_data.content, 'html.parser').find()[0]
# g1_(i.content, 'h1', {'class': 'content-head__title'} )[0], g1_( i.content, 'h2', {'class': 'content-head__subtitle' } )[0], g1_(i.content, 'p', {'class':'content-text__container'})[0][0]  ] for i in nws_data 
nws_data_ = []
g1aux = None 

for i in nws_data[:3]:
    try:

        nws_data_.append( 
            [ 
                BeautifulSoup(i.content, 'html.parser').find('h1', class_='content-head__title' ).text,
                BeautifulSoup(i.content, 'html.parser').find('h2', class_='content-head__subtitle').text,
                BeautifulSoup(i.content, 'html.parser').find('p', class_='content-text__container').text
            ]
        )
    except:
        pass

#print(nws_data_)

```


```python
nws_data_[0]
```


```python

s = 'Olá. Bem vindo e bem vinda ao nosso noticiário diário. Eu sou Ani Fátima Liu e apresentarei as principais noticias. \n'
s_interv = 'Agora vamos a nossa próxima notícia.'

#for i in nws_data_[0]:
#    s += i

for i in nws_data_[:3]:
    for j in i:
        s += j
    s += s_interv+'\n'

print(s)
```


```python
#pyespeak.speech(s, '120', 'noticia_dia_full.wav')

```



# CNN Crawler de Noticias do Portal




```python
cnn_data = requests.get('https://www.cnnbrasil.com.br/')

```


```python
cnn_soup = BeautifulSoup(cnn_data.content, 'html.parser')
cnn_nw_data = cnn_soup.find_all('section')
cnn_nw_data[0]
```


```python
c = cnn_nw_data[0].find('a')
#dir(c)

```


```python
c.attrs
```


```python
cnn_list_news = []
aux = None 
for news in cnn_nw_data:
    aux = news.find('a')
    
    
    try :
        
        aux = aux.attrs
        cnn_list_news.extend( [ { 'title': aux['title'], 'href': aux['href'] } ] ) 

    except:
        pass

print(cnn_list_news)
```


```python
cnn_list_news_ma = None
for i in cnn_list_news:
    
    try:
        print(f"\n{i['title']} \n{i['href']}\n\n" ) 
    except:
        pass 
    #keys = i.keys()
    #print(keys)   
    

    #print( f'\t\n\n{out}') 
    #out = '' 

```


```python
len(dw)
```


```python
len(cnn_list_news)
```

# BBC Brasil 

Crawler das notícias do portal do site BBC Brasil.


```python
url_bbc = 'https://www.bbc.com/portuguese'
url_bbc_base = 'https://www.bbc.com'
```


```python
bbc_data = requests.get(url_bbc)
bbc_soup = BeautifulSoup(bbc_data.content, 'html.parser')
bbc_sections =  bbc_soup.find_all('section' , class_= 'bbc-iinl4t')
```


```python
bbc_news_lists = []
```

``` python
url_bbc_base+bbc_sections[0].select('a')[0]['href']
```

Saída 'https://www.bbc.com/portuguese/brasil-63507138'


```python
bbc_sections[0].select('a')[0].text
```


```python
for news in bbc_sections:
    bbc_news_lists.extend( [ { 'title': i.text, 'url': i['href'] } for i in news.select('a') ] )
```


```python
bbc_news_lists = []
aux = None 

for section_news in bbc_sections:
    for news in section_news.select( 'a' ):
        if news['href'].find('topic') != -1:
            pass
        else :
            if news['href'].find('https') != -1:
                bbc_news_lists.extend( [ { 'title': news.text, 'href': news['href'] } ] )
            else:
                bbc_news_lists.extend( [ { 'title': news.text, 'href': url_bbc_base+news['href'] } ] )
```


```python
print(f'Número de notícias: {len(bbc_news_lists)}')
```


```python
random.choices(bbc_news_lists, k = 3)
```


```python
print(url_bbc_base+'/portuguese/topics/cz74k71p8ynt')
```


```python
with open('bbc_news.txt', 'w') as fl:
    for i in bbc_news_lists:
        fl.write(i['title'] +'\n' + i['href'] +'\n\n')
    fl.close()
```


```python

```

# Montando Lista de Notícias


```python
number_news = 6

```


```python
import random
```


```python
news_list = []

news_list.extend( [ {'title': random.choices( [ (news['titulo'], news['url']) for news in dw ] , k = 2 ), 'source': 'G1/Globo' } ] )

news_list.extend( [ {'title': random.choices( [ (news['title'], news['href']) for news in cnn_list_news ] , k = 2 ), 'source': 'CNN Brasil' } ] )

news_list.extend( [ {'title': random.choices( [ (news['title'], news['href']) for news in bbc_news_lists ] , k = 2 ), 'source': 'BBC Brasil' } ] )

```


```python
for i in news_list:
    for j in i['title']:
        print(f"{j[0]}. \n{j[1]}\n")
    
    print(f"Fonte: {i['source']}\n\n")
```


```python
i = j = None

for i in news_list:
    for j in i['title']:
        print(f'{j[0]}.')
    print(f'Fonte: {i["source"] }\n\n ' )
```


```python
i = j = None

print(f"Olá bem vindo ao Diário de Notícias Dimensão Alfa. Estas são as principais manchetes do dia.\n")
for i in news_list:
    print(f'Portal de Notícias {i["source"] }\n ' )
    for j in i['title']:
        print(f'{j[0]}.')
    print('\n\n')
```

# Sobre

## Dimensão Alfa

Dimensão Alfa é uma página no formato de revista eletrônica/digital que trás conhecimento e notícias.

## Info

O presente projeto tem sido usado com fins de divulgação e facilitação de acesso a noticias e conhecimento em comunhão com objetivo da plataforma/página Dimensão Alfa. 
Conteúdos de terceiros são de responsabilidades dos mesmos bem como seus direitos autorais.

O projeto encontra-se em desenvolvimento, inicialmente fôra batizado de Ani Fátima Liu, e estará passando por alterações estando de inicio disponibilizado em formato "_jupyter notebook_" podendo servir como _case_ de estudo para os que se interessam por "web scrap" (raspagem de dados).

Tecnologias foram usadas para gerar vídeo de noticias diária para página [Dimensão Alfa no facebook](https://www.facebook.com) e [Youtube](https://www.youtube.com/@dimensaoalfa); foi usada as seguintes tecnologias:

* [Editor de códigos VSCode](https://code.visualstudio.com/)
* [Python (linguagem de programação)](https://www.python.org/)
* [Ambiente JupyterLab](https://jupyter.org/)
* [Biblioteca "Requests"](https://requests.readthedocs.io/en/latest/)
* [Biblioteca "BeautifulSoup"](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Serviço de Sintese de Voz Microsoft/Azure](https://speech.microsoft.com)


Peço e agradeço a compreensão e apoio de todos. 

Para contribuições, dúvidas, sugestões visitem nossas páginas no [Facebook](https://www.facebook.com/).


## Sugestões de Conteúdo

Deixamos abaixo algumas sugestões de conteúdos e canais com recursos para estudos e pesquisa que podem ser uteis para quem se interessa por tecnologia, programação de computadores, matemática, ciências de dados e inteligência artificial.

* [Programação Dinâmica](https://www.youtube.com/c/Programa%C3%A7%C3%A3oDin%C3%A2mica)
* [Toda Matemática](https://www.youtube.com/c/GustavoViegascurso)
* [Matemática Universitária](https://www.youtube.com/c/Matem%C3%A1ticaUniversit%C3%A1riaProfRenan)
* [Reflexões Matemáticas](https://www.youtube.com/c/Reflex%C3%B5esMatem%C3%A1ticasDrDilbertoJ%C3%BAnior)
* [Programação Descomplicada](https://www.youtube.com/user/progdescomplicada)
* [Univesp](https://www.youtube.com/user/univesptv)
* [USP no Youtube](https://www.youtube.com/c/CanalUSP)
* [IME/USP](https://www.ime.usp.br/)
* [IMPA](https://www.youtube.com/c/impabr)



## Links

* [Dimensão Alfa](https://www.dimensaoalfa.com.br)
* [Facebook](https://www.facebook.com/dimensaoalfa)
* [Youtube](https://www.youtube.com/@dimensaoalfa)
* [WSRicardo](https://wsricardo.blogspot.com)


```python

```
