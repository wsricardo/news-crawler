# Crawler Noticias



## Introdução

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

    /tmp/ipykernel_34675/1468998341.py:8: DeprecationWarning: Importing display from IPython.core.display is deprecated since IPython 7.14, please import from IPython display
      from IPython.core.display import display, HTML


# Modelagem Portal G1



Capturando noticias do portal G1 da Globo
Funções básicas. Especifincando "selector css" classe 'bastian-page'  para tags div.


```python
# Baixando html do portal de noticia para processamento e salvando em disco.
url = 'https://g1.globo.com'
attr = {'class': 'bastian-page'}
data = g1_(requests.get( url ).content, 'div', attr, debug=False)
dw = requests.get('https://g1.globo.com/').content
with open('/tmp/data', 'w') as fl:
    fl.write( dw.decode() )
    
```


```python
type(data)
```




    tuple




```python
# Replace field name 'titulo' for 'title' name.
#dw = [ { key.replace('titulo', 'title'):value for key, value in i.items() } for i in dw ]
#dw = [ { key.replace('url', 'href'):value for key, value in i.items() } for i in dw ]
#replKey = lambda listdc, old_key, new_key: [ ]
def replKey(listdc, old_key, new_key  ):
    dt = []
    
    
    for i in listdc:
        for keys, value in i.items():
            dt.append( { keys.replace('url', 'href'): value } ) 
            
    return dt

data = replKey(data[0], 'url', 'href' )

print(data)
```

    [{'title': 'Mensagens e prints ligam jogadores a esquema de manipulação'}, {'href': 'https://g1.globo.com/go/goias/noticia/2023/05/13/chamadas-de-video-com-apostador-comprovantes-de-pagamento-e-mensagens-veja-provas-apontadas-pelo-mp-que-ligam-jogadores-a-esquema-de-manipulacao-de-jogos.ghtml'}, {'title': 'Preso acusado de manipular jogos ligou da cadeia para esposa; VEJA'}, {'href': 'https://g1.globo.com/go/goias/noticia/2023/05/13/preso-acusado-de-integrar-grupo-que-manipulava-resultados-de-jogos-ligou-para-a-esposa-de-dentro-da-cadeia-e-pediu-dinheiro-para-comprar-celular-veja-conversas.ghtml'}, {'title': 'Treinador de futsal denunciado por assediar jogadoras morre na cadeia'}, {'href': 'https://g1.globo.com/ce/ceara/noticia/2023/05/13/treinador-de-futsal-denunciado-por-assediar-ao-menos-12-jogadoras-morre-dentro-de-presidio-apos-passar-mal-no-ceara.ghtml'}, {'title': 'VÍDEO mostra momento em que meteoro é engolido por nuvem em SC'}, {'href': 'https://g1.globo.com/sc/santa-catarina/noticia/2023/05/13/meteoro-cruza-o-ceu-e-desaparece-dentro-de-nuvem-sob-a-luz-da-lua-em-sc-video.ghtml'}, {'title': 'MS, RJ e SP devem ter frio de menos de 10ºC no fim de semana; veja previsão'}, {'href': 'https://www.climatempo.com.br/noticia/2023/05/13/ar-frio-de-origem-polar-continua-sobre-o-centro-sul-do-brasil-0521'}, {'title': 'Menina vítima de agressões dos pais espalha cartas com pedido de socorro'}, {'href': 'https://g1.globo.com/sp/sao-jose-do-rio-preto-aracatuba/noticia/2023/05/12/menina-espalha-cartas-pedindo-socorro-e-e-acolhida-pelo-conselho-tutelar-no-interior-de-sao-paulo.ghtml'}, {'title': 'Quem é Danilo Tandera, o miliciano mais procurado do RJ '}, {'href': 'https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/05/13/quem-e-danilo-tandera-miliciano-mais-procurado-do-rj-e-com-apenas-duas-passagens-rapidas-pela-cadeia.ghtml'}]



```python
dw, cwn = g1_( dw, 'div', attr)
```

Ao abrir link da noticia pesquisar pela tag *'p'* com atributos **class** com valor **"content-text__container** definir o tamanho para caso extrair só parte do corpo do texto.


