import joblib
import json

from sentence_transformers import SentenceTransformer

from tools import read_dictionary

DICT_NAME   = '2023-03-06_news.json'
DIRECTORY 	= 'data/embeddings/'

date = DICT_NAME.split('_')[0]
EMBEDDING_NAME = date+'_embedding.z'


doc_dic = read_dictionary('data/'+DICT_NAME)
assert(doc_dic != False)

corpus = [value[1] for value in doc_dic.values()]

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(corpus, show_progress_bar = True)

joblib.dump(embeddings, DIRECTORY+EMBEDDING_NAME, compress = 3)