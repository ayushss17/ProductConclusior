import string
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as mp
import asyncio
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def getReviews(rev_data):

    # review_data= ""

    # if __name__ == "__main__":
    #     review_data=asyncio.run(sen())



#converting into lowercase
    lower_dt=rev_data.lower()

    print(lower_dt)

#data cleaning - removing punctuations
    cleaned_txt=lower_dt.translate(str.maketrans('','',string.punctuation))



# #tokenization
    token_words=word_tokenize(cleaned_txt,"english")
    final_dt=[]
#removing stop words
    for word in token_words:
        if word not in stopwords.words("english"):
            final_dt.append(word)
    
    emotion_list=set()
    with open("D:\Projects\ProductConclusior\Conclusior\static\emotions.txt","r") as file:
        for line in file:
            clear_line=line.replace("'","").replace(",","").replace("\n","").strip()
        #separating words and emotions
            word,emotion=clear_line.split(':')
        # print(word,"=",emotion)
            if word in final_dt:
                emotion_list.add(emotion)

    print("\nEmotion list: ",emotion_list)
    res=''.join(emotion_list)
    score=SentimentIntensityAnalyzer().polarity_scores(cleaned_txt)
    neg=score['neg']
    pos=score['pos']
    if(neg>pos):
        return (res,neg)
    elif pos>neg:
        return (res,pos)
    else:
        return 3





