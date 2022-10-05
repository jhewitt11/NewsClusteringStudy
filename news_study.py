import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from tools      import read_dictionary, save_dictionary
from scraping   import pull_fivethirtyeight, pull_foxnews, pull_apnews

# file name for json.dump()
file_name = '100322_news.json'

doc_dic = read_dictionary(file_name)

if not(doc_dic) :

    print("{} not found, scraping sites and building dictionary".format(file_name))
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
            print("{} failed, exception found\n".format(tool))
            print(e)

    save_dictionary(doc_dic, file_name)

corpus = [value[1] for value in doc_dic.values()]

# create TFIDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names_out()

# need to transform X from a sparse matrix
X = X.toarray()

# PCA => 3 dims
pca = PCA(n_components = 3)
X_prime = pca.fit_transform(X)

# Format data to plot
X_prime = np.array(X_prime)

x = X_prime[:,0]
y = X_prime[:,1]
z = X_prime[:,2]

# Create color mapping by source
links = [value[2] for value in doc_dic.values()]
source_colors = []

for link in links:
    
    if link.find('foxnews') != -1:
        source_colors.append('r')
        
    elif link.find('apnews') != -1:
        source_colors.append('b')
    
    elif link.find('fivethirtyeight') != -1:
        source_colors.append('g')
        
    else:
        source_colors.append('k')

# Plot
fig = plt.figure(figsize = (8,8))
ax = plt.axes(projection='3d')

for i in range(len(x)):
    ax.scatter(x[i], y[i], z[i],  color = source_colors[i], depthshade = True)
    ax.text(x[i], y[i], z[i], '%s' % i, color = 'k')
    
ax.set_title('PCA reduced TFIDF embeddings')
plt.show()
