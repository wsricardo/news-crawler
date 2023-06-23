# Documentação e Testes

## Import módulos


```python
import trackersWEB
import crawler
import trackers
import pandas as pd
```

## Instanciando o Crawler

Ao instanciar módulo obtêm-se acesso aos atributos e funções base para obter o html da página.
Através do parâmetro _tracker_ acesse as listas de funções disponiveis contidas no módulo _trackers_ responsável por 
processar o html em seu formato texto (string).


```python
c = crawler.Crawler()
```

Abaixo atributos e métodos contidos na classe _Crawler_ dentro do módulo _crawler_.


```python
print( dir(c) )
```

    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_text', 'args', 'attrs', 'cleandataframe', 'data', 'dataframe', 'get', 'kwargs', 'rs', 'save', 'text', 'toJSON', 'track', 'tracker', 'url']


### Exemplo - Obtendo Conteúdo e noticias para site BBC Brasil


```python
c.get('https://www.bbc.com/portuguese')
news = c.tracker.trackerBBC( c.text )
```

Atributo **data** refere-se a resposta retornada pelo servidor.


```python
print("response server", c.data )
```

    response server <Response [200]>


Aqui usa-se o pacote **Pandas** para criar-se a tabela com links de notícias para o portal da BBC Brasil. Nota-se que nem todos links referem-se a links das noticias sendo necessário uma limpeza nos dados para manter-se unicamente os artigos jornalísticos.


```python
dfnews = pd.DataFrame( news )
dfnews.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>href</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Celso Sabino: o que pode levar Lula a dar mini...</td>
      <td>https://www.bbc.com/portuguese/articles/c4n4q8...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Febre maculosa: quem deve responder pelas mort...</td>
      <td>https://www.bbc.com/portuguese/articles/c0xe9e...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Por que Beyoncé está sendo responsabilizada po...</td>
      <td>https://www.bbc.com/portuguese/articles/ckvzjp...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A falta de remédios nos EUA que deixa paciente...</td>
      <td>https://www.bbc.com/portuguese/articles/cjqzy4...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Discriminação de políticos: o que seria crime,...</td>
      <td>https://www.bbc.com/portuguese/articles/ckrm4e...</td>
    </tr>
  </tbody>
</table>
</div>




```python
import json
# List news from json format data
for i in json.loads( dfnews.head().to_json( orient='records' )):
    print( f"[{ i[ 'title' ] }] - [{ i[ 'href' ] }]" )
```

    Celso Sabino: o que pode levar Lula a dar ministério a ex-aliado de Bolsonaro - https://www.bbc.com/portuguese/articles/c4n4q8q2q29o
    Febre maculosa: quem deve responder pelas mortes no interior de SP? - https://www.bbc.com/portuguese/articles/c0xe9eq0x4qo
    Por que Beyoncé está sendo responsabilizada por inflação na Suécia - https://www.bbc.com/portuguese/articles/ckvzjp9p399o
    A falta de remédios nos EUA que deixa pacientes com câncer sem quimioterapia - https://www.bbc.com/portuguese/articles/cjqzy41k3q5o
    Discriminação de políticos: o que seria crime, segundo projeto aprovado pela Câmara - https://www.bbc.com/portuguese/articles/ckrm4ez9393o



```python

```
