import json
from datetime import date

from scraping_tools import pull_fivethirtyeight
from scraping_tools import pull_foxnews
from scraping_tools import pull_apnews

from tools import save_dictionary


DATE = str(date.today())
DIRECTORY = 'data/'

tools = [
    pull_fivethirtyeight, 
    pull_foxnews, 
    pull_apnews,
]

doc_dic = {}

for tool in tools:

    titles, authors, contents, links = tool()

    # ToDo : troubleshoot why duplicates are always found
    added = 0
    for k, title in enumerate(titles):
        if doc_dic.get(title):
            pass

        else:
            added += 1
            doc_dic[title] = (authors[k], contents[k], links[k])


    print(f'Number of titles extracted : {len(titles)}')
    print(f'Number of titles added : {added}\n')


file_name = DATE+"_news.json"

save_dictionary(doc_dic, DIRECTORY+file_name)