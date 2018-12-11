# Team name: Evil Geniuses
# Authors:
# Vijayasaradhi Muthavarapu (Vijay)
# Nikhil Reddy Pathuri (Nikhil)
# Dilip Molugu (Dilip)
# Date: 10/03/2018

# 1. This program implements the concept of ngrams to know the dependencies for each word with their next word in a document. After it trains from the document the program is
# capable of creating sentences by its own.

# 2. Inorder to make this program work first we need to install the required libraries. Then in the command line arguments you need to pass a minimum of 3 arguments. 
#   -> The first argument should be the value of n to determine which ngram model to use.
#   -> The second argument should be the value of number of sentences to print using the ngram mmodel.
#   -> From the third argument you need to pass the text files that you want to make the model train on. You can also pass multiple text files as additional arguments to train
#      the model.
# An example to run this program:
# >python ngram.py 3 2 text1.txt text2.txt text3.txt
# Sample Output: 
# Ngrams = 3
# Number of Sentences = 2
# File no. 1= text1.txt
# File no. 2= text2.txt
# File no. 3= text3.txt
# n-1 table created
# n table created
# Laplace prob table created
# starting to print...
# Sentence 1: they did indeed advance , or from their pulpits as were true sons of religion and shadowy echoes of literature lived on later into the words and loyalty on
#             later into the clergy , in england .
# Sentence 2: if one more characteristic thought of time like faint and the world .

# 3. About our code and algorithm:
# Training data: We used the text files of some of the books found in Project Gutenberg.
# Program Logic: 
# Step 1: First our program reads all the text files and appends the files into a variable. We transform the data to lower case at the same time.
# Step 2: In order to capture each punctuation mark we added one space before and after the punctuation mark to the document and tokenized the document.
# Step 3: We used a different algorithm for computing unigram model and a common model for rest of the ngrams. For Unigram We calculate the frequency table of the tokens. 
#         Then we identify start and end tokens and separate them from our frequency table. After this we transform the frequencies to probabilities. Using a random number we 
#         determine which token to pick from the intervals of probability and print as output. This process itterates until an end token is found.
# Step 4: For rest of the ngrams we create tokens of n-1 length of words combination and n length of words combination.
# Step 5: Calculate frequencies for both list of tokens.
# Step 6: Identify Start and End tokens.
# Step 7: Now create a 2D-List with rows representing n-1 gram tokens and columns representing each unique token present in the document.
# Step 8: Calculate Laplace probabilities for each of the combinations in the list. Laplace probabilities helps in avoiding the dead lock cases where certain probabilities are zero.
#         About 80% of the combinations will have 0 probabilities so this calculations take a very long time. Without Laplace we directly ignore these cases and this drastically
#         increases the model performance.
# Step 9: Normalize the probabilities and calculate the intervals on a scale of 0-1.
# Step 10: We first start printing our sentences from a random start token and then we pick the next possible word using a random number. This process is iterated until an end 
#          token is found.  

# Key Feature: We have made use of Laplace probabilities to avoid any dead lock cases and reach the end tag. In this we give a slight probability for the tokens even if there 
#             is no such combination in the documents. As we are calculating for each and every combination of the tokens, there is a high performance toll on our program.

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

fdist = FreqDist(tokens)
#print(fdist)

end = ['.','!','?']
start = []

#different logic for uni gram only
if(ngrams==1):
    count =0
    #identifying start tokens that come after end tokens
    for word in tokens:
        if(word=="." or word=="!" or word=="?"):
            if(count== len(tokens)-1):
                break
            start.append(tokens[count+1])
        count+=1

    start = set(start)
    #print(start)

    #remove end tokens if any from start
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

    #fdist2

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
     #n gram model
     #compute n-1 tokens
    tokens_n1=[]

    for pos in range(len(tokens)):
        if(pos==len(tokens)-(ngrams-2)):
            break
        line = ""
        for pos2 in range(ngrams-1):
            if(pos2==0):
                line = str(tokens[pos+pos2])
            else:
                line = line + " " + str(tokens[pos+pos2])
        #print(string)
        tokens_n1.append(line)

    print("n-1 table created")

    # compute n-1 token frequency table
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

        print("n table created")

    #compute n token frequency table
    fdist_n = FreqDist(tokens_n)

    #create dataframe for for calculating next word probability
    d = {}
    df = pd.DataFrame(data=d, index=set(tokens_n1),columns=set(tokens))
    #converting data frame to 2d list for faster processing time
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
    
    print("Laplace prob table created")

    #calculate absolute probabilities
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
    print("starting to print...")
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
                            line = line + " " + cols
                            re_line = rows + " " + cols
                            # spotting last n-1 words
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