Retornando uma lista dos itens encontrados (como visto acima no código) pegamos estes itens e os concatenamos exibintido o texto no corpo da noticia. (_Como visto abaixo_)

Cada "_evt" (_css selector_ class) class css em "bastian-page" refere-se a uma noticia na lista central de noticias.
Dentro de cada "_evt" haverá "bastian-feed-item" e neste o feed-post. 

**feed-post-body** _contêm_  ( 'feed-post-link', 'feed-post-body-title', 'feed-post-body-resumo')

**bastian-feed-item** _contem_ um feed-post-body referindo-se a cada item (noticia)


Para link da noticia (quando acessando a noticia)

**content-head__title** em tag 'h1' (Título da noticia)

**content-head__subtitle** em tag 'h2' (subtitulo/resumo da noticia)

**content-text__container** corpo do texto da noticia css-selector, tag 'p' (pegar só a primeira referente ao primeiro paragrafo da noticia)


```python
news2 = '<h1 style="padding: 12px;">Notícias</h1>'
news2 += '<br><br>'.join( [ '<br>'.join( [ str( i['title'] ) , str( i[ 'url' ]  ) ] ) for i in dw ] )
display( HTML( news2 ))
```


<h1 style="padding: 12px;">Notícias</h1>Mensagens e prints ligam jogadores a esquema de manipulação<br>https://g1.globo.com/go/goias/noticia/2023/05/13/chamadas-de-video-com-apostador-comprovantes-de-pagamento-e-mensagens-veja-provas-apontadas-pelo-mp-que-ligam-jogadores-a-esquema-de-manipulacao-de-jogos.ghtml<br><br>Preso acusado de manipular jogos ligou da cadeia para esposa; VEJA<br>https://g1.globo.com/go/goias/noticia/2023/05/13/preso-acusado-de-integrar-grupo-que-manipulava-resultados-de-jogos-ligou-para-a-esposa-de-dentro-da-cadeia-e-pediu-dinheiro-para-comprar-celular-veja-conversas.ghtml<br><br>Treinador de futsal denunciado por assediar jogadoras morre na cadeia<br>https://g1.globo.com/ce/ceara/noticia/2023/05/13/treinador-de-futsal-denunciado-por-assediar-ao-menos-12-jogadoras-morre-dentro-de-presidio-apos-passar-mal-no-ceara.ghtml<br><br>VÍDEO mostra momento em que meteoro é engolido por nuvem em SC<br>https://g1.globo.com/sc/santa-catarina/noticia/2023/05/13/meteoro-cruza-o-ceu-e-desaparece-dentro-de-nuvem-sob-a-luz-da-lua-em-sc-video.ghtml<br><br>MS, RJ e SP devem ter frio de menos de 10ºC no fim de semana; veja previsão<br>https://www.climatempo.com.br/noticia/2023/05/13/ar-frio-de-origem-polar-continua-sobre-o-centro-sul-do-brasil-0521<br><br>Menina vítima de agressões dos pais espalha cartas com pedido de socorro<br>https://g1.globo.com/sp/sao-jose-do-rio-preto-aracatuba/noticia/2023/05/12/menina-espalha-cartas-pedindo-socorro-e-e-acolhida-pelo-conselho-tutelar-no-interior-de-sao-paulo.ghtml<br><br>Quem é Danilo Tandera, o miliciano mais procurado do RJ <br>https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/05/13/quem-e-danilo-tandera-miliciano-mais-procurado-do-rj-e-com-apenas-duas-passagens-rapidas-pela-cadeia.ghtml


# CNN Crawler de Noticias do Portal


```python
cnn_data = requests.get('https://www.cnnbrasil.com.br/')

```


