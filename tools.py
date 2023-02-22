import sys
import io
import re
import numpy as np
import json


'''
SAVING DATA
'''
#  Save dictionary as JSON file
#
#  dictionary - python dictionary
#  FILE - file name "xyz.json"
#
def save_dictionary(dictionary,  FILE):
    with open(FILE,'w') as outfile:
        json.dump(
            dictionary, 
            outfile,
            ensure_ascii = True,
            indent = 4
            )

    return 


#  Save embeddings as np.array to file
#
#  FILE - file name "xyz.np"
#  embeddings - n dimension embeddings
#
def save_embeddings(FILE, embeddings):

    embeddings = np.array(embeddings)
    np.save(FILE, embeddings)
    
    return FILE


'''
DATA INTAKE
'''
#  Read and clean text from .txt file
#
#  TEXT_A - file name
#
def read_clean(TEXT_A):

    file_a = open(TEXT_A, "r")

    try:
        text_a = file_a.read()
    except:
        file_a = open(TEXT_A, "r", encoding="utf8")
        text_a = file_a.read()
        
    file_a.close()
    text_clean_lines = text_a.replace("\n"," ")
    
    text_clean = re.sub(r'\.\d', '. ', text_clean_lines)
    

    return text_clean_lines 

#  Read in dictionary from JSON file
#
#  FILE - file name
#
def read_dictionary(FILE):
    
    try :
        with open(FILE) as infile:
            doc_dic = json.load(infile)
    except:
        doc_dic = False
            
    return doc_dic

'''
OTHER TOOLS
'''
def generate_report(model_name, TEXT_A, TEXT_B, sent_a, sent_b, vals_a, vals_b, indices_a, indices_b, K_RESULTS, THRESHOLD):   
    
    header = 'model used : ' + model_name + '\n'
    output = header + 'TEXT_A is ' + TEXT_A + '\nTEXT_B is ' + TEXT_B + '\n\n'

    for i in range(len(sent_a)):
        if vals_a[i][0] > THRESHOLD :
            a="\n\nTEXT_A sentence #{} is : \n{}".format(i, sent_a[i])
            b=""
            for k in range(K_RESULTS):
                if vals_a[i][k] > THRESHOLD :
                    b+="\n\n\tScore : {}\tTEXT_B sentence #{} is :\n\t{}".format(vals_a[i][k], indices_a[i][k], sent_b[indices_a[i][k]])
            output+= a+b

    ## add divider in report
    output += "\n\n\n------------------------\n\n"

    ## add new loop
    output2 = ""
    for i in range(len(sent_b)):
        if vals_b[i][0] > THRESHOLD :
            a="\n\nTEXT_B sentence #{} is : \n{}".format(i, sent_b[i])
            b=""
            for k in range(K_RESULTS):
                if vals_b[i][k] > THRESHOLD :
                    b+="\n\n\tScore : {}\tTEXT_A sentence #{} is :\n\t{}".format(vals_b[i][k], indices_b[i][k], sent_a[indices_b[i][k]])
            output2+= a+b

    output += output2

    file_name = "Results "+" "+ model_name + " " + TEXT_A + " AND " + TEXT_B + '.txt'

    return output, file_name

def pull_doc_num(collection):

    #manage faults
    num = len(collection.partitions)

    return num
