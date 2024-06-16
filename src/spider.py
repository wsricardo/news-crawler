"""
    Author: WSRicardo
    Blog: https://wsricardo.blogspot.com
    Site: www.dimensaoalfa.com.br
    Github: www.github.com/wsricardo

    Código para extrair links.
"""

from bs4 import BeautifulSoup
import requests


def createSpider( ):
    """
        Create and return requests Session.
    """
    
    return requests.Session()
    
def getContent( url ):
    """
    url - web page
    Return html content from url.
    
    """
    header = {"User-Agent": "Mozilla/5.0 Firefox/126.0"}
    spider = createSpider()
    
    return spider.get( url, headers = header ).text
    
    


def saveWebPageContentHTML( htmlcontent, namefile ):
    """
        Save file with HTML content from web page.
    """
    
    with open( namefile, "w", encoding="utf-8" ) as fl:
        fl.write( htmlcontent )

def saveLinksList( l, filename ):
    """
    Save file csv with link list.
    """
    index = 1
    with open( filename+".csv", "w", encoding="utf-8" ) as fl:
        fl.write( '"' + 'Index' + '"' + ';' + '"' + 'URL' + '"' + ';' + '"' + 'TEXT' + '"' + '\n' )
        
        for link in l:
            #if link['url']=='' or link['text'] == '':
            
            fl.write( '"' + str( index ) + '"'  + ' ; ' + '"' + link["url"] + '"' + ' ; ' + '"' + str( link["text"] ) + '"'  + "\n" )
            index = index + 1
    
    
def get_links( webcontent ):
    """
        get_links
        arguments
        webcoment - html text
        return list[ {'url':'', 'text':'' } ] 

        Return list links found in html content.
    """


    soup = BeautifulSoup(webcontent, 'html.parser' )

    linksall = soup.find_all( 'a' )
    links = [ ]

    for link in linksall:
        l = link.get( 'href' )
        if l:
            if  ( 'http' in l or 'https' in l ) and len( link.text ) > 3 :
                links.append( {
                    'url': l,
                    'text': link.text.strip( ) 

                    } )
    return links

if __name__== "__main__":
    html = ''

    with open( "main2.html", "r", encoding='utf-8' ) as fl:
        html = fl.read()

    #print( html )
    print( get_links( html ) )
