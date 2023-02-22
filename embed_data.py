import joblib
import json

from sentence_transformers import SentenceTransformer

from tools import read_dictionary

DICT_NAME   = '2023-02-22_news.json'

doc_dic = read_dictionary(DICT_NAME)
assert(doc_dic != False)

corpus = [value[1] for value in doc_dic.values()]

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(corpus, show_progress_bar = True)

date = DICT_NAME.split('_')[0]
EMBEDDING_NAME = date+'_embedding.z'
joblib.dump(embeddings, EMBEDDING_NAME, compress = 3)