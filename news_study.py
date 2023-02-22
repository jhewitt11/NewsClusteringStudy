import json
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits import mplot3d


from tools      import read_dictionary, save_dictionary
from scraping   import pull_fivethirtyeight, pull_foxnews, pull_apnews

FILE_NAME   = '100_news.json'
SCHEME      = 'tfidf'


doc_dic = read_dictionary(FILE_NAME)
assert(doc_dic != False)


headlines = list(doc_dic.keys())
corpus = [value[1] for value in doc_dic.values()]

if SCHEME == 'tfidf' :

    # create TFIDF vectors
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)


elif SCHEME == 'bert' :

    continue

else :
    print('error: encoding scheme not recognized.')



# need to transform X from a sparse matrix
X = X.toarray()

# PCA => 3 dims
pca = PCA(n_components = 3)
X_prime = pca.fit_transform(X)

# Format data to plot
X_prime = np.array(X_prime)


neighbs = NearestNeighbors(n_neighbors = 4)
neighbs.fit(X_prime)
distances, indices = neighbs.radius_neighbors(X_prime, radius = 0.1, return_distance = True, sort_results = True)

np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})


#for k, index in enumerate(indices):
#    print(f'#{k}\t{indices[k]}\n   \t{distances[k]}\n')
        






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

red_patch = mpatches.Patch(color='red', label='foxnews')
blue_patch = mpatches.Patch(color='blue', label='apnews')
green_patch = mpatches.Patch(color='green', label='fivethirtyeight')


# Plot
fig = plt.figure(figsize = (8,8))
ax = plt.axes(projection='3d')

for i in range(len(x)):
    ax.scatter(x[i], y[i], z[i],  color = source_colors[i], label = source_colors[i], depthshade = True)
    ax.text(x[i], y[i], z[i], '%s' % i, color = 'k')
    
ax.set_title('PCA reduced TFIDF embeddings')
plt.legend(handles=[red_patch, green_patch, blue_patch])
plt.show()
