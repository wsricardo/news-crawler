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

    /tmp/ipykernel_33177/1468998341.py:8: DeprecationWarning: Importing display from IPython.core.display is deprecated since IPython 7.14, please import from IPython display
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

    [{'title': 'Mensagens e prints ligam jogadores a esquema de manipulação'}, {'href': 'https://g1.globo.com/go/goias/noticia/2023/05/13/chamadas-de-video-com-apostador-comprovantes-de-pagamento-e-mensagens-veja-provas-apontadas-pelo-mp-que-ligam-jogadores-a-esquema-de-manipulacao-de-jogos.ghtml'}, {'title': 'Preso acusado manipular jogos ligou da cadeia para esposa; VEJA'}, {'href': 'https://g1.globo.com/go/goias/noticia/2023/05/13/preso-acusado-de-integrar-grupo-que-manipulava-resultados-de-jogos-ligou-para-a-esposa-de-dentro-da-cadeia-e-pediu-dinheiro-para-comprar-celular-veja-conversas.ghtml'}, {'title': 'Treinador de futsal denunciado por assediar jogadoras morre na cadeia'}, {'href': 'https://g1.globo.com/ce/ceara/noticia/2023/05/13/treinador-de-futsal-denunciado-por-assediar-ao-menos-12-jogadoras-morre-dentro-de-presidio-apos-passar-mal-no-ceara.ghtml'}, {'title': 'VÍDEO mostra momento em que meteoro é engolido por nuvem em SC'}, {'href': 'https://g1.globo.com/sc/santa-catarina/noticia/2023/05/13/meteoro-cruza-o-ceu-e-desaparece-dentro-de-nuvem-sob-a-luz-da-lua-em-sc-video.ghtml'}, {'title': 'MS, RJ e SP devem ter frio de menos de 10ºC no fim de semana; veja previsão'}, {'href': 'https://www.climatempo.com.br/noticia/2023/05/13/ar-frio-de-origem-polar-continua-sobre-o-centro-sul-do-brasil-0521'}, {'title': 'Menina vítima de agressões dos pais espalha cartas com pedido de socorro'}, {'href': 'https://g1.globo.com/sp/sao-jose-do-rio-preto-aracatuba/noticia/2023/05/12/menina-espalha-cartas-pedindo-socorro-e-e-acolhida-pelo-conselho-tutelar-no-interior-de-sao-paulo.ghtml'}, {'title': 'Quem é Danilo Tandera, o miliciano mais procurado do RJ '}, {'href': 'https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/05/13/quem-e-danilo-tandera-miliciano-mais-procurado-do-rj-e-com-apenas-duas-passagens-rapidas-pela-cadeia.ghtml'}]



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


<h1 style="padding: 12px;">Notícias</h1>Mensagens e prints ligam jogadores a esquema de manipulação<br>https://g1.globo.com/go/goias/noticia/2023/05/13/chamadas-de-video-com-apostador-comprovantes-de-pagamento-e-mensagens-veja-provas-apontadas-pelo-mp-que-ligam-jogadores-a-esquema-de-manipulacao-de-jogos.ghtml<br><br>Preso acusado manipular jogos ligou da cadeia para esposa; VEJA<br>https://g1.globo.com/go/goias/noticia/2023/05/13/preso-acusado-de-integrar-grupo-que-manipulava-resultados-de-jogos-ligou-para-a-esposa-de-dentro-da-cadeia-e-pediu-dinheiro-para-comprar-celular-veja-conversas.ghtml<br><br>Treinador de futsal denunciado por assediar jogadoras morre na cadeia<br>https://g1.globo.com/ce/ceara/noticia/2023/05/13/treinador-de-futsal-denunciado-por-assediar-ao-menos-12-jogadoras-morre-dentro-de-presidio-apos-passar-mal-no-ceara.ghtml<br><br>VÍDEO mostra momento em que meteoro é engolido por nuvem em SC<br>https://g1.globo.com/sc/santa-catarina/noticia/2023/05/13/meteoro-cruza-o-ceu-e-desaparece-dentro-de-nuvem-sob-a-luz-da-lua-em-sc-video.ghtml<br><br>MS, RJ e SP devem ter frio de menos de 10ºC no fim de semana; veja previsão<br>https://www.climatempo.com.br/noticia/2023/05/13/ar-frio-de-origem-polar-continua-sobre-o-centro-sul-do-brasil-0521<br><br>Menina vítima de agressões dos pais espalha cartas com pedido de socorro<br>https://g1.globo.com/sp/sao-jose-do-rio-preto-aracatuba/noticia/2023/05/12/menina-espalha-cartas-pedindo-socorro-e-e-acolhida-pelo-conselho-tutelar-no-interior-de-sao-paulo.ghtml<br><br>Quem é Danilo Tandera, o miliciano mais procurado do RJ <br>https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/05/13/quem-e-danilo-tandera-miliciano-mais-procurado-do-rj-e-com-apenas-duas-passagens-rapidas-pela-cadeia.ghtml


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




    [{'title': 'O que o SUS está ensinando ao serviço de saúde britânico',
      'href': 'https://www.bbc.com/portuguese/articles/cq5ww8jryk0o'},
     {'title': 'Vídeo, O desastre que ameaça líder turco, no poder há duas décadas, Duration 4,54',
      'href': 'https://www.bbc.com/portuguese/internacional-65573941'},
     {'title': 'A família boêmia que chocou a Grã-Bretanha vitoriana',
      'href': 'https://www.bbc.com/portuguese/articles/cjqk08z5ew4o'}]




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

    
    Antonio Fagundes precisou tirar carteira de motorista especial para Carga Pesada
    /entretenimento/melhor-da-tarde/noticias/antonio-fagundes-precisou-tirar-carteira-de-motorista-especial-para-carga-pesada-16601873
    
    Luiza Martins relembra episódio engraçado com Marília Mendonça: “Não enxergava” 
    /entretenimento/faustao-na-band/noticias/luiza-martins-relembra-episodio-engracado-com-marilia-mendonca-nao-enxergava-16601910
    
    TRAGÉDIA
    /noticias/cenipa-conclui-relatorio-sobre-acidente-aereo-que-matou-marilia-mendonca-16601833
    
    Show do Esporte
    /esportes/show-do-esporte



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

    Quem é Danilo Tandera, o miliciano mais procurado do RJ . 
    https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/05/13/quem-e-danilo-tandera-miliciano-mais-procurado-do-rj-e-com-apenas-duas-passagens-rapidas-pela-cadeia.ghtml
    
    Treinador de futsal denunciado por assediar jogadoras morre na cadeia. 
    https://g1.globo.com/ce/ceara/noticia/2023/05/13/treinador-de-futsal-denunciado-por-assediar-ao-menos-12-jogadoras-morre-dentro-de-presidio-apos-passar-mal-no-ceara.ghtml
    
    Fonte: G1/Globo
    
    
    Se o dinheiro está caro, a culpa não é do BC, porque é malvado, mas do governo, que deve muito, diz Campos Neto à CNN. 
    https://www.cnnbrasil.com.br/economia/se-o-dinheiro-esta-caro-a-culpa-nao-e-do-bc-porque-e-malvado-mas-do-governo-que-deve-muito-diz-campos-neto-a-cnn/
    
    Ciência e Tecnologia. 
    https://www.cnnbrasil.com.br/tecnologia/
    
    Fonte: CNN Brasil
    
    
    Podcast busca entender como brasileiros chegaram a atual grau de divisão; ouça aqui. 
    https://www.bbc.com/portuguese/podcasts/p0cyhvny
    
    Facebook. 
    https://www.facebook.com/bbcnewsbrasil/
    
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
     {'title': 'Preso acusado manipular jogos ligou da cadeia para esposa; VEJA',
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
print( texto )
```

     Chamadas de vídeo com apostador, comprovantes de pagamento e mensagens: veja provas apontadas pelo MP que ligam jogadores a esquema de manipulação de jogos | Goiás | G1
    
                       Goiás                          
    
    
    
    
    
    
    
    
    fique por dentro
    
    
              Imposto de Renda 
          
    
              Mega-Sena
          
    
              Quiz
          
    
              Frio
          
    
              Anderson Torres solto
          
    
    
    
    
    
    
    Empresário Bruno Lopez de Moura que foi preso em São Paulo acusado de participar de esquema criminoso — Foto: Reprodução/Instagram     Empresário Bruno Lopez de Moura que foi preso em São Paulo acusado de participar de esquema criminoso — Foto: Reprodução/Instagram        Também havia o "Núcleo Financiadores". Eles eram os responsáveis por assegurar a existência de verbas para o pagamento dos jogadores aliciados e também nas apostas manipuladas.       Além disso, havia o "Núcleo Intermediadores". Estes eram responsáveis por indicar contatos e facilitar a aproximação entre apostadores e atletas aptos a promover a manipulação dos eventos esportivos.       Também havia o "Núcleo Administrativo", que era responsável por fazer as transferências financeiras a integrantes da organização criminosa e também em benefício de jogadores cooptados.     Como a operação começou     A Operação Penalidade Máxima já fez buscas e apreensões nos endereços dos envolvidos. As investigações começaram no final de 2022, quando o volante Romário, do Vila Nova-GO, aceitou uma oferta de R$ 150 mil para cometer um pênalti no jogo contra o Sport, pela Série B do Campeonato Brasileiro.             Romário recebeu um sinal de R$ 10 mil, e só teria os outros R$ 140 mil após a partida, com o pênalti cometido. À época, o presidente do Vila Nova-GO, Hugo Jorge Bravo, que também é policial militar, investigou o caso e entregou as provas ao MP-GO.     Nota Esporte Clube Novo Hamburgo     O Esporte Clube Novo Hamburgo, neste ato representado pelo seu Presidente Jeronimo da Silva Freitas, vem a público novamente se pronunciar em relação a investigação de tentativas de fraude de resultados conduzida pelo Ministério Público de Goiás.       Em matéria veiculada pela mídia no dia de hoje, o clube é mencionado através do jogador Nikolas Farias, que atuou pelo Esporte Clube Novo Hamburgo na partida válida pelo Gauchão 2023 no dia 11 de fevereiro de 2023. No entanto, para fins de esclarecimentos, o clube informa que o jogador não faz mais parte do quadro de funcionários desde fevereiro do presente ano.       O Esporte Clube Novo Hamburgo está adotando todas as medidas necessárias para a proteção do clube contra eventuais atos criminosos, bem como encontra-se à disposição para colaborar na investigação e identificação de todos os envolvidos.       O Esporte Clube Novo Hamburgo repudia todo e qualquer ato criminoso contra a prática desportiva e contra a sociedade, agindo sempre com transparência perante sua torcida e toda a comunidade.             Veja outras notícias da região no g1 Goiás.     VÍDEOS: últimas notícias de Goiás        50 vídeos                                    Deseja receber as notícias mais importantes em tempo real? Ative as notificações do G1!    Agora não                  Ativar            Veja também                         Mais do G1     
    
    Escândalo no futebolMensagens e prints ligam jogadores a esquema de manipulaçãoHá 5 horas Goiás Mulher de apostador usa ofensa racista contra jogador do SantosHá 5 horasMP identifica pela 1ª vez fraude em resultado de partidaHá 5 horasPreso acusado manipular jogos ligou da cadeia para esposa; VEJADefesa de Thiago Chambó diz que conversas não são incriminadoras.Há 23 minutos Goiás CearáTreinador de futsal denunciado por assediar jogadoras morre na cadeiaTécnico sentiu fortes dores provocadas por hérnia inguinescrotal e desmaiou.Há 2 horas Ceará Sumiço no céu ☁️☄️VÍDEO mostra momento em que meteoro é engolido por nuvem em SCHá 1 hora Santa Catarina 🥶Não esqueça o agasalho!MS, RJ e SP devem ter frio de menos de 10ºC no fim de semana; veja previsãoHá 3 horasViolência infantilMenina vítima de agressões dos pais espalha cartas com pedido de socorroHá 2 horas São José do Rio Preto e Araçatuba Ligado a paramilitaresQuem é Danilo Tandera, o miliciano mais procurado do RJ Há 6 horas Rio de Janeiro Veja mais
                     Outra sugestão    Ir para reportagem                Sugerida para você            Outra sugestão    Ir para reportagem       Você deseja continuar recebendo este tipo de sugestões de matérias?    Não quero   Sim, por favor!    
    
    
    
    
    
    
    
    
    
    
    Últimas Notícias
    
    
    
    Globo Notícias
    
    
    
    © Copyright 2000-2023 Globo Comunicação e Participações S.A.
    
    princípios editoriais
    política de privacidade
    minha conta
    anuncie conosco
    
    
    
    
              
    
    
    
    
    
    
    
    Editorias
    
    
    
    
    
    menu g1
    
    
    
    Editorias
    
    
    
    Agro
    
    
    
    
    
    Editorias
    
    
    
    Agro
    
    
    
    Primeira Página
    
    
    
    
    Agro de gente pra gente
    
    
    
    
    Globo Rural
    
    
    
    
    A Indústria-Riqueza do Brasil
    
    
     
    
    
    Carnaval 2023
    
    
    
    
    
    Editorias
    
    
    
    Carnaval 2023
    
    
    
    primeira página
    
    
    
    
    Rio de Janeiro
    
    
    
    
    São Paulo
    
    
    
    
    Pernambuco
    
    
    
    
    Minas Gerais
    
    
     
    
    
    Ciência
    
    
    
    
    
    Editorias
    
    
    
    Ciência
    
    
    
    Primeira Página
    
    
    
    
    Viva Você
    
    
     
    
    
    Economia
    
    
    
    
    
    Editorias
    
    
    
    Economia
    
    
    
    Primeira Página
    
    
    
    
    Bitcoin
    
    
    
    
    Calculadoras
    
    
    
    
    Dólar
    
    
    
    
    Educação Financeira
    
    
    
    
    Imposto de Renda
    
    
    
    
    Mídia e Marketing
    
    
    
    
    Open banking
    
    
     
    
    
    Educação
    
    
    
    
    
    Editorias
    
    
    
    Educação
    
    
    
    Primeira Página
    
    
    
    
    Enem
    
    
    
    
    Estuda.com
    
    
    
    
    Guia de Carreiras
    
    
    
    
    Teste Vocacional
    
    
    
    
    Universidades
    
    
     
    
    
    Empreendedorismo​
    
    
    
    
    
    Editorias
    
    
    
    Empreendedorismo​
    
    
    
    Primeira página
    
    
    
    
    pequenas empresas
    
    
    
    
    Menos 30 Fest
    
    
     
    
    
    Fato ou Fake
    
    
    
    
    Guia de compras
    
    
    
    
    Inovação
    
    
    
    
    Loterias
    
    
    
    
    Meio Ambiente
    
    
    
    
    
    Editorias
    
    
    
    Meio Ambiente
    
    
    
    Primeira Página
    
    
    
    
    Amazônia
    
    
    
    
    Globo Natureza
    
    
    
    
    Sustentabilidade​
    
    
     
    
    
    Monitor da Violência
    
    
    
    
    Mundo
    
    
    
    
    
    Editorias
    
    
    
    Mundo
    
    
    
    Primeira página
    
    
    
    
    Guerra na Ucrânia
    
    
     
    
    
    Olha que legal
    
    
    
    
    Política
    
    
    
    
    
    Editorias
    
    
    
    Política
    
    
    
    Primeira Página
    
    
    
    
    Reforma da Previdência
    
    
     
    
    
    Pop & Arte
    
    
    
    
    
    Editorias
    
    
    
    Pop & Arte
    
    
    
    Primeira Página
    
    
    
    
    Cinema
    
    
    
    
    CCXP
    
    
    
    
    Diversidade
    
    
    
    
    Games
    
    
    
    
    Música
    
    
    
    
    Tv e séries
    
    
    
    
    Lollapalooza
    
    
    
    
    Oscar
    
    
    
    
    Rock in Rio
    
    
     
    
    
    Saúde
    
    
    
    
    
    Editorias
    
    
    
    Saúde
    
    
    
    Primeira página
    
    
    
    
    Bem Estar
    
    
    
    
    Coronavirus
    
    
     
    
    
    Tecnologia
    
    
    
    
    Trabalho e Carreira​
    
    
    
    
    
    Editorias
    
    
    
    Trabalho e Carreira​
    
    
    
    Primeira página
    
    
    
    
    Concursos
    
    
    
    
    Vagas de emprego
    
    
     
    
    
    Turismo e Viagem
    
    
    
    
    
    Editorias
    
    
    
    Turismo e Viagem
    
    
    
    Primeira Página
    
    
    
    
    Descubra o Brasil
    
    
     
     
    
    
    Guia de Compras
    
    
    
    
    Regiões
    
    
    
    
    
    menu g1
    
    
    
    Regiões
    
    
    
    centro-oeste
    
    
    
    
    
    Regiões
    
    
    
    centro-oeste
    
    
    
    Distrito Federal
    
    
    
    
    
    centro-oeste
    
    
    
    Distrito Federal
    
    
    
    Primeira página
    
    
    
    
    Bom Dia DF
    
    
    
    
    DF1
    
    
    
    
    DF2
    
    
    
    
    Globo Comunidade DF
    
    
    
    
    O que fazer no DF
    
    
     
    
    
    Goiás
    
    
    
    
    
    centro-oeste
    
    
    
    Goiás
    
    
    
    Primeira página
    
    
    
    
    Bom Dia GO
    
    
    
    
    Bom dia sábado
    
    
    
    
    JA 1ª Edição
    
    
    
    
    JA 2ª Edição
    
    
    
    
    Jornal do Campo
    
    
    
    
    Esporte
    
    
    
    
    Mercado Imobiliário
    
    
     
    
    
    Mato Grosso
    
    
    
    
    
    centro-oeste
    
    
    
    Mato Grosso
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia MT
    
    
    
    
    MT TV 1ª Edição
    
    
    
    
    MT Rural
    
    
    
    
    MT TV 2ª Edição
    
    
    
    
    Esporte
    
    
     
    
    
    Mato Grosso do Sul
    
    
    
    
    
    centro-oeste
    
    
    
    Mato Grosso do Sul
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia MS
    
    
    
    
    MS TV 1ª Edição
    
    
    
    
    MS TV 2ª Edição
    
    
    
    
    MS Rural
    
    
    
    
    Esporte
    
    
     
     
    
    
    nordeste
    
    
    
    
    
    Regiões
    
    
    
    nordeste
    
    
    
    Alagoas
    
    
    
    
    
    nordeste
    
    
    
    Alagoas
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Alagoas
    
    
    
    
    AL TV 1ª Edição
    
    
    
    
    AL TV 2ª Edição
    
    
    
    
    Gazeta Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Bahia
    
    
    
    
    
    nordeste
    
    
    
    Bahia
    
    
    
    Primeira Página
    
    
    
    
    Jornal da manhã
    
    
    
    
    Bahia Meio Dia
    
    
    
    
    BATV
    
    
    
    
    Bahia Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Ceará
    
    
    
    
    
    nordeste
    
    
    
    Ceará
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia CE
    
    
    
    
    CETV 1ª Edição
    
    
    
    
    CETV 2ª Edição
    
    
    
    
    NE Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Maranhão
    
    
    
    
    
    nordeste
    
    
    
    Maranhão
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Mirante
    
    
    
    
    JMTV 1ª Edição
    
    
    
    
    JMTV 2ª edição
    
    
    
    
    Mirante Rural
    
    
    
    
    Esporte
    
    
    
    
    Daqui
    
    
    
    
    Repórter Mirante
    
    
     
    
    
    Paraíba
    
    
    
    
    
    nordeste
    
    
    
    Paraíba
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Paraíba
    
    
    
    
    JPB 1ª Edição
    
    
    
    
    JPB 2ª Edição
    
    
    
    
    Paraíba Comunidade
    
    
    
    
    Esporte
    
    
     
    
    
    Pernambuco
    
    
    
    
    
    nordeste
    
    
    
    Pernambuco
    
    
    
    Recife e região
    
    
    
    
    
    Pernambuco
    
    
    
    Recife e região
    
    
    
    Primeira página
    
    
    
    
    Bom Dia PE
    
    
    
    
    NE 1
    
    
    
    
    NE 2
    
    
    
    
    Espaço PE
    
    
    
    
    Globo Comunidade PE
    
    
    
    
    Nordeste Viver e Preservar
    
    
    
    
    Educação
    
    
    
    
    Esporte
    
    
     
    
    
    Caruaru e região
    
    
    
    
    
    Pernambuco
    
    
    
    Caruaru e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia PE
    
    
    
    
    ABTV 1ª Edição
    
    
    
    
    ABTV 2ª Edição
    
    
    
    
    Globo Comunidade
    
    
    
    
    Esporte
    
    
     
    
    
    Petrolina e região
    
    
    
    
    
    Pernambuco
    
    
    
    Petrolina e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Pernambuco
    
    
    
    
    GRTV 1ª Edição
    
    
    
    
    GRTV 2ª edição
    
    
    
    
    Esporte
    
    
     
     
    
    
    Piauí
    
    
    
    
    
    nordeste
    
    
    
    Piauí
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Piauí
    
    
    
    
    Bom dia Sábado
    
    
    
    
    PI TV 1ª edição
    
    
    
    
    PI TV 2ª Edição
    
    
    
    
    Clube Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Rio Grande do Norte
    
    
    
    
    
    nordeste
    
    
    
    Rio Grande do Norte
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia RN
    
    
    
    
    RN TV 1ª Edição
    
    
    
    
    RN TV 2ª edição
    
    
    
    
    Inter TV Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Sergipe
    
    
    
    
    
    nordeste
    
    
    
    Sergipe
    
    
    
    Primeira página
    
    
    
    
    Bom Dia SE
    
    
    
    
    SETV 1ª Edição
    
    
    
    
    SETV 2ª Edição
    
    
    
    
    Estação Agrícola
    
    
    
    
    Esporte
    
    
     
     
    
    
    norte
    
    
    
    
    
    Regiões
    
    
    
    norte
    
    
    
    Acre
    
    
    
    
    
    norte
    
    
    
    Acre
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Amazônia
    
    
    
    
    JAC 1ª Edição
    
    
    
    
    JAC 2ª Edição
    
    
    
    
    Globo Esporte Acre
    
    
     
    
    
    Amapá
    
    
    
    
    
    norte
    
    
    
    Amapá
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Amazônia
    
    
    
    
    JAP 1ª Edição
    
    
    
    
    JAP 2ª Edição
    
    
    
    
    Amazônia Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Amazonas
    
    
    
    
    
    norte
    
    
    
    Amazonas
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Amazônia
    
    
    
    
    JAM 1ª Edição
    
    
    
    
    JAM 2ª Edição
    
    
    
    
    Amazônia rural
    
    
    
    
    Esporte
    
    
     
    
    
    Pará
    
    
    
    
    
    norte
    
    
    
    Pará
    
    
    
    Belém e região
    
    
    
    
    
    Pará
    
    
    
    Belém e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Pará
    
    
    
    
    Jornal Liberal 1ª Edição
    
    
    
    
    Jornal Liberal 2ª Edição
    
    
    
    
    Liberal Comunidade
    
    
    
    
    É do Pará
    
    
    
    
    Esporte
    
    
     
    
    
    Santarém e região
    
    
    
    
    
    Pará
    
    
    
    Santarém e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Santarém
    
    
    
    
    Jornal Tapajós 1ª Edição
    
    
    
    
    Jornal Tapajós 2ª Edição
    
    
    
    
    Esporte
    
    
     
     
    
    
    Rondônia
    
    
    
    
    
    norte
    
    
    
    Rondônia
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Amazônia
    
    
    
    
    JRO 1ª Edição
    
    
    
    
    JRO 2ª Edição
    
    
    
    
    Amazônia Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Roraima
    
    
    
    
    
    norte
    
    
    
    Roraima
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Amazônia
    
    
    
    
    JRR 1ª Edição
    
    
    
    
    JRR 2ª Edição
    
    
    
    
    Amazônia Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Tocantins
    
    
    
    
    
    norte
    
    
    
    Tocantins
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Tocantins
    
    
    
    
    JA 1ª Edição
    
    
    
    
    JA 2ª Edição
    
    
    
    
    Jornal do Campo
    
    
    
    
    Esporte
    
    
     
     
    
    
    sudeste
    
    
    
    
    
    Regiões
    
    
    
    sudeste
    
    
    
    Espírito Santo
    
    
    
    
    
    sudeste
    
    
    
    Espírito Santo
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Espírito Santo
    
    
    
    
    ESTV 1ª Edição
    
    
    
    
    ESTV  2ª Edição
    
    
    
    
    Jornal do Campo
    
    
    
    
    Agronégocios
    
    
    
    
    Educação
    
    
    
    
    Concursos
    
    
    
    
    Esporte
    
    
     
    
    
    Minas Gerais
    
    
    
    
    
    sudeste
    
    
    
    Minas Gerais
    
    
    
    Belo Horizonte e região
    
    
    
    
    
    Minas Gerais
    
    
    
    Belo Horizonte e região
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Minas
    
    
    
    
    MG1
    
    
    
    
    MG2
    
    
    
    
    Rolê nas Gerais
    
    
    
    
    Terra de Minas
    
    
    
    
    pelas cozinhas de minas
    
    
    
    
    O que fazer em BH
    
    
    
    
    Esporte
    
    
     
    
    
    Centro-Oeste
    
    
    
    
    
    Minas Gerais
    
    
    
    Centro-Oeste
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Minas
    
    
    
    
    MG TV 1ª Edição
    
    
    
    
    MG TV 2ª Edição
    
    
    
    
    MG Rural
    
    
    
    
    Integração notícia
    
    
    
    
    Esporte
    
    
     
    
    
    Grande Minas
    
    
    
    
    
    Minas Gerais
    
    
    
    Grande Minas
    
    
    
    Primeira página
    
    
    
    
    Inter TV Notícia
    
    
    
    
    MG Inter TV 1ª Edição
    
    
    
    
    MG Inter TV 2ª Edição
    
    
    
    
    Inter TV Rural
    
    
    
    
    É o bicho
    
    
    
    
    Esporte
    
    
     
    
    
    Sul de Minas
    
    
    
    
    
    Minas Gerais
    
    
    
    Sul de Minas
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Cidade
    
    
    
    
    Jornal da EPTV 1ª Edição
    
    
    
    
    Jornal da EPTV 2ª Edição
    
    
    
    
    Terra da gente
    
    
    
    
    Esporte
    
    
     
    
    
    Triângulo Mineiro
    
    
    
    
    
    Minas Gerais
    
    
    
    Triângulo Mineiro
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Minas
    
    
    
    
    Uberlândia
    
    
    
    
    
    Triângulo Mineiro
    
    
    
    Uberlândia
    
    
    
    MG TV 1ª Edição
    
    
    
    
    MGTV 2ª edição 
    
    
     
    
    
    Uberaba
    
    
    
    
    
    Triângulo Mineiro
    
    
    
    Uberaba
    
    
    
    MGTV 1ª Edição
    
    
    
    
    MGTV 2ª Edição
    
    
     
    
    
    MG Rural
    
    
    
    
    Integração notícia
    
    
    
    
    Concursos
    
    
    
    
    Esporte
    
    
    
    
    Globo Esporte
    
    
     
    
    
    Vales de Minas Gerais
    
    
    
    
    
    Minas Gerais
    
    
    
    Vales de Minas Gerais
    
    
    
    Primeira Página
    
    
    
    
    Inter TV notícia
    
    
    
    
    MG Inter TV 1ª Edição
    
    
    
    
    MG Inter TV 2ª Edição
    
    
    
    
    Inter TV Rural
    
    
    
    
    É o bicho
    
    
    
    
    Esporte
    
    
     
    
    
    Zona da Mata
    
    
    
    
    
    Minas Gerais
    
    
    
    Zona da Mata
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Minas
    
    
    
    
    MG TV 1ª Edição
    
    
    
    
    MG TV 2ª Edição 
    
    
    
    
    MG Rural
    
    
    
    
    Integração notícia
    
    
    
    
    Esporte
    
    
    
    
    Globo Esporte
    
    
     
     
    
    
    Rio de Janeiro
    
    
    
    
    
    sudeste
    
    
    
    Rio de Janeiro
    
    
    
    Rio de Janeiro e região
    
    
    
    
    
    Rio de Janeiro
    
    
    
    Rio de Janeiro e região
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Rio
    
    
    
    
    RJ1
    
    
    
    
    RJ2
    
    
    
    
    Globo Comunidade RJ
    
    
    
    
    O que fazer no RJ
    
    
    
    
    Fora do ponto
    
    
    
    
    Esporte
    
    
     
    
    
    Norte Fluminense
    
    
    
    
    
    Rio de Janeiro
    
    
    
    Norte Fluminense
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Rio
    
    
    
    
    RJ TV Inter 1ª Edição
    
    
    
    
    RJ TV Inter 2ª Edição
    
    
    
    
    Inter TV Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Região dos Lagos
    
    
    
    
    
    Rio de Janeiro
    
    
    
    Região dos Lagos
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Rio
    
    
    
    
    RJ TV Inter 1ª Edição
    
    
    
    
    RJ TV Inter 2ª Edição
    
    
    
    
    Inter TV Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Região Serrana
    
    
    
    
    
    Rio de Janeiro
    
    
    
    Região Serrana
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Rio
    
    
    
    
    RJ TV Inter 1ª Edição
    
    
    
    
    RJ TV Inter 2ª Edição
    
    
    
    
    Inter TV Rural
    
    
    
    
    Esporte
    
    
     
    
    
    Sul e Costa Verde
    
    
    
    
    
    Rio de Janeiro
    
    
    
    Sul e Costa Verde
    
    
    
    Primeira Página
    
    
    
    
    Bom dia Rio
    
    
    
    
    RJ TV 1ª Edição
    
    
    
    
    RJ TV 2ª Edição
    
    
    
    
    Esporte
    
    
     
     
    
    
    São Paulo
    
    
    
    
    
    sudeste
    
    
    
    São Paulo
    
    
    
    São Paulo e região
    
    
    
    
    
    São Paulo
    
    
    
    São Paulo e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia SP
    
    
    
    
    SP1
    
    
    
    
    SP2
    
    
    
    
    Antena Paulista
    
    
    
    
    Mistura Paulista
    
    
    
    
    O que fazer em SP
    
    
    
    
    Esporte
    
    
     
    
    
    Bauru e Marília
    
    
    
    
    
    São Paulo
    
    
    
    Bauru e Marília
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia SP
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    Tem Notícias 1ª Edição
    
    
    
    
    Tem Notícias 2ª Edição
    
    
    
    
    Nosso Campo
    
    
    
    
    Esporte
    
    
     
    
    
    Campinas e região
    
    
    
    
    
    São Paulo
    
    
    
    Campinas e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    Jornal da EPTV 1ª Edição
    
    
    
    
    Jornal da EPTV 2ª Edição
    
    
    
    
    Terra da Gente
    
    
    
    
    Concursos
    
    
    
    
    Esporte
    
    
     
    
    
    Itapetininga e região
    
    
    
    
    
    São Paulo
    
    
    
    Itapetininga e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia SP
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    TEM Notícias 1ª Edição
    
    
    
    
    TEM Notícias 2ª Edição
    
    
    
    
    Antena Paulista
    
    
    
    
    Nosso Campo
    
    
    
    
    Resumo da Notícia
    
    
    
    
    Memória
    
    
    
    
    TEM Comunidade
    
    
    
    
    Esporte
    
    
     
    
    
    Mogi das Cruzes e Suzano
    
    
    
    
    
    São Paulo
    
    
    
    Mogi das Cruzes e Suzano
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Diário
    
    
    
    
    Diário TV 1ª Edição
    
    
    
    
    Diário TV 2ª Edição
    
    
    
    
    Diário Comunidade
    
    
    
    
    Concursos
    
    
    
    
    Esporte
    
    
     
    
    
    Piracicaba e região
    
    
    
    
    
    São Paulo
    
    
    
    Piracicaba e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    Jornal da EPTV 1ª Edição
    
    
    
    
    Jornal da EPTV 2ª Edição
    
    
    
    
    Terra da Gente
    
    
    
    
    Esporte
    
    
     
    
    
    Prudente e região
    
    
    
    
    
    São Paulo
    
    
    
    Prudente e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Fronteira
    
    
    
    
    Bom Dia SP
    
    
    
    
    Fronteira Notícias 1ª Edição
    
    
    
    
    Fronteira Notícias 2ª Edição
    
    
    
    
    Esporte
    
    
     
    
    
    Ribeirão Preto e Franca
    
    
    
    
    
    São Paulo
    
    
    
    Ribeirão Preto e Franca
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    Jornal da EPTV 1ª Edição
    
    
    
    
    Jornal da EPTV 2ª Edição
    
    
    
    
    Terra da Gente
    
    
    
    
    Esporte
    
    
     
    
    
    Rio Preto e Araçatuba
    
    
    
    
    
    São Paulo
    
    
    
    Rio Preto e Araçatuba
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia SP
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    TEM Notícias 1ª Edição
    
    
    
    
    TEM Notícias 2ª Edição
    
    
    
    
    Nosso Campo
    
    
    
    
    Esporte
    
    
     
    
    
    Santos e região
    
    
    
    
    
    São Paulo
    
    
    
    Santos e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Região
    
    
    
    
    Jornal Tribuna 1ª Edição
    
    
    
    
    Jornal Tribuna 2ª Edição
    
    
    
    
    Antena Paulista
    
    
    
    
    G1 em um Minuto Santos
    
    
    
    
    Viver Bem
    
    
    
    
    O Que Fazer Em Santos
    
    
    
    
    Culinária #13
    
    
    
    
    Por Dentro do Porto
    
    
    
    
    Esporte
    
    
     
    
    
    São Carlos e Araraquara
    
    
    
    
    
    São Paulo
    
    
    
    São Carlos e Araraquara
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    Jornal da EPTV 1ª Edição
    
    
    
    
    Jornal da EPTV 2ª edição
    
    
    
    
    Terra da Gente
    
    
     
    
    
    Sorocaba e Jundiaí
    
    
    
    
    
    São Paulo
    
    
    
    Sorocaba e Jundiaí
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia SP
    
    
    
    
    Bom Dia Cidade
    
    
    
    
    Tem Notícias 1ª Edição
    
    
    
    
    Tem notícias 2ª Edição
    
    
    
    
    Nosso Campo
    
    
    
    
    Esporte
    
    
     
    
    
    Vale do Paraíba e região
    
    
    
    
    
    São Paulo
    
    
    
    Vale do Paraíba e região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Vanguarda
    
    
    
    
    Link Vanguarda
    
    
    
    
    Jornal Vanguarda
    
    
    
    
    Vanguarda Comunidade
    
    
    
    
    Esporte
    
    
     
     
     
    
    
    sul
    
    
    
    
    
    Regiões
    
    
    
    sul
    
    
    
    Paraná
    
    
    
    
    
    sul
    
    
    
    Paraná
    
    
    
    Curitiba e Região
    
    
    
    
    
    Paraná
    
    
    
    Curitiba e Região
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Paraná
    
    
    
    
    Meio Dia Paraná
    
    
    
    
    Boa Noite Paraná
    
    
    
    
    Caminhos do Campo
    
    
    
    
    Bom Dia Sábado 
    
    
    
    
    Globo Esporte Paraná
    
    
     
    
    
    Campos Gerais e Sul
    
    
    
    
    
    Paraná
    
    
    
    Campos Gerais e Sul
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Paraná
    
    
    
    
    Meio Dia Paraná – Ponta Grossa 
    
    
    
    
    Boa Noite Paraná
    
    
    
    
    Caminhos do Campo
    
    
    
    
    Bom Dia Sábado 
    
    
    
    
    Globo Esporte Paraná
    
    
     
    
    
    Norte e Noroeste
    
    
    
    
    
    Paraná
    
    
    
    Norte e Noroeste
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Paraná
    
    
    
    
    Meio Dia Paraná – Maringá 
    
    
    
    
    Boa Noite Paraná
    
    
    
    
    Caminhos do Campo
    
    
    
    
    Meio Dia Paraná – Londrina 
    
    
    
    
    Meio Dia Paraná - Noroeste
    
    
    
    
    Bom Dia Sábado
    
    
    
    
    Globo Esporte Paraná
    
    
     
    
    
    Oeste e Sudoeste
    
    
    
    
    
    Paraná
    
    
    
    Oeste e Sudoeste
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Paraná
    
    
    
    
    Meio Dia Paraná – Foz do Iguaçu
    
    
    
    
    Boa Noite Paraná
    
    
    
    
    Caminhos do Campo
    
    
    
    
    Meio Dia Paraná – Cascavel 
    
    
    
    
    Bom Dia Sábado 
    
    
    
    
    Globo Esporte Paraná
    
    
     
     
    
    
    Rio Grande do Sul
    
    
    
    
    
    sul
    
    
    
    Rio Grande do Sul
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Rio Grande
    
    
    
    
    Jornal do Almoço
    
    
    
    
    RBS Notícias
    
    
    
    
    Campo e Lavoura
    
    
    
    
    Esporte
    
    
     
    
    
    Santa Catarina
    
    
    
    
    
    sul
    
    
    
    Santa Catarina
    
    
    
    Primeira Página
    
    
    
    
    Bom Dia Santa Catarina
    
    
    
    
    Jornal do Almoço
    
    
    
    
    NSC Notícias
    
    
    
    
    Nossa Santa Catarina
    
    
    
    
    Campo e Negócios
    
    
    
    
    Tech SC
    
    
    
    
    Esporte
    
    
     
     
     
    
    
    Telejornais
    
    
    
    
    
    menu g1
    
    
    
    Telejornais
    
    
    
    Bom Dia Brasil
    
    
    
    
    
    Telejornais
    
    
    
    Bom Dia Brasil
    
    
    
    Primeira Página
    
    
    
    
    Redação
    
    
    
    
    História
    
    
    
    
    Vídeos
    
    
     
    
    
    Fantástico
    
    
    
    
    
    Telejornais
    
    
    
    Fantástico
    
    
    
    Primeira Página
    
    
    
    
    quadros e séries
    
    
    
    
    
    Fantástico
    
    
    
    quadros e séries
    
    
    
    repórter por um dia
    
    
    
    
    shows e musicais
    
    
    
    
    gols do fantástico
    
    
     
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no fantástico
    
    
     
    
    
    G1  em 1 Minuto
    
    
    
    
    Globo Repórter
    
    
    
    
    
    Telejornais
    
    
    
    Globo Repórter
    
    
    
    Primeira Página
    
    
    
    
    redação
    
    
    
    
    história
    
    
    
    
    receitas
    
    
    
    
    testes
    
    
    
    
    vídeos
    
    
    
    
    vc no globo repórter
    
    
     
    
    
    Globo Rural
    
    
    
    
    
    Telejornais
    
    
    
    Globo Rural
    
    
    
    Primeira Página
    
    
    
    
    agro
    
    
    
    
    guia do globo rural
    
    
    
    
    revista globo rural
    
    
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no globo rural
    
    
     
    
    
    Hora 1
    
    
    
    
    
    Telejornais
    
    
    
    Hora 1
    
    
    
    Primeira Página
    
    
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no hora um
    
    
     
    
    
    Jornal da Globo
    
    
    
    
    
    Telejornais
    
    
    
    Jornal da Globo
    
    
    
    Primeira Página
    
    
    
    
    redação
    
    
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no jg
    
    
     
    
    
    Jornal Hoje
    
    
    
    
    
    Telejornais
    
    
    
    Jornal Hoje
    
    
    
    Primeira Página
    
    
    
    
    crônicas
    
    
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no jh
    
    
     
    
    
    Jornal Nacional
    
    
    
    
    
    Telejornais
    
    
    
    Jornal Nacional
    
    
    
    Primeira Página
    
    
    
    
    Brasil em Constituição
    
    
    
    
    jornal nacional 50 anos
    
    
    
    
    redação
    
    
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no jornal nacional
    
    
     
    
    
    Pequenas Empresas
    
    
    
    
    
    Telejornais
    
    
    
    Pequenas Empresas
    
    
    
    Primeira Página
    
    
    
    
    pme
    
    
    
    
    quadros
    
    
    
    
    
    Pequenas Empresas
    
    
    
    quadros
    
    
    
    pegn.tec
    
    
     
    
    
    contato das empresas
    
    
    
    
    revista pegn
    
    
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no pegn
    
    
     
    
    
    Profissão Repórter
    
    
    
    
    
    Telejornais
    
    
    
    Profissão Repórter
    
    
    
    Primeira Página
    
    
    
    
    equipe
    
    
    
    
    história
    
    
    
    
    vídeos
    
    
    
    
    vc no profissão repórter
    
    
     
     
    
    
    GloboNews
    
    
    
    
    
    menu g1
    
    
    
    GloboNews
    
    
    
    Primeira Página
    
    
    
    
    jornais
    
    
    
    
    
    GloboNews
    
    
    
    jornais
    
    
    
    Estúdio i
    
    
    
    
    GloboNews Em Pauta
    
    
    
    
    GloboNews em Ponto
    
    
    
    
    Jornal das Dez
    
    
    
    
    Jornal GloboNews
    
    
    
    
    Conexão GloboNews
    
    
    
    
    GloboNews Mais
    
    
    
    
    Edição das 18
    
    
    
    
    Especial de Domingo
    
    
     
    
    
    programas
    
    
    
    
    
    GloboNews
    
    
    
    programas
    
    
    
    cidades e soluções
    
    
    
    
    Central das Eleições
    
    
    
    
    diálogos com mario sergio conti
    
    
    
    
    Fernando Gabeira
    
    
    
    
    globonews documentário
    
    
    
    
    globonews internacional
    
    
    
    
    globonews miriam leitão
    
    
    
    
    Papo de Política
    
    
    
    
    roberto d'avila
    
    
     
    
    
    podcasts
    
    
    
    
    
    GloboNews
    
    
    
    podcasts
    
    
    
    as histórias na globonews
    
    
    
    
    em movimento
    
    
    
    
    globonews internacional
    
    
    
    
    hub globonews
    
    
    
    
    papo de política
    
    
     
    
    
    globonews ao vivo
    
    
    
    
    Converse com outras ideias
    
    
    
    
    canais globo
    
    
    
    
    programação
    
    
    
    
    redes sociais
    
    
    
    
    
    GloboNews
    
    
    
    redes sociais
    
    
    
    globonews
    
    
    
    
    time globonews
    
    
     
    
    
    História
    
    
    
    
    --
    
    
    
    
    grupo globo
    
    
    
    
    princípios editoriais
    
    
     
    
    
    Blogs e Colunas
    
    
    
    
    Podcasts
    
    
    
    
    
    menu g1
    
    
    
    Podcasts
    
    
    
    Todos
    
    
    
    
    o assunto
    
    
    
    
    Abuso
    
    
    
    
    À Mão Armada
    
    
    
    
    bem estar
    
    
    
    
    Cadê meu trampo
    
    
    
    
    desenrola, rio
    
    
    
    
    De onde vem o que eu como
    
    
    
    
    educação financeira
    
    
    
    
    Escuta Que O Filho É Teu
    
    
    
    
    Frango com Quiabo
    
    
    
    
    Funciona Assim
    
    
    
    
    g1 ouviu
    
    
    
    
    isso é fantástico
    
    
    
    
    meu pedaço
    
    
    
    
    papo de política
    
    
    
    
    Resumão Diário
    
    
    
    
    Prazer, Renata
    
    
    
    
    Bichos na Escuta
    
    
    
    
    Isso Está Acontecendo
    
    
     
    
    
    Serviços
    
    
    
    
    
    menu g1
    
    
    
    Serviços
    
    
    
    App g1
    
    
    
    
    Calculadoras
    
    
    
    
    Loterias
    
    
    
    
    Newsletter
    
    
    
    
    Previsão do Tempo
    
    
    
    
    Climatempo
    
    
     
    
    
    Vídeos
    
    
    
    
    Newsletter
    
    
    
    
    Webstories
    
    
    
    
    Especial Publicitário
    
    
    
    
    
    menu g1
    
    
    
    Especial Publicitário
    
    
    
    Bradesco
    
    
    
    
    Brumadinho – Reparação e Desenvolvimento
    
    
    
    
    Duque de Caxias
    
    
    
    
    GSK/HIV Heathcare
    
    
    
    
    ibp
    
    
    
    
    Na Estrada com quem faz
    
    
    
    
    Nissan
    
    
    
    
    Inteligência Financeira
    
    
    
    
    Praia Limpa
    
    
    
    
    VAE
    
    
    
    
    Voz dos Oceanos
    
    
     
    
    
    --
    
    
    
    
    Princípios editoriais
    
    
    
    
    Sobre o g1
    
    
    
    
    App g1
    
    
    
    
    Equipe
    
    
    
    
    Entre em contato
    
    
    
    
    Termos de uso do g1
    
    
     
    
    
    
    
    
    
    Acesse sua conta ou cadastre-se grátis
    
    
    
    
    
    
    
    
    
    
    
    
    grupo globo
    
    
    
    
    
    
    
    
    
    
    
    
    sair da conta
    
    
    
    
    
    
    
    
    
            



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

    Quem é Danilo Tandera, o miliciano mais procurado do RJ .
    Treinador de futsal denunciado por assediar jogadoras morre na cadeia.
    Fonte: G1/Globo
    
     
    Se o dinheiro está caro, a culpa não é do BC, porque é malvado, mas do governo, que deve muito, diz Campos Neto à CNN.
    Ciência e Tecnologia.
    Fonte: CNN Brasil
    
     
    Podcast busca entender como brasileiros chegaram a atual grau de divisão; ouça aqui.
    Facebook.
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
     
    Quem é Danilo Tandera, o miliciano mais procurado do RJ .
    Treinador de futsal denunciado por assediar jogadoras morre na cadeia.
    
    
    
    Portal de Notícias CNN Brasil
     
    Se o dinheiro está caro, a culpa não é do BC, porque é malvado, mas do governo, que deve muito, diz Campos Neto à CNN.
    Ciência e Tecnologia.
    
    
    
    Portal de Notícias BBC Brasil
     
    Podcast busca entender como brasileiros chegaram a atual grau de divisão; ouça aqui.
    Facebook.
    
    
    


# Sobre

## Dimensão Alfa

Dimensão Alfa projetos e conteúdos de tecnologia.

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


```python

```
