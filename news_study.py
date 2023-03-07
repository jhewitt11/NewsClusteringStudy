import json
import numpy as np
import joblib
import umap as up

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits import mplot3d

from tools      import read_dictionary
from tools      import generate_knn_report

DICT_NAME               = '2023-02-22_news.json'
VECTOR_SCHEME           = 'BERT'
DIM_REDUCTION_SCHEME    = 'UMAP'
DIMENSIONALITY          = 2

DATE                    = DICT_NAME.split('_')[0]
ID                      = str(np.random.randint(low = 0, high = 1000))

TITLE                   = DATE+' '+ID+' '+DIM_REDUCTION_SCHEME+' reduced '+VECTOR_SCHEME+' embeddings'



doc_dic = read_dictionary('data/' + DICT_NAME)
assert(doc_dic != False)

headlines = list(doc_dic.keys())
corpus = [value[1] for value in doc_dic.values()]



if VECTOR_SCHEME == 'TFIDF' :

    # create TFIDF vectors
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    X = X.toarray()

elif VECTOR_SCHEME == 'BERT' :

    date = DICT_NAME.split('_')[0]
    EMBEDDING_NAME = date+'_embedding.z'

    X = joblib.load('data/embeddings/' + EMBEDDING_NAME)    

else :
    print('error: VECTOR_SCHEME not recognized.')



if DIM_REDUCTION_SCHEME == 'PCA':

    pca = PCA(n_components = DIMENSIONALITY)
    X_prime = pca.fit_transform(X)

elif DIM_REDUCTION_SCHEME == 'UMAP':
    
    reducer = up.UMAP(n_components = DIMENSIONALITY,
                        metric = 'cosine')

    X_prime = reducer.fit_transform(X)

else :
    print('error: DIM_REDUCTION_SCHEME not recognized.')


neighbs = NearestNeighbors(n_neighbors = 4)
neighbs.fit(X_prime)
distances, indices = neighbs.kneighbors(X_prime, return_distance = True)

np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})


generate_knn_report(headlines, distances, indices, TITLE)






x = X_prime[:,0]
y = X_prime[:,1]
#z = X_prime[:,2]

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
ax = plt.axes()
#ax = plt.axes(projection='3d')

for i in range(len(x)):
    ax.scatter(x[i], y[i],  color = source_colors[i], label = source_colors[i])
    ax.text(x[i], y[i], '%s' % i, color = 'k')
    
ax.set_title(DIM_REDUCTION_SCHEME+' reduced '+VECTOR_SCHEME+' embeddings')
plt.legend(handles=[red_patch, green_patch, blue_patch])
fig.savefig('results/'+TITLE+'.png')