```python
cnn_soup = BeautifulSoup(cnn_data.content, 'html.parser')
cnn_nw_data = cnn_soup.find_all('section')
cnn_nw_data[0]
```




    <section class="hot__content"> <div class="carousel"> <div class="carousel__screen infinite"> <ul class="carousel__track"> <li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/politica/a-cnn-bolsonaro-diz-que-vai-processar-lula-por-falas-sobre-mansao-e-mortes-na-pandemia/" target="_self" title="LULA X BOLSONARO À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/Reuters_Direct_Media/BrazilOnlineReportTopNews/tagreuters.com2022binary_LYNXMPEI9T0AZ-FILEDIMAGE.jpg?w=65&amp;h=37&amp;crop=1" title="LULA X BOLSONARO À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia"/> <div class="i_ch"> <i></i> <span class="ch"> LULA X BOLSONARO </span> </div> <span class="tp"> À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia </span> </a></div></li><li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/politica/bolsonaro-esta-em-casa-com-o-rabinho-preso-esta-prestando-depoimento-diz-lula-durante-evento-no-ce/" target="_self" title="ATRITOS Bolsonaro está em casa com o rabinho preso, está prestando depoimento, diz Lula durante evento no CE"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2022/10/1666951818390839.jpg?w=65&amp;h=37&amp;crop=1" title="ATRITOS Bolsonaro está em casa com o rabinho preso, está prestando depoimento, diz Lula durante evento no CE"/> <div class="i_ch"> <i></i> <span class="ch"> ATRITOS </span> </div> <span class="tp"> Bolsonaro está em casa com o rabinho preso, está prestando depoimento, diz Lula durante evento no CE </span> </a></div></li><li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/internacional/forcas-da-ucrania-estao-a-500-metros-de-bakhmut-diz-lider-do-grupo-wagner/" target="_self" title="UCRÂNIA Forças da Ucrânia estão “a 500 metros de Bakhmut”, diz líder do Grupo Wagner"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2023/05/Tanque-Ucrania.jpg?w=65&amp;h=37&amp;crop=1" title="UCRÂNIA Forças da Ucrânia estão “a 500 metros de Bakhmut”, diz líder do Grupo Wagner"/> <div class="i_ch"> <i></i> <span class="ch"> UCRÂNIA </span> </div> <span class="tp"> Forças da Ucrânia estão “a 500 metros de Bakhmut”, diz líder do Grupo Wagner </span> </a></div></li><li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/nacional/casal-de-brasileiros-e-encontrado-morto-em-apartamento-nos-eua-e-familia-busca-respostas/" target="_self" title="ESTADOS UNIDOS Casal de brasileiros é encontrado morto em apartamento nos EUA e família busca respostas"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2023/05/1683895412327085.jpg?w=65&amp;h=37&amp;crop=1" title="ESTADOS UNIDOS Casal de brasileiros é encontrado morto em apartamento nos EUA e família busca respostas"/> <div class="i_ch"> <i></i> <span class="ch"> ESTADOS UNIDOS </span> </div> <span class="tp"> Casal de brasileiros é encontrado morto em apartamento nos EUA e família busca respostas </span> </a></div></li> </ul> <ul class="carousel__track"> <li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/politica/a-cnn-bolsonaro-diz-que-vai-processar-lula-por-falas-sobre-mansao-e-mortes-na-pandemia/" target="_self" title="LULA X BOLSONARO À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/Reuters_Direct_Media/BrazilOnlineReportTopNews/tagreuters.com2022binary_LYNXMPEI9T0AZ-FILEDIMAGE.jpg?w=65&amp;h=37&amp;crop=1" title="LULA X BOLSONARO À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia"/> <div class="i_ch"> <i></i> <span class="ch"> LULA X BOLSONARO </span> </div> <span class="tp"> À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia </span> </a></div></li><li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/politica/bolsonaro-esta-em-casa-com-o-rabinho-preso-esta-prestando-depoimento-diz-lula-durante-evento-no-ce/" target="_self" title="ATRITOS Bolsonaro está em casa com o rabinho preso, está prestando depoimento, diz Lula durante evento no CE"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2022/10/1666951818390839.jpg?w=65&amp;h=37&amp;crop=1" title="ATRITOS Bolsonaro está em casa com o rabinho preso, está prestando depoimento, diz Lula durante evento no CE"/> <div class="i_ch"> <i></i> <span class="ch"> ATRITOS </span> </div> <span class="tp"> Bolsonaro está em casa com o rabinho preso, está prestando depoimento, diz Lula durante evento no CE </span> </a></div></li><li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/internacional/forcas-da-ucrania-estao-a-500-metros-de-bakhmut-diz-lider-do-grupo-wagner/" target="_self" title="UCRÂNIA Forças da Ucrânia estão “a 500 metros de Bakhmut”, diz líder do Grupo Wagner"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2023/05/Tanque-Ucrania.jpg?w=65&amp;h=37&amp;crop=1" title="UCRÂNIA Forças da Ucrânia estão “a 500 metros de Bakhmut”, diz líder do Grupo Wagner"/> <div class="i_ch"> <i></i> <span class="ch"> UCRÂNIA </span> </div> <span class="tp"> Forças da Ucrânia estão “a 500 metros de Bakhmut”, diz líder do Grupo Wagner </span> </a></div></li><li class="carousel__item"><div class="hot__list__itens"> <a href="https://www.cnnbrasil.com.br/nacional/casal-de-brasileiros-e-encontrado-morto-em-apartamento-nos-eua-e-familia-busca-respostas/" target="_self" title="ESTADOS UNIDOS Casal de brasileiros é encontrado morto em apartamento nos EUA e família busca respostas"> <img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2023/05/1683895412327085.jpg?w=65&amp;h=37&amp;crop=1" title="ESTADOS UNIDOS Casal de brasileiros é encontrado morto em apartamento nos EUA e família busca respostas"/> <div class="i_ch"> <i></i> <span class="ch"> ESTADOS UNIDOS </span> </div> <span class="tp"> Casal de brasileiros é encontrado morto em apartamento nos EUA e família busca respostas </span> </a></div></li> </ul> </div> </div> </section>




```python
c = cnn_nw_data[0].find('a')
#dir(c)

```


```python
c.attrs
```




    {'href': 'https://www.cnnbrasil.com.br/politica/a-cnn-bolsonaro-diz-que-vai-processar-lula-por-falas-sobre-mansao-e-mortes-na-pandemia/',
     'title': 'LULA X BOLSONARO À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia',
     'target': '_self'}




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

    [{'title': 'LULA X BOLSONARO À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia', 'href': 'https://www.cnnbrasil.com.br/politica/a-cnn-bolsonaro-diz-que-vai-processar-lula-por-falas-sobre-mansao-e-mortes-na-pandemia/'}, {'title': 'Governo espera ter regulamentação das apostas online até o fim do ano, diz Fazenda', 'href': 'https://www.cnnbrasil.com.br/nacional/governo-espera-ter-regulamentacao-das-apostas-online-ate-o-fim-do-ano-diz-fazenda/'}, {'title': 'Se o dinheiro está caro, a culpa não é do BC, porque é malvado, mas do governo, que deve muito, diz Campos Neto à CNN', 'href': 'https://www.cnnbrasil.com.br/economia/se-o-dinheiro-esta-caro-a-culpa-nao-e-do-bc-porque-e-malvado-mas-do-governo-que-deve-muito-diz-campos-neto-a-cnn/'}, {'title': 'Política', 'href': 'https://www.cnnbrasil.com.br/politica/'}, {'title': 'Pop', 'href': 'https://www.cnnbrasil.com.br/pop/'}, {'title': 'Mercado', 'href': '/cotacoes/bolsa'}, {'title': 'Economia', 'href': 'https://www.cnnbrasil.com.br/economia/'}, {'title': 'Internacional', 'href': 'https://www.cnnbrasil.com.br/internacional/'}, {'title': 'Viagem & Gastronomia', 'href': 'https://www.cnnbrasil.com.br/viagemegastronomia/'}, {'title': 'Nacional', 'href': 'https://www.cnnbrasil.com.br/nacional/'}, {'title': 'Saúde', 'href': 'https://www.cnnbrasil.com.br/saude/'}, {'title': 'Esportes', 'href': 'https://www.cnnbrasil.com.br/esportes/'}, {'title': 'CNN Plural', 'href': 'https://www.cnnbrasil.com.br/tudo-sobre/cnn-plural/'}, {'title': 'Ciência e Tecnologia', 'href': 'https://www.cnnbrasil.com.br/tecnologia/'}, {'title': 'Fórmula ucraniana é "a única capaz de parar guerra", diz Zelensky a Amorim', 'href': 'https://www.cnnbrasil.com.br/internacional/formula-ucraniana-e-a-unica-capaz-de-parar-guerra-diz-zelensky-a-amorim/'}]



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

    
    LULA X BOLSONARO À CNN, Bolsonaro diz que vai processar Lula por falas sobre mansão e mortes na pandemia 
    https://www.cnnbrasil.com.br/politica/a-cnn-bolsonaro-diz-que-vai-processar-lula-por-falas-sobre-mansao-e-mortes-na-pandemia/
    
    
    
    Governo espera ter regulamentação das apostas online até o fim do ano, diz Fazenda 
    https://www.cnnbrasil.com.br/nacional/governo-espera-ter-regulamentacao-das-apostas-online-ate-o-fim-do-ano-diz-fazenda/
    
    
    
    Se o dinheiro está caro, a culpa não é do BC, porque é malvado, mas do governo, que deve muito, diz Campos Neto à CNN 
    https://www.cnnbrasil.com.br/economia/se-o-dinheiro-esta-caro-a-culpa-nao-e-do-bc-porque-e-malvado-mas-do-governo-que-deve-muito-diz-campos-neto-a-cnn/
    
    
    
    Política 
    https://www.cnnbrasil.com.br/politica/
    
    
    
    Pop 
    https://www.cnnbrasil.com.br/pop/
    
    
    
    Mercado 
    /cotacoes/bolsa
    
    
    
    Economia 
    https://www.cnnbrasil.com.br/economia/
    
    
    
    Internacional 
    https://www.cnnbrasil.com.br/internacional/
    
    
    
    Viagem & Gastronomia 
    https://www.cnnbrasil.com.br/viagemegastronomia/
    
    
    
    Nacional 
    https://www.cnnbrasil.com.br/nacional/
    
    
    
    Saúde 
    https://www.cnnbrasil.com.br/saude/
    
    
    
    Esportes 
    https://www.cnnbrasil.com.br/esportes/
    
    
    
    CNN Plural 
    https://www.cnnbrasil.com.br/tudo-sobre/cnn-plural/
    
    
    
    Ciência e Tecnologia 
    https://www.cnnbrasil.com.br/tecnologia/
    
    
    
    Fórmula ucraniana é "a única capaz de parar guerra", diz Zelensky a Amorim 
    https://www.cnnbrasil.com.br/internacional/formula-ucraniana-e-a-unica-capaz-de-parar-guerra-diz-zelensky-a-amorim/
    
    



```python
len(dw)
```




    7




```python
len(cnn_list_news)
```




    15



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




    'As sacerdotisas africanas perseguidas pela Inquisição no Brasil'




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

    Número de notícias: 63



```python
random.choices(bbc_news_lists, k = 3)
```




    [{'title': 'Jovem de 16 anos recebe R$ 45 milhões em ofertas de bolsas universitárias nos EUA e se aproxima de recorde',
      'href': 'https://www.bbc.com/portuguese/articles/cqezgqj2gd5o'},
     {'title': 'Os mitos e erros sobre os hemisférios do cérebro',
      'href': 'https://www.bbc.com/portuguese/articles/cjj999w39dgo'},
     {'title': 'Vídeo, O desastre que ameaça líder turco, no poder há duas décadas, Duration 4,54',
      'href': 'https://www.bbc.com/portuguese/internacional-65573941'}]




```python
print(url_bbc_base+'/portuguese/topics/cz74k71p8ynt')
```

    https://www.bbc.com/portuguese/topics/cz74k71p8ynt



```python
with open('bbc_news.txt', 'w') as fl:
    for i in bbc_news_lists:
        fl.write(i['title'] +'\n' + i['href'] +'\n\n')
    fl.close()
```

# Portal Band

Busca de lista de notícias do portal Band.


```python
url_band = 'https://www.band.uol.com.br/'
```


```python
band_data = requests.get(url_band).content
soup_band = BeautifulSoup(band_data, 'html.parser')

```


```python
news_band_section = soup_band.find_all('section')
print(f'Número: {len(news_band_section)}')
```

    Número: 17



```python
aux = []
list_ = None
for secs in news_band_section:
    list_ = secs.find_all('a', class_='link')
    for i in list_:
        
        try:
            aux.extend( [ { 'title': i.h3.text+'. '+ i.h2.text, 'href': i['href']} ] )
        except:
            aux.extend( [ { 'title': i.text, 'href': i['href'] } ] )
    #aux.extend([ { 'title': i}  for i in list_ ]  )
news_list_band = [] 
news_list_band.extend(random.choices(aux, k=4 ) )
```


```python
n = soup_band.find_all('a')
```


```python
import random

random.choices(news_list_band, k = 4)[0:]
for i in news_list_band:
    print(f"\n{i['title']}\n{i['href']}")
```

    
    
    /bandnews-fm/colunistas/paloma-tocci
    
    
    /band-shop/guia-de-compras/dia-do-cozinheiro-utensilios-culinarios-essenciais-16601251
    
    
    /esportes/luis-castro-critica-cobranca-excessiva-a-tecnicos-e-diz-nos-jogaram-no-lixo-16601722
    
    Presidente da Ucrânia chega em Roma para encontrar Papa Francisco
    /noticias/presidente-da-ucrania-chega-em-roma-para-encontrar-papa-francisco-16602006



```python
n[0]
```




    <a _ngcontent-sc85="" aria-label="Band" class="logo logo--portal logo-name--Band logo--image center" href="/"><img _ngcontent-sc85="" alt="Band" class="logo-image" height="35" src="https://pubimg.band.uol.com.br/Files/logo-band-2022-v2.png?v2" width="101"/><!-- --><!-- --><!-- --></a>



# Montando Lista de Notícias


```python
number_news = 6

```


```python
import random
```


```python
news_list = []

news_list.extend( [ {'title': random.choices( [ (news['title'], news['url']) for news in dw ] , k = 2 ), 'source': 'G1/Globo' } ] )

news_list.extend( [ {'title': random.choices( [ (news['title'], news['href']) for news in cnn_list_news ] , k = 2 ), 'source': 'CNN Brasil' } ] )

news_list.extend( [ {'title': random.choices( [ (news['title'], news['href']) for news in bbc_news_lists ] , k = 2 ), 'source': 'BBC Brasil' } ] )

```


```python
for i in news_list:
    for j in i['title']:
        print(f"{j[0]}. \n{j[1]}\n")
    
    print(f"Fonte: {i['source']}\n\n")
```

    Preso acusado de manipular jogos ligou da cadeia para esposa; VEJA. 
    https://g1.globo.com/go/goias/noticia/2023/05/13/preso-acusado-de-integrar-grupo-que-manipulava-resultados-de-jogos-ligou-para-a-esposa-de-dentro-da-cadeia-e-pediu-dinheiro-para-comprar-celular-veja-conversas.ghtml
    
    Mensagens e prints ligam jogadores a esquema de manipulação. 
    https://g1.globo.com/go/goias/noticia/2023/05/13/chamadas-de-video-com-apostador-comprovantes-de-pagamento-e-mensagens-veja-provas-apontadas-pelo-mp-que-ligam-jogadores-a-esquema-de-manipulacao-de-jogos.ghtml
    
    Fonte: G1/Globo
    
    
    Internacional. 
    https://www.cnnbrasil.com.br/internacional/
    
    Fórmula ucraniana é "a única capaz de parar guerra", diz Zelensky a Amorim. 
    https://www.cnnbrasil.com.br/internacional/formula-ucraniana-e-a-unica-capaz-de-parar-guerra-diz-zelensky-a-amorim/
    
    Fonte: CNN Brasil
    
    
    A campanha por jovem com doença rara que enganou celebridades e teve desfecho trágico . 
    https://www.bbc.com/portuguese/articles/cv2vvdw5q0vo
    
    Como Marília Mendonça continua a ser fenômeno após sua morte. 
    https://www.bbc.com/portuguese/articles/ckrk07gg2reo
    
    Fonte: BBC Brasil
    
    


## Salvando Todas Noticias (JSON)

### View news for test algorithm


```python
# List news
news = None
portaisvar = [
    'dw', #Globo/G1
    'cnn_list_news', # CNN Brazil
    'bbc_news_list' # BBC Brazil
]

portais = { 'dw': 'Globo/G1', 'cnn_list_news': 'CNN Brasil', 'bbc_news_lists': 'BBC Brasil' }    
```


```python
dw[0].keys(), cnn_list_news[0].keys(), bbc_news_lists[0].keys()
```




    (dict_keys(['title', 'url']),
     dict_keys(['title', 'href']),
     dict_keys(['title', 'href']))




```python
# Replace field name 'titulo' for 'title' name.
dw = [ { key.replace('titulo', 'title'):value for key, value in i.items() } for i in dw ]
dw = [ { key.replace('url', 'href'):value for key, value in i.items() } for i in dw ]
dw
```




    [{'title': 'Mensagens e prints ligam jogadores a esquema de manipulação',
      'href': 'https://g1.globo.com/go/goias/noticia/2023/05/13/chamadas-de-video-com-apostador-comprovantes-de-pagamento-e-mensagens-veja-provas-apontadas-pelo-mp-que-ligam-jogadores-a-esquema-de-manipulacao-de-jogos.ghtml'},
     {'title': 'Preso acusado de manipular jogos ligou da cadeia para esposa; VEJA',
      'href': 'https://g1.globo.com/go/goias/noticia/2023/05/13/preso-acusado-de-integrar-grupo-que-manipulava-resultados-de-jogos-ligou-para-a-esposa-de-dentro-da-cadeia-e-pediu-dinheiro-para-comprar-celular-veja-conversas.ghtml'},
     {'title': 'Treinador de futsal denunciado por assediar jogadoras morre na cadeia',
      'href': 'https://g1.globo.com/ce/ceara/noticia/2023/05/13/treinador-de-futsal-denunciado-por-assediar-ao-menos-12-jogadoras-morre-dentro-de-presidio-apos-passar-mal-no-ceara.ghtml'},
     {'title': 'VÍDEO mostra momento em que meteoro é engolido por nuvem em SC',
      'href': 'https://g1.globo.com/sc/santa-catarina/noticia/2023/05/13/meteoro-cruza-o-ceu-e-desaparece-dentro-de-nuvem-sob-a-luz-da-lua-em-sc-video.ghtml'},
     {'title': 'MS, RJ e SP devem ter frio de menos de 10ºC no fim de semana; veja previsão',
      'href': 'https://www.climatempo.com.br/noticia/2023/05/13/ar-frio-de-origem-polar-continua-sobre-o-centro-sul-do-brasil-0521'},
     {'title': 'Menina vítima de agressões dos pais espalha cartas com pedido de socorro',
      'href': 'https://g1.globo.com/sp/sao-jose-do-rio-preto-aracatuba/noticia/2023/05/12/menina-espalha-cartas-pedindo-socorro-e-e-acolhida-pelo-conselho-tutelar-no-interior-de-sao-paulo.ghtml'},
     {'title': 'Quem é Danilo Tandera, o miliciano mais procurado do RJ ',
      'href': 'https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/05/13/quem-e-danilo-tandera-miliciano-mais-procurado-do-rj-e-com-apenas-duas-passagens-rapidas-pela-cadeia.ghtml'}]




```python
#[ { key.replace('title', 'titulo' ) } ]
newslist = dw + cnn_list_news + bbc_news_lists
#newslist
```


```python
import os
count = 0
try:
    os.mkdir( 'newsdata' )
except FileExistsError:
    print("File exist")
    
webdata = ''
# Save data of link news in files to folder.
for news in newslist:
    try:
        #news['data'] = requests.get(news['href']).text
        foldername = f'newsdata'
        #os.mkdir( foldername )
        news['datafile'] = f'{foldername}/'+str( count )
        with open( foldername+f'/{str(count)}', 'a' ) as fl:
            webdata = requests.get( news['href'] ).text 
            fl.write( webdata )
            fl.close()
            
        count += 1
    except :
        print('not get page')
        continue
    
```

    File exist
    not get page



```python
newslist[0]['datafile']
```




    'newsdata/0'




```python
p = requests.get( newslist[0]['href'] )
soup = BeautifulSoup( p.text, 'html.parser')
texto = soup.get_text()
print( texto[0:150] )
```

     Chamadas de vídeo com apostador, comprovantes de pagamento e mensagens: veja provas apontadas pelo MP que ligam jogadores a esquema de manipulação de



```python
d = ''
with open(foldername+'/0', 'r') as fl:
    d = fl.read()
    fl.close()


soup = BeautifulSoup(d, 'html.parser')
#souptext = soup.text
content = soup.find_all('div')
#dir(soup)
```


```python
texto = ' '.join( [ i.get_text() for i in content ] )
texto = texto.replace('\n', ' ')
with open('texto', 'w' ) as fl:
    #fl.write( souptext )
    fl.write( texto )
    
```


```python
print( texto[0:100] )
```

                  Goiás                                   fique por dentro             Imposto de Renda 



```python
import json

with open('noticias.json', 'w') as fl:
    fl.write(json.dumps(newslist, ensure_ascii=False, indent=4))
    fl.close()
```

### Salva noticias


```python
def savenews(newslist: list, filename: str) -> None:
    import json
    jsondata = None
    with open(filename, 'w') as fl:
        fl.write( json.dumps( newslist, encode='utf-8', indent=4 ) )
        fl.close()
    print('Saved...')
    
```


```python
i = j = None

for i in news_list:
    for j in i['title']:
        print(f'{j[0]}.')
    print(f'Fonte: {i["source"] }\n\n ' )
```

    Preso acusado de manipular jogos ligou da cadeia para esposa; VEJA.
    Mensagens e prints ligam jogadores a esquema de manipulação.
    Fonte: G1/Globo
    
     
    Internacional.
    Fórmula ucraniana é "a única capaz de parar guerra", diz Zelensky a Amorim.
    Fonte: CNN Brasil
    
     
    A campanha por jovem com doença rara que enganou celebridades e teve desfecho trágico .
    Como Marília Mendonça continua a ser fenômeno após sua morte.
    Fonte: BBC Brasil
    
     



```python
i = j = None

print(f"Olá bem vindo ao Diário de Notícias Dimensão Alfa. Estas são as principais manchetes do dia.\n")
for i in news_list:
    print(f'Portal de Notícias {i["source"] }\n ' )
    for j in i['title']:
        print(f'{j[0]}.')
    print('\n\n')
```

    Olá bem vindo ao Diário de Notícias Dimensão Alfa. Estas são as principais manchetes do dia.
    
    Portal de Notícias G1/Globo
     
    Preso acusado de manipular jogos ligou da cadeia para esposa; VEJA.
    Mensagens e prints ligam jogadores a esquema de manipulação.
    
    
    
    Portal de Notícias CNN Brasil
     
    Internacional.
    Fórmula ucraniana é "a única capaz de parar guerra", diz Zelensky a Amorim.
    
    
    
    Portal de Notícias BBC Brasil
     
    A campanha por jovem com doença rara que enganou celebridades e teve desfecho trágico .
    Como Marília Mendonça continua a ser fenômeno após sua morte.
    
    
    


# Sobre

## Dimensão Alfa

Dimensão Alfa projetos e conteúdos de tecnologia.

## Info

O presente projeto tem sido usado com fins de divulgação e facilitação de acesso a noticias e conhecimento em comunhão com objetivo da plataforma/página Dimensão Alfa. 
Conteúdos de terceiros são de responsabilidades dos mesmos bem como seus direitos autorais.

O projeto encontra-se em desenvolvimento, inicialmente fôra batizado de Ani Fátima Liu, e estará passando por alterações estando de inicio disponibilizado em formato "_jupyter notebook_" podendo servir como _case_ de estudo para os que se interessam por "web scrap" (raspagem de dados).

Tecnologias foram usadas para gerar vídeo de noticias diária para página [Youtube](https://www.youtube.com/@dimensaoalfa); foi usada as seguintes tecnologias:

* [Editor de códigos VSCode](https://code.visualstudio.com/)
* [Python (linguagem de programação)](https://www.python.org/)
* [Ambiente JupyterLab](https://jupyter.org/)
* [Biblioteca "Requests"](https://requests.readthedocs.io/en/latest/)
* [Biblioteca "BeautifulSoup"](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Serviço de Sintese de Voz Microsoft/Azure](https://speech.microsoft.com)


Peço e agradeço a compreensão e apoio de todos. 

Para contribuições, dúvidas, sugestões visitem meu blog [WSRicardo](https://wsricardo.blogspot.com).


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


```python

```
