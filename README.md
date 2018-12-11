# Ngrams

 Team name: Evil Geniuses
 Authors:
 Vijayasaradhi Muthavarapu (Vijay)
 Nikhil Reddy Pathuri (Nikhil)
 Dilip Molugu (Dilip)
 Date: 10/03/2018

 1. This program implements the concept of ngrams to know the dependencies for each word with their next word in a document. After it trains from the document the program is# capable of creating sentences by its own.

 2. Inorder to make this program work first we need to install the required libraries. Then in the command line arguments you need to pass a minimum of 3 arguments. 
   -> The first argument should be the value of n to determine which ngram model to use.
   -> The second argument should be the value of number of sentences to print using the ngram mmodel.
   -> From the third argument you need to pass the text files that you want to make the model train on. You can also pass multiple text files as additional arguments to train the model.
 An example to run this program:
 >python ngram.py 3 2 text1.txt text2.txt text3.txt
 
 Sample Output: 
 Ngrams = 3
 Number of Sentences = 2
 File no. 1= text1.txt
 File no. 2= text2.txt
 File no. 3= text3.txt
 n-1 table created
 n table created
 Laplace prob table created
 starting to print...
 Sentence 1: they did indeed advance , or from their pulpits as were true sons of religion and shadowy echoes of literature lived on later into the words and loyalty on later into the clergy , in england .
 Sentence 2: if one more characteristic thought of time like faint and the world .

 3. About our code and algorithm:
 Training data: We used the text files of some of the books found in Project Gutenberg.
 Program Logic: 
 Step 1: First our program reads all the text files and appends the files into a variable. We transform the data to lower case at the same time.
 Step 2: In order to capture each punctuation mark we added one space before and after the punctuation mark to the document and tokenized the document.
 Step 3: We used a different algorithm for computing unigram model and a common model for rest of the ngrams. For Unigram We calculate the frequency table of the tokens. Then we identify start and end tokens and separate them from our frequency table. After this we transform the frequencies to probabilities. Using a random number we determine which token to pick from the intervals of probability and print as output. This process itterates until an end token is found.
 Step 4: For rest of the ngrams we create tokens of n-1 length of words combination and n length of words combination.
 Step 5: Calculate frequencies for both list of tokens.
 Step 6: Identify Start and End tokens.
 Step 7: Now create a 2D-List with rows representing n-1 gram tokens and columns representing each unique token present in the document.
 Step 8: Calculate Laplace probabilities for each of the combinations in the list. Laplace probabilities helps in avoiding the dead lock cases where certain probabilities are zero. About 80% of the combinations will have 0 probabilities so this calculations take a very long time. Without Laplace we directly ignore these cases and this drastically increases the model performance.
 Step 9: Normalize the probabilities and calculate the intervals on a scale of 0-1.
 Step 10: We first start printing our sentences from a random start token and then we pick the next possible word using a random number. This process is iterated until an end token is found.  

 Key Feature: We have made use of Laplace probabilities to avoid any dead lock cases and reach the end tag. In this we give a slight probability for the tokens even if there is no such combination in the documents. As we are calculating for each and every combination of the tokens, there is a high performance toll on our program.
