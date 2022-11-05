from bs4 import BeautifulSoup

# Funções para processar ágina e filtrar conteudos.
url = 'https://g1.globo.com/'
# Crawler function in G1 page
# Extraindo noticias do portal G1
def g1_(hdata, htag='div', attr={'class': '_b', 'id':''}, debug=False):
    #global dnews
    dnews = []

    soup = BeautifulSoup(hdata, 'html.parser')
    cwn = soup.find_all(htag, class_=attr['class'])
    # Debug
    if debug:
        print('>> ',hdata[0:20])
        print('> ',cwn)
    #------------
    for l in cwn[0].children:
        for news in l:
            dnews.append({'titulo': news.a.text, 'url': news.a['href']})

    return dnews, cwn

# Generate json file with G1 news.
# Gerando arquivo json com lista de noticias do portal G1 da Globo.
def g1_gen_json(dnews):
    import json
    data = json.dumps(dnews, ensure_ascii = False, sort_keys = False, indent = 4)
    with open('out_g1.json','w') as file_:
        file_.write(data)
        file_.close()

# Generate html file with G1 news
# Gerando arquivo com as noticias de destaque do portal G1 da globo.
def g1_gen_html(dnews):
    import wtemplate
    news_page = wtemplate.newstemplate
    #for i in dnews:


    with open('out_g1.html', 'w') as file_:
        file_.write(news_page)
        file_.close()
