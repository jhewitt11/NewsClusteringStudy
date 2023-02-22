import json
from datetime import date

from scraping_tools import pull_fivethirtyeight, pull_foxnews, pull_apnews
from tools import save_dictionary



DATE = str(date.today())


tools = [pull_fivethirtyeight, pull_foxnews, pull_apnews]
doc_dic = {}

for tool in tools:
    try:
        titles, authors, contents, links = tool()
        
        for k in range(len(titles)):
            if doc_dic.get(titles[k]):
                print(titles[k])
                print('error : duplicate title found\n')
            else:
                doc_dic[titles[k]] = (authors[k], contents[k], links[k])
    
    except Exception as e:
        print("{} failed, exception found :\n\t{}".format(tool, e))

file_name = DATE+"_news.json"

print(file_name)

save_dictionary(doc_dic, file_name)