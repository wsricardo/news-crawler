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

    /tmp/ipykernel_43998/1468998341.py:8: DeprecationWarning: Importing display from IPython.core.display is deprecated since IPython 7.14, please import from IPython display
      from IPython.core.display import display, HTML


# Modelagem Portal G1



Capturando noticias do portal G1 da Globo
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

    https://g1.globo.com/economia/noticia/2022/11/05/por-que-lula-vai-precisar-de-um-ministro-mais-politico-do-que-tecnico-para-a-economia.ghtml
    
    
    dict_keys(['titulo', 'url'])




 <b>Economia deverá ter ministro mais político do que técnico para negociar</b>

<br><br> Page: <a href="https://g1.globo.com/economia/noticia/2022/11/05/por-que-lula-vai-precisar-de-um-ministro-mais-politico-do-que-tecnico-para-a-economia.ghtml"> G1/Globo 



```python
#soup1 = BeautifulSoup
dw


```




    [{'titulo': 'Economia deverá ter ministro mais político do que técnico para negociar',
      'url': 'https://g1.globo.com/economia/noticia/2022/11/05/por-que-lula-vai-precisar-de-um-ministro-mais-politico-do-que-tecnico-para-a-economia.ghtml'},
     {'titulo': 'Marília Mendonça colocou mulheres como protagonistas no sertanejo ',
      'url': 'https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/marilia-mendonca-lider-do-movimento-que-colocou-as-mulheres-como-protagonistas-da-musica-sertaneja.ghtml'},
     {'titulo': "Avó não voltou à casa de Marília: 'Dói até na alma'",
      'url': 'https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/avo-de-marilia-mendonca-conta-que-nao-teve-coragem-de-voltar-a-casa-da-cantora-apos-perder-neta-e-filho-doi-ate-na-alma.ghtml'},
     {'titulo': 'Frio diminui no país; veja a previsão para o fim de semana',
      'url': 'https://www.climatempo.com.br/noticia/2022/11/05/chove-forte-nordeste-ar-seco-predomina-e-frio-diminui-no-pais--8076'},
     {'titulo': 'Incêndio em boate na Rússia mata 13 pessoas',
      'url': 'https://g1.globo.com/mundo/noticia/2022/11/05/incendio-em-boate-na-russia-deixa-mortos.ghtml'},
     {'titulo': 'Coreia do Sul e EUA fazem sobrevoos após novos disparos da Coreia do Norte',
      'url': 'https://g1.globo.com/mundo/noticia/2022/11/05/coreia-do-norte-volta-a-disparar-misseis-dizem-sul-coreanos.ghtml'},
     {'titulo': 'Ativistas climáticos protestam sentados embaixo de jatos em aeroporto',
      'url': 'https://g1.globo.com/mundo/noticia/2022/11/05/ativistas-climaticos-protestam-contra-poluicao-aerea-em-patio-de-aeroporto-da-holanda.ghtml'},
     {'titulo': '2,7 mil celulares são bloqueados por dia no Brasil por roubo ou perda',
      'url': 'https://g1.globo.com/tecnologia/noticia/2022/11/05/brasil-tem-27-mil-celulares-bloqueados-por-dia-contra-roubos-e-perdas.ghtml'}]



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

    [<a class="feed-post-link gui-color-primary gui-color-hover" elementtiming="text-ssr" href="https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/marilia-mendonca-lider-do-movimento-que-colocou-as-mulheres-como-protagonistas-da-musica-sertaneja.ghtml">Marília Mendonça colocou mulheres como protagonistas no sertanejo </a>]
    Número de noticias 8



<h3 style="padding: 2px;"> Economia deverá ter ministro mais político do que técnico para negociar</h3><a href="https://g1.globo.com/economia/noticia/2022/11/05/por-que-lula-vai-precisar-de-um-ministro-mais-politico-do-que-tecnico-para-a-economia.ghtml" style="padding: 1px; margin: 0;" >Leia mais</a> <h3 style="padding: 2px;"> Marília Mendonça colocou mulheres como protagonistas no sertanejo </h3><a href="https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/marilia-mendonca-lider-do-movimento-que-colocou-as-mulheres-como-protagonistas-da-musica-sertaneja.ghtml" style="padding: 1px; margin: 0;" >Leia mais</a> <h3 style="padding: 2px;"> Avó não voltou à casa de Marília: 'Dói até na alma'</h3><a href="https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/avo-de-marilia-mendonca-conta-que-nao-teve-coragem-de-voltar-a-casa-da-cantora-apos-perder-neta-e-filho-doi-ate-na-alma.ghtml" style="padding: 1px; margin: 0;" >Leia mais</a> <h3 style="padding: 2px;"> Frio diminui no país; veja a previsão para o fim de semana</h3><a href="https://www.climatempo.com.br/noticia/2022/11/05/chove-forte-nordeste-ar-seco-predomina-e-frio-diminui-no-pais--8076" style="padding: 1px; margin: 0;" >Leia mais</a> <h3 style="padding: 2px;"> Incêndio em boate na Rússia mata 13 pessoas</h3><a href="https://g1.globo.com/mundo/noticia/2022/11/05/incendio-em-boate-na-russia-deixa-mortos.ghtml" style="padding: 1px; margin: 0;" >Leia mais</a> <h3 style="padding: 2px;"> Coreia do Sul e EUA fazem sobrevoos após novos disparos da Coreia do Norte</h3><a href="https://g1.globo.com/mundo/noticia/2022/11/05/coreia-do-norte-volta-a-disparar-misseis-dizem-sul-coreanos.ghtml" style="padding: 1px; margin: 0;" >Leia mais</a> <h3 style="padding: 2px;"> Ativistas climáticos protestam sentados embaixo de jatos em aeroporto</h3><a href="https://g1.globo.com/mundo/noticia/2022/11/05/ativistas-climaticos-protestam-contra-poluicao-aerea-em-patio-de-aeroporto-da-holanda.ghtml" style="padding: 1px; margin: 0;" >Leia mais</a> <h3 style="padding: 2px;"> 2,7 mil celulares são bloqueados por dia no Brasil por roubo ou perda</h3><a href="https://g1.globo.com/tecnologia/noticia/2022/11/05/brasil-tem-27-mil-celulares-bloqueados-por-dia-contra-roubos-e-perdas.ghtml" style="padding: 1px; margin: 0;" >Leia mais</a>



```python
news2 = '<h1 style="padding: 12px;">Notícias</h1>'
news2 += '<br><br>'.join( [ '<br>'.join( [ str( i['titulo'] ) , str( i[ 'url' ]  ) ] ) for i in dw ] )
display( HTML( news2 ))
```


<h1 style="padding: 12px;">Notícias</h1>Economia deverá ter ministro mais político do que técnico para negociar<br>https://g1.globo.com/economia/noticia/2022/11/05/por-que-lula-vai-precisar-de-um-ministro-mais-politico-do-que-tecnico-para-a-economia.ghtml<br><br>Marília Mendonça colocou mulheres como protagonistas no sertanejo <br>https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/marilia-mendonca-lider-do-movimento-que-colocou-as-mulheres-como-protagonistas-da-musica-sertaneja.ghtml<br><br>Avó não voltou à casa de Marília: 'Dói até na alma'<br>https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/avo-de-marilia-mendonca-conta-que-nao-teve-coragem-de-voltar-a-casa-da-cantora-apos-perder-neta-e-filho-doi-ate-na-alma.ghtml<br><br>Frio diminui no país; veja a previsão para o fim de semana<br>https://www.climatempo.com.br/noticia/2022/11/05/chove-forte-nordeste-ar-seco-predomina-e-frio-diminui-no-pais--8076<br><br>Incêndio em boate na Rússia mata 13 pessoas<br>https://g1.globo.com/mundo/noticia/2022/11/05/incendio-em-boate-na-russia-deixa-mortos.ghtml<br><br>Coreia do Sul e EUA fazem sobrevoos após novos disparos da Coreia do Norte<br>https://g1.globo.com/mundo/noticia/2022/11/05/coreia-do-norte-volta-a-disparar-misseis-dizem-sul-coreanos.ghtml<br><br>Ativistas climáticos protestam sentados embaixo de jatos em aeroporto<br>https://g1.globo.com/mundo/noticia/2022/11/05/ativistas-climaticos-protestam-contra-poluicao-aerea-em-patio-de-aeroporto-da-holanda.ghtml<br><br>2,7 mil celulares são bloqueados por dia no Brasil por roubo ou perda<br>https://g1.globo.com/tecnologia/noticia/2022/11/05/brasil-tem-27-mil-celulares-bloqueados-por-dia-contra-roubos-e-perdas.ghtml



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

    Número de noticias capturadas: 8



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




    ['Por que Lula vai precisar de um ministro mais político do que técnico para a Economia?',
     'Principais políticas propostas por Lula precisam passar por aprovação do Congresso, com uma composição com bastante oposição ao presidente eleito. Capacidade de negociar vai ser necessária para garantir cumprimento das promessas de campanha.',
     ' Além dos desafios naturais da gestão da economia em um governo, o presidente eleito Luiz Inácio Lula da Silva (PT) precisará que seu ministro ou ministra da pasta tenha capacidade de barganhar com o Congresso Nacional para conseguir tocar promessas feitas durante a campanha. ']




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

    Olá. Bem vindo e bem vinda ao nosso noticiário diário. Eu sou Ani Fátima Liu e apresentarei as principais noticias. 
    Por que Lula vai precisar de um ministro mais político do que técnico para a Economia?Principais políticas propostas por Lula precisam passar por aprovação do Congresso, com uma composição com bastante oposição ao presidente eleito. Capacidade de negociar vai ser necessária para garantir cumprimento das promessas de campanha. Além dos desafios naturais da gestão da economia em um governo, o presidente eleito Luiz Inácio Lula da Silva (PT) precisará que seu ministro ou ministra da pasta tenha capacidade de barganhar com o Congresso Nacional para conseguir tocar promessas feitas durante a campanha. Agora vamos a nossa próxima notícia.
    Marília Mendonça: líder do movimento que colocou as mulheres como protagonistas da música sertaneja Considerada por músicos e especialistas como a líder de um movimento transformador dentro do sertanejo, Marília é apontada como um divisor de águas no gênero musical e como uma lacuna que jamais será preenchida.  Do microfone do barzinho aos maiores palcos do Brasil, Marília Mendonça não inspirou apenas fãs, mas também mulheres que usam o poder da voz para cantar o que vai muito além da música, a representatividade. Agora vamos a nossa próxima notícia.
    Avó de Marília Mendonça conta que não teve coragem de voltar à casa da cantora após perder neta e filho: 'Dói até na alma'Aos 80 anos, Teresa Vieira relata que soube pela televisão que a artista e Abicelí Silveira tinham morrido no acidente aéreo. Na parede da sala, ela guarda fotos deles e as olha todos os dias.  Falar de Marília Mendonça para Teresa de Jesus Vieira, de 80 anos, avó da cantora, ainda é difícil sem que ela se emocione e precise fazer pausas para retomar o ânimo. A imagem da neta a chamando de "minha vózinha" está tão recente e presente que a idosa não teve coragem de voltar à casa da cantora depois que ela morreu, há um ano, num acidente de avião, o qual também causou a morte de Abicelí Silveira, filho de Teresa que trabalhava com a artista. Agora vamos a nossa próxima notícia.
    



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




    <section class="hot__content"> <div class="container splide__track"> <ul class="hot__list splide__list"> <li class="hot__list__itens splide__slide"> <a href="https://www.cnnbrasil.com.br/politica/pouco-antes-de-quebrar-o-silencio-bolsonaro-consultou-exercito-sobre-judicializar-eleicoes-e-nao-teve-apoio-segundo-oficiais-ouvidos-pela-cnn/" target="_self" title="ANTES DE PRONUNCIAMENTO Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio"><img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/Reuters_Direct_Media/BrazilOnlineReportTopNews/tagreuters.com2022binary_LYNXMPEIA01P1-FILEDIMAGE.jpg?w=65&amp;h=37&amp;crop=1" title="ANTES DE PRONUNCIAMENTO Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio"/><div class="i_ch"><i class=""></i> <span class="ch">ANTES DE PRONUNCIAMENTO</span></div><span class="tp">Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio</span></a>  </li> <li class="hot__list__itens splide__slide"> <a href="https://www.cnnbrasil.com.br/politica/justica-do-rio-recebe-noticia-crime-contra-atriz-cassia-kis-por-declaracoes-homofobicas/" target="_self" title="ACUSADA DE HOMOFOBIA Justiça do Rio recebe notícia-crime contra atriz Cássia Kis"><img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2022/11/cassiakis.png?w=65&amp;h=37&amp;crop=1" title="ACUSADA DE HOMOFOBIA Justiça do Rio recebe notícia-crime contra atriz Cássia Kis"/><div class="i_ch"><i class=""></i> <span class="ch">ACUSADA DE HOMOFOBIA</span></div><span class="tp">Justiça do Rio recebe notícia-crime contra atriz Cássia Kis</span></a>  </li> <li class="hot__list__itens splide__slide"> <a href="https://www.cnnbrasil.com.br/business/mp-do-tcu-pede-suspensao-de-pagamento-antecipado-de-megadividendos-da-petrobras/" target="_self" title="PETROBRAS MP do TCU pede suspensão de pagamento antecipado de “megadividendos”"><img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/Reuters_Direct_Media/BrazilOnlineReportTopNews/tagreuters.com2022binary_LYNXMPEIA30O3-FILEDIMAGE.jpg?w=65&amp;h=37&amp;crop=1" title="PETROBRAS MP do TCU pede suspensão de pagamento antecipado de “megadividendos”"/><div class="i_ch"><i class=""></i> <span class="ch">PETROBRAS</span></div><span class="tp">MP do TCU pede suspensão de pagamento antecipado de “megadividendos”</span></a>  </li> <li class="hot__list__itens splide__slide"> <a href="https://www.cnnbrasil.com.br/tudo-sobre/manifestacoes/" target="_self" title="MANIFESTAÇÕES "><img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/Reuters_Direct_Media/BrazilOnlineReportWorldNews/tagreuters.com2022binary_LYNXMPEI9H0XR-FILEDIMAGE.jpg?w=65&amp;h=37&amp;crop=1" title="MANIFESTAÇÕES "/><div class="i_ch"><i class=""></i> <span class="ch">MANIFESTAÇÕES</span></div><span class="tp"></span></a>  </li> <li class="hot__list__itens splide__slide"> <a href="https://www.cnnbrasil.com.br/loterias/" target="_self" title="LOTERIAS "><img class="tb" src="https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2021/11/maleta-bolinhas.png?w=65&amp;h=37&amp;crop=1" title="LOTERIAS "/><div class="i_ch"><i class=""></i> <span class="ch">LOTERIAS</span></div><span class="tp"></span></a>  </li> </ul> </div> </section>




```python
c = cnn_nw_data[0].find('a')
#dir(c)

```


```python
c.attrs
```




    {'href': 'https://www.cnnbrasil.com.br/politica/pouco-antes-de-quebrar-o-silencio-bolsonaro-consultou-exercito-sobre-judicializar-eleicoes-e-nao-teve-apoio-segundo-oficiais-ouvidos-pela-cnn/',
     'title': 'ANTES DE PRONUNCIAMENTO Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio',
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

    [{'title': 'ANTES DE PRONUNCIAMENTO Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio', 'href': 'https://www.cnnbrasil.com.br/politica/pouco-antes-de-quebrar-o-silencio-bolsonaro-consultou-exercito-sobre-judicializar-eleicoes-e-nao-teve-apoio-segundo-oficiais-ouvidos-pela-cnn/'}, {'title': 'Lula articula base aliada no Congresso para se contrapor a ala bolsonarista', 'href': 'https://www.cnnbrasil.com.br/politica/lula-articula-base-aliada-no-congresso-para-se-contrapor-a-ala-bolsonarista/'}, {'title': 'Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio, dizem oficiais', 'href': 'https://www.cnnbrasil.com.br/politica/pouco-antes-de-quebrar-o-silencio-bolsonaro-consultou-exercito-sobre-judicializar-eleicoes-e-nao-teve-apoio-segundo-oficiais-ouvidos-pela-cnn/'}, {'title': 'Valdemar deve anunciar oposição a Lula, mas trabalha por "atuação responsável"', 'href': 'https://www.cnnbrasil.com.br/politica/valdemar-deve-anunciar-oposicao-a-governo-lula-mas-trabalha-por-atuacao-responsavel-do-pl/'}, {'title': 'Twitter tem “queda maciça na receita” após anunciantes interromperem investimentos', 'href': 'https://www.cnnbrasil.com.br/business/twitter-tem-queda-macica-na-receita-apos-anunciantes-interromperem-investimentos/'}, {'title': 'Setor hoteleiro de Brasília estima ocupação de 90% para posse de Lula', 'href': 'https://www.cnnbrasil.com.br/business/setor-hoteleiro-de-brasilia-estima-ocupacao-de-90-para-posse-de-lula/'}, {'title': 'Polícia Civil de MG apresenta relatório sobre o acidente com Marília Mendonça', 'href': 'https://www.cnnbrasil.com.br/nacional/policia-civil-de-mg-apresenta-relatorio-sobre-o-acidente-com-marilia-mendonca/'}, {'title': 'Veja quais autoridades do atual e novo governo participam do evento global', 'href': 'https://www.cnnbrasil.com.br/nacional/cop27-veja-quais-autoridades-do-atual-e-novo-governo-participam-do-evento-global/'}, {'title': 'Fiocruz aponta aumento de casos de vírus sincicial respiratório em crianças', 'href': 'https://www.cnnbrasil.com.br/saude/fiocruz-aponta-aumento-de-casos-de-virus-sincicial-respiratorio-em-criancas/'}, {'title': 'Fim de semana na cidade de São Paulo deve ter sol, mas temperaturas continuam baixas', 'href': 'https://www.cnnbrasil.com.br/nacional/fim-de-semana-na-cidade-de-sao-paulo-deve-ter-sol-mas-temperaturas-continuam-baixas/'}, {'title': 'O futuro do euro: entenda as perspectivas para a economia europeia', 'href': 'https://www.cnnbrasil.com.br/business/o-futuro-do-euro-entenda-as-perspectivas-para-a-economia-europeia/'}, {'title': 'Pessoas trans em situação de vulnerabilidade se formam em capacitação do Einstein em SP', 'href': 'https://www.cnnbrasil.com.br/nacional/pessoas-trans-em-situacao-de-vulnerabilidade-se-formam-em-capacitacao-do-einstein-em-sp/'}, {'title': 'Piqué, do Barça, anuncia o último jogo da carreira', 'href': 'https://www.cnnbrasil.com.br/esporte/jogador-pique-do-barcelona-anuncia-que-jogara-o-ultimo-jogo-da-carreira-no-sabado-5/'}, {'title': 'Filho mais velho de Tom Jobim morre aos 72 anos no Rio', 'href': 'https://www.cnnbrasil.com.br/entretenimento/paulo-jobim-filho-mais-velho-de-tom-jobim-morre-no-rio-de-janeiro-aos-72-anos/'}, {'title': 'Saiba quais os cuidados e as regras no transporte de pets em viagens de avião', 'href': 'https://viagemegastronomia.cnnbrasil.com.br/noticias/cuidados-regras-transporte-de-pets-em-viagens-de-aviao/'}, {'title': 'Turista brasileiro morre na Argentina após ser atingido por placa de gelo em caverna', 'href': 'https://www.cnnbrasil.com.br/internacional/turista-brasileiro-morre-na-argentina-apos-ser-atingido-por-placa-de-gelo-em-caverna/'}]



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

    
    ANTES DE PRONUNCIAMENTO Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio 
    https://www.cnnbrasil.com.br/politica/pouco-antes-de-quebrar-o-silencio-bolsonaro-consultou-exercito-sobre-judicializar-eleicoes-e-nao-teve-apoio-segundo-oficiais-ouvidos-pela-cnn/
    
    
    
    Lula articula base aliada no Congresso para se contrapor a ala bolsonarista 
    https://www.cnnbrasil.com.br/politica/lula-articula-base-aliada-no-congresso-para-se-contrapor-a-ala-bolsonarista/
    
    
    
    Bolsonaro consultou Exército sobre judicializar eleições e não teve apoio, dizem oficiais 
    https://www.cnnbrasil.com.br/politica/pouco-antes-de-quebrar-o-silencio-bolsonaro-consultou-exercito-sobre-judicializar-eleicoes-e-nao-teve-apoio-segundo-oficiais-ouvidos-pela-cnn/
    
    
    
    Valdemar deve anunciar oposição a Lula, mas trabalha por "atuação responsável" 
    https://www.cnnbrasil.com.br/politica/valdemar-deve-anunciar-oposicao-a-governo-lula-mas-trabalha-por-atuacao-responsavel-do-pl/
    
    
    
    Twitter tem “queda maciça na receita” após anunciantes interromperem investimentos 
    https://www.cnnbrasil.com.br/business/twitter-tem-queda-macica-na-receita-apos-anunciantes-interromperem-investimentos/
    
    
    
    Setor hoteleiro de Brasília estima ocupação de 90% para posse de Lula 
    https://www.cnnbrasil.com.br/business/setor-hoteleiro-de-brasilia-estima-ocupacao-de-90-para-posse-de-lula/
    
    
    
    Polícia Civil de MG apresenta relatório sobre o acidente com Marília Mendonça 
    https://www.cnnbrasil.com.br/nacional/policia-civil-de-mg-apresenta-relatorio-sobre-o-acidente-com-marilia-mendonca/
    
    
    
    Veja quais autoridades do atual e novo governo participam do evento global 
    https://www.cnnbrasil.com.br/nacional/cop27-veja-quais-autoridades-do-atual-e-novo-governo-participam-do-evento-global/
    
    
    
    Fiocruz aponta aumento de casos de vírus sincicial respiratório em crianças 
    https://www.cnnbrasil.com.br/saude/fiocruz-aponta-aumento-de-casos-de-virus-sincicial-respiratorio-em-criancas/
    
    
    
    Fim de semana na cidade de São Paulo deve ter sol, mas temperaturas continuam baixas 
    https://www.cnnbrasil.com.br/nacional/fim-de-semana-na-cidade-de-sao-paulo-deve-ter-sol-mas-temperaturas-continuam-baixas/
    
    
    
    O futuro do euro: entenda as perspectivas para a economia europeia 
    https://www.cnnbrasil.com.br/business/o-futuro-do-euro-entenda-as-perspectivas-para-a-economia-europeia/
    
    
    
    Pessoas trans em situação de vulnerabilidade se formam em capacitação do Einstein em SP 
    https://www.cnnbrasil.com.br/nacional/pessoas-trans-em-situacao-de-vulnerabilidade-se-formam-em-capacitacao-do-einstein-em-sp/
    
    
    
    Piqué, do Barça, anuncia o último jogo da carreira 
    https://www.cnnbrasil.com.br/esporte/jogador-pique-do-barcelona-anuncia-que-jogara-o-ultimo-jogo-da-carreira-no-sabado-5/
    
    
    
    Filho mais velho de Tom Jobim morre aos 72 anos no Rio 
    https://www.cnnbrasil.com.br/entretenimento/paulo-jobim-filho-mais-velho-de-tom-jobim-morre-no-rio-de-janeiro-aos-72-anos/
    
    
    
    Saiba quais os cuidados e as regras no transporte de pets em viagens de avião 
    https://viagemegastronomia.cnnbrasil.com.br/noticias/cuidados-regras-transporte-de-pets-em-viagens-de-aviao/
    
    
    
    Turista brasileiro morre na Argentina após ser atingido por placa de gelo em caverna 
    https://www.cnnbrasil.com.br/internacional/turista-brasileiro-morre-na-argentina-apos-ser-atingido-por-placa-de-gelo-em-caverna/
    
    



```python
len(dw)
```




    8




```python
len(cnn_list_news)
```




    16



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




    "Vitória do 'campo democrático' encerra ciclo dos protestos de 2013, diz pesquisador"




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

    Número de notícias: 71



```python
random.choices(bbc_news_lists, k = 3)
```




    [{'title': 'O que é o artigo 142 da Constituição',
      'href': 'https://www.bbc.com/portuguese/brasil-52857654'},
     {'title': "A descoberta sobre 'matéria escura' que pode mudar o tratamento do câncer",
      'href': 'https://www.bbc.com/portuguese/geral-63425540'},
     {'title': 'Vídeo, A metamorfose do voto na maior cidade do país, Duration 13,36',
      'href': 'https://www.bbc.com/portuguese/brasil-63456545'}]




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

    Avó não voltou à casa de Marília: 'Dói até na alma'. 
    https://g1.globo.com/go/goias/um-ano-sem-marilia/noticia/2022/11/05/avo-de-marilia-mendonca-conta-que-nao-teve-coragem-de-voltar-a-casa-da-cantora-apos-perder-neta-e-filho-doi-ate-na-alma.ghtml
    
    Incêndio em boate na Rússia mata 13 pessoas. 
    https://g1.globo.com/mundo/noticia/2022/11/05/incendio-em-boate-na-russia-deixa-mortos.ghtml
    
    Fonte: G1/Globo
    
    
    Pessoas trans em situação de vulnerabilidade se formam em capacitação do Einstein em SP. 
    https://www.cnnbrasil.com.br/nacional/pessoas-trans-em-situacao-de-vulnerabilidade-se-formam-em-capacitacao-do-einstein-em-sp/
    
    Saiba quais os cuidados e as regras no transporte de pets em viagens de avião. 
    https://viagemegastronomia.cnnbrasil.com.br/noticias/cuidados-regras-transporte-de-pets-em-viagens-de-aviao/
    
    Fonte: CNN Brasil
    
    
    Vídeo, O que números revelam sobre resultado da eleição, Duration 5,32. 
    https://www.bbc.com/portuguese/brasil-63465066
    
    Crise dos mísseis de Cuba: como os EUA prepararam áreas para ataque soviético. 
    https://www.bbc.com/portuguese/internacional-63420870
    
    Fonte: BBC Brasil
    
    



```python
i = j = None

for i in news_list:
    for j in i['title']:
        print(f'{j[0]}.')
    print(f'Fonte: {i["source"] }\n\n ' )
```

    Avó não voltou à casa de Marília: 'Dói até na alma'.
    Incêndio em boate na Rússia mata 13 pessoas.
    Fonte: G1/Globo
    
     
    Pessoas trans em situação de vulnerabilidade se formam em capacitação do Einstein em SP.
    Saiba quais os cuidados e as regras no transporte de pets em viagens de avião.
    Fonte: CNN Brasil
    
     
    Vídeo, O que números revelam sobre resultado da eleição, Duration 5,32.
    Crise dos mísseis de Cuba: como os EUA prepararam áreas para ataque soviético.
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
     
    Avó não voltou à casa de Marília: 'Dói até na alma'.
    Incêndio em boate na Rússia mata 13 pessoas.
    
    
    
    Portal de Notícias CNN Brasil
     
    Pessoas trans em situação de vulnerabilidade se formam em capacitação do Einstein em SP.
    Saiba quais os cuidados e as regras no transporte de pets em viagens de avião.
    
    
    
    Portal de Notícias BBC Brasil
     
    Vídeo, O que números revelam sobre resultado da eleição, Duration 5,32.
    Crise dos mísseis de Cuba: como os EUA prepararam áreas para ataque soviético.
    
    
    


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
