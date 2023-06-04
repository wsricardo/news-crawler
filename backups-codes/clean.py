import pandas as pd
import json
import glob


def clean(df, datajson):


    """
    Remove fields by title in list of names specifieds.
    """
    
    # Remove lines specified to link of Twitter
    v = [ 'Política',
        'Pop',
        'Economia',
        'Internacional',
        'Viagem & Gastronomia',
        'Nacional',
        'Saúde',
        'Esportes',
        'CNN Plural',
        'Ciência e Tecnologia',
        'Mercado',
        'Facebook',
        'Twitter',
        'Youtube',
        'YouTube',
        'Instagram' 
    ]
    arqjson = ''
    import time
    for k in datajson:
        with open(f'{k}', 'r') as fl:
            arqjson = fl.read() 

        #df = pd.read_json( k  )
        df = pd.DataFrame( json.loads( arqjson  ))
        #print('> df', df )
        #time.sleep(4)
        for i in v:
            df = df.drop( index=df.index[ df['title'] == i ] )
        df.drop_duplicates( ignore_index=True )

        #print('> ', k)
        
        yield  json.loads( df.to_json(orient='records' ) )
    

    #return df,datajson


    #for j in df:
    #    for i in v:
    #        j = j.drop( index=j.index[ j['title'] == i ] )
    #    j = j.drop_duplicates( ignore_index = True )
    #return df.to_json( orient='records' )

if __name__== '__main__':
    datajson = glob.glob('news-crawler/datanews/*.json')

    df = [ pd.read_json( files ) for files in datajson ]
    #print(df[0])  
    df = clean(df, datajson)
    #print("final df", df)
    for i,j in zip( df, datajson ):
        j = j.split('/')[2]
        print(j)
        #print('i ', i)   
        with open(f'datacleaned/{j}', 'w') as fl:
            fl.write(   json.dumps(i, ensure_ascii=False, indent=4 )   )
        #i.to_json( f'datacleaned/{j}' )

    #d = ''
    #for i in datajson:
    #    with open(f'datacleaned/{i}', 'w' ) as fl:
    #        d = json.loads( clean() )

