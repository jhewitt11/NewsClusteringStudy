from bs4 import BeautifulSoup
import urllib3
import requests
import re

from datetime import date

def pull_fivethirtyeight():
    page_url = 'https://fivethirtyeight.com/politics/'

    # Open connection and pull html contents from homepage
    PM = urllib3.PoolManager()
    r = PM.request('GET', page_url)

    print('fivethirtyeight connection made..') 

    soup = BeautifulSoup(r.data.decode('utf-8'), 'lxml')

    containers = soup.findAll("div", id = re.compile('post-\d*'))

    links = []

    # Extract links to individual articles
    for container in containers:
        if container.get('data-href'):
            link = container['data-href']
            if link.find('/videos/') == -1:
                links.append(link)

    titles = []
    by_lines = []
    contents = []
    
    # Extract info from each article
    for link in links :
        PM2 = urllib3.PoolManager()
        r2 = PM2.request('GET', link)
        soup2 = BeautifulSoup(r2.data.decode('utf-8'), 'lxml')

        title = soup2.find('div', {'class':'single-header'}).h1.text
        by_line = soup2.find('div', {'class':'single-header-metadata-wrap'}).p.text

        post = soup2.findAll('p', {'data-paragraph':'main'})
        
        text  = '' 
        for p in post :
            text+= ' ' + p.text
        
        
        titles.append(title)
        by_lines.append(by_line)
        contents.append(text)
        
    return titles, by_lines, contents, links

def pull_foxnews():
    page_url = 'https://www.foxnews.com/politics'

    # Open connection and pull html contents from homepage
    
    PM = urllib3.PoolManager()
    r = PM.request('GET', page_url)

    print('FoxNews connection made..')         
            
    soup = BeautifulSoup(r.data.decode('utf-8'), 'lxml')
    containers = soup.findAll("article", {'class':'article'})

    links = []

    # Extract links to individual articles
    for container in containers:
        if container.div.a.get('href'):         
            link = container.div.a['href']
            if link.find('/video') == -1:
                links.append('https://foxnews.com' + link)

    titles = []
    by_lines = []
    contents = []
        
    # Extract info from each article
    for link in links :
        PM2 = urllib3.PoolManager()
        r2 = PM2.request('GET', link)
        soup2 = BeautifulSoup(r2.data.decode('utf-8'), 'lxml')

        title = soup2.find('h1').text
        by_line = soup2.find('div', {'class':'author-byline'}).text
        
        body = soup2.find('div', {'class':'article-body'})
                
        text = ''
        for tag in body :
            if tag.name == 'p':
                text += ' ' + tag.get_text(strip = True)
        
        titles.append(title)
        by_lines.append(by_line)
        contents.append(text)
       
    return titles, by_lines, contents, links

#titles, by_lines, content, links = pull_foxnews()

def pull_apnews():
    page_url = 'https://apnews.com/hub/politics'

    # Open connection and pull html contents from homepage
    
    PM = urllib3.PoolManager()
    r = PM.request('GET', page_url)
            
    print('AP connection made..')        
            
    soup = BeautifulSoup(r.data.decode('utf-8'), 'lxml')
    containers = soup.findAll("a", {'data-key': 'story-link'})

    # Extract links to individual articless
    links = []
    
    for container in containers:
        if container.get('href'):         
            link = container['href']
            links.append('https://apnews.com' + link)
    
    # Extract info from each article
    titles = []
    by_lines = []
    contents = []

    for link in links :
        PM2 = urllib3.PoolManager()
        r2 = PM2.request('GET', link)
        soup2 = BeautifulSoup(r2.data.decode('utf-8'), 'lxml')
        
        title = soup2.find('h1').text
        by_line = soup2.find('span', {'class': re.compile(r'^Component-signature')})
        
        body = soup2.find('div', {'class':'Article', 'data-key' : 'article'})          
    
        try :
            text = ''
            for tag in body :

                if tag.name == 'p':
                    piece = tag.get_text(strip = True)
                    text += ' ' + piece
                    
            titles.append(title)
            contents.append(text)   
            by_lines.append(by_line.text)

        except Exception as e: 
            print(f'\nByline : {by_line}\nFrom : {title}\nError : {e}')

    return titles, by_lines, contents, links
    
#titles, by_lines, content, links = pull_apnews()

def pull_BBC():
    page_url = 'https://bbc.com/news'
    main_url = 'https://bbc.com'

    # Open connection and pull html contents from homepage
    
    PM = urllib3.PoolManager()
    r = PM.request('GET', page_url)
            
    print('BBC connection made..')

    soup = BeautifulSoup(r.data.decode('utf-8'), 'lxml')
    containers = soup.findAll('a', {'class' : 'gs-c-promo-heading nw-o-link gs-o-bullet__text gs-o-faux-block-link__overlay-link gel-pica-bold gs-u-pl-@xs'})

    links = []

    for container in containers:
        if container.get('href'):         
            link = container['href']
            links.append(main_url + link)

    titles = []
    by_lines = []
    contents = []

    for link in links :
        PM2 = urllib3.PoolManager()
        r2 = PM2.request('GET', link)
        soup2 = BeautifulSoup(r2.data.decode('utf-8'), 'lxml')

        title = soup2.find('h1').text

        # check for null value
        by_line_tag = soup2.find('div', {'class' : re.compile('TextContributorName')})
        if by_line_tag == None:
            by_line = 'None'
        else:
            by_line = by_line_tag.text


        body = soup2.findAll('div', {'data-component' : 'text-block'})

        text = ''
        for tag in body :
            text += ' ' + tag.get_text(strip = True)

        titles.append(title)
        by_lines.append(by_line)
        contents.append(text)

    return titles, by_lines, contents, links




def pull_globaltimes():
    page_url = 'https://www.globaltimes.cn/world/index.html'
    main_url = 'https://www.globaltimes.cn'

    # Open connection and pull html contents from homepage
    
    PM = urllib3.PoolManager()
    r = PM.request('GET', page_url)
            
    print('GlobalTimes connection made..')

    soup = BeautifulSoup(r.data.decode('utf-8'), 'lxml')
    containers = soup.findAll('a', {'target' : '_blank'})

    links = []

    for container in containers:
        if container.get('href'):         
            link = container['href']
            links.append(link)
            print(link)

    titles = []
    by_lines = []
    contents = []

    for link in links :
        PM2 = urllib3.PoolManager()
        r2 = PM2.request('GET', link)
        soup2 = BeautifulSoup(r2.data.decode('utf-8'), 'lxml')

        title = soup2.find('div', {'class' : 'article_title'}).text

        # check for null value
        

        by_line_tag = soup2.find('span', {'class' : 'byline'})
        if by_line_tag == None:
            by_line = 'None'
        else:
            by_line = by_line_tag.text
        

        body = soup2.find('div', {'class' : 'article_right'})

        print(body.text)

        text = ''
        for tag in body :
            text += ' ' + tag.get_text(strip = True)

        titles.append(title)
        by_lines.append(by_line)
        contents.append(text)

    return titles, by_lines, contents, links