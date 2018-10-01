import sys
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from random import random
import numpy as np
import pandas as pd
import re

print("This program generates random sentences based on an Ngram model.")
for x in range(len(sys.argv[1:])):
    if(x==0):
        print("Ngrams= "+sys.argv[1])
        ngrams = int(sys.argv[1])
    elif(x==1):
        print("Number of sentences= "+sys.argv[2])
        sentences = sys.argv[2]
    else:
        print("File no."+ str(x-1)+"= "+ sys.argv[x+1])

#reading all the files and extracting tokens

txt_data=""
for y in range(2,len(sys.argv[1:])):
    with open(sys.argv[y+1],encoding="latin-1") as f_open:
        txt_data= txt_data + (f_open.read().lower())

text= re.sub(r'(-|\'|_|\.|\/|\*)', r' \1 ',txt_data)

tokens=[]
tokens = (word_tokenize(text))

#print(len(tokens))
#print(len(set(tokens)))

fdist = FreqDist(tokens)
#print(fdist)

end = ['.','!','?']
start = []

if(ngrams==1):
    count =0
    for word in tokens:
        if(word=="." or word=="!" or word=="?"):
            if(count== len(tokens)-1):
                break
            start.append(tokens[count+1])
        count+=1

    start = set(start)
    #print(start)

    #remove end tokens from start
    t_start=[]
    for word in start:
        if word in end:
            continue
        t_start.append(word)
    start = t_start

    #add start to freqdist
    count = 0
    for key,value in fdist.items():
        for word in start:
            if(key==word):
                count= count+ value
    #print(count)
    fdist["<start>"]= count

    #add end to freqdist
    count = 0
    for key,value in fdist.items():
        for word in end:
            if(key==word):
                count= count+ value
    #print(count)
    fdist["<end>"]= count

    #remove start and end tokens
    fdist2 = {}
    for key,value in fdist.items():
        if key in end: continue
        elif key in start: continue
        fdist2[key]= value

    fdist2

    #create probability distribution

    probdist={}
    for key,value in fdist2.items():
        probdist[key]=value/len(tokens)

    #probdist  

    #create interval prob dist

    lineprobdist={}
    sum=0
    for key,value in probdist.items():
        sum=sum+value
        lineprobdist[key]=sum

    #1gram model
    for x in range(int(sentences)):
        start_c=1
        end_c=0
        line="Sentence "+str(x+1)+" :"
        while(end_c==0):
            rand = random()
            if(start_c==1):
                line= line+" "+np.random.choice(list(start))
                start_c=0
            for key,value in lineprobdist.items():
                if(rand<value):
                    if(key=="<start>"):
                        key = np.random.choice(list(start))
                    elif(key=="<end>"):
                        key = np.random.choice(list(end))
                        end_c=1
                    line=line+" "+key
                    break
            
        print(line)    

else:
     #compute n-1 table
    tokens_n1=[]

    for pos in range(len(tokens)):
        if(pos==len(tokens)-(ngrams-2)):
            break
        line = ""
        #str(tokens[pos])+" "+str(tokens[pos+1])
        for pos2 in range(ngrams-1):
            if(pos2==0):
                line = str(tokens[pos+pos2])
            else:
                line = line + " " + str(tokens[pos+pos2])
        #print(string)
        tokens_n1.append(line)

    #print(tokens_n1)

    # compute n-1 table frequencies
    fdist_n1 = FreqDist(tokens_n1)
    
    #create n gram tokens
    if(ngrams>1):
        tokens_n=[]

        for pos in range(len(tokens)):
            if(pos==len(tokens)-(ngrams-1)):
                break
            line = ""
            for pos2 in range(ngrams):
                if(pos2==0):
                    line = str(tokens[pos+pos2])
                else:
                    line = line + " " + str(tokens[pos+pos2])
            tokens_n.append(line)

        #print(tokens_n)

    #compute n table frequency
    fdist_n = FreqDist(tokens_n)
    #create n freq table
    d = {}
    df = pd.DataFrame(data=d, index=set(tokens_n1),columns=set(tokens))
    array = df.values.tolist()

    #create n gram data frame indicating probabilities with laplace smoothing
    prob = 0
    row_sum=[]
    len_tokens = len(set(tokens))
    row_n=0
    for rows in df.index.values:
        sum=0
        col_n=0
        for cols in df.columns.values:
            line = str(rows)+" "+str(cols)
            value = fdist_n[line]
            prob=(value+1)/(fdist_n1[rows]+len_tokens)
            array[row_n][col_n]=prob
            sum=sum+prob
            col_n +=1
        row_n += 1
        row_sum.append(sum)
    
    #print(df.iloc[1,1])
    #absolute probabilities
    for row in range(len(df.index.values)):
        prob=0
        for col in range(len(df.columns.values)):
            array[row][col]=array[row][col]/row_sum[row]
            prob = prob+array[row][col]
            array[row][col] = prob

    #convert list to df
    df = pd.DataFrame(data=array, index=set(tokens_n1),columns=set(tokens))

    #create start and end
    end = ['.','!','?']
    start = []

    for pos in range(len(tokens)):
        if tokens[pos] in end:
            if(pos>=len(tokens)-(ngrams-1)):
                break
            line = ""
            for pos2 in range(ngrams-1):
                if(pos2==0):
                    line = str(tokens[pos+pos2+1])
                else:
                    line = line + " " + str(tokens[pos+pos2+1])
            start.append(line)

    start = set(start)

    #print sentences

    for x in range(int(sentences)):
        line =np.random.choice(list(start))
        line2 =line
        end_c=0
        while(end_c==0):
            row_n=0
            for rows in df.index.values:
                if(rows==line2):
                    col_n=0
                    rand = random()
                    for cols in df.columns.values:
                        if(rand<array[row_n][col_n]):
                            prev_line = line
                            prev_line2 = line2
                            line = line + " " + str(cols)
                            re_line = rows + " " + cols
                            res = re.match(r'^\S+(.*)',re_line)
                            line2 = res[1].strip()                           
                            break
                        col_n +=1
                    if line2 not in tokens_n1:
                        line = prev_line
                        line2= prev_line2 
                        break
                    elif re.search(r'(\.|\?|!)',line):
                        end_c=1
                        break
                row_n+=1
                
        print("Sentence "+str(x+1)+": "+line)
