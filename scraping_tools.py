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

    links = []

    # Extract links to individual articles
    for container in containers:
        if container.get('href'):         
            link = container['href']
            links.append('https://apnews.com' + link)



    titles = []
    by_lines = []
    contents = []

        
    # Extract info from each article
    for link in links :
        PM2 = urllib3.PoolManager()
        r2 = PM2.request('GET', link)
        soup2 = BeautifulSoup(r2.data.decode('utf-8'), 'lxml')
        

        title = soup2.find('h1').text
        by_line = soup2.find('div', {'class': re.compile(r'^Component-signature')})
        
        body = soup2.find('div', {'class':'Article', 'data-key' : 'article'})          
    
    
        try :
            text = ''
            for tag in body :
                if tag.name == 'p':
                    text += ' ' + tag.get_text(strip = True)
                    
            titles.append(title)
            by_lines.append(by_line.text)
            contents.append(text)

        except Exception as e: 
            print('Failed to pull {}\n\t{}'.format(link, e))


    return titles, by_lines, contents, links
    
#titles, by_lines, content, links = pull_apnews()


'''
page_url = 'https://apnews.com/article/brittney-griner-paul-whelan-biden-meeting-8a9049fcedf67bdda9d0bac1b83d53c3'

# Open connection and pull html contents from homepage
    

r = requests.get(page_url).content
        
print('connection made..')        
        
soup = BeautifulSoup(r, 'html.parser')


Main = soup.find('main', {'class' : 'Main'})

Body = Main.find('div', 'Body')

Containers = Body.findAll('div', {'class' : re.compile(r'^Component-signature')})
'''