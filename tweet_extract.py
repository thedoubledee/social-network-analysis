import pandas as pd
from textblob import TextBlob

url='https://raw.githubusercontent.com/itsDevhere/DataRepo/master/'
def downloadcsv(filename):
    tweetfile=pd.read_csv(url+filename+'_cleaned.csv')
    tweetfile.to_csv(filename+'_cleaned.csv',index=False,encoding='utf-8')
def readfromcsv(filename):
    tweetfile=pd.read_csv(filename+'_cleaned.csv')
    tweetText = []
    username = []
    positivetweets=[]
    hash_count=''
    for row in tweetfile.itertuples():
        # Append to temp so that we can store in csv later. I use encode UTF-8
        tweetText.append(row[1])
        username.append(row[2])
        hash_count+=row[3].strip('[]')    
    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    n=len(tweetText)
    for i in range(n) :
        analysis = TextBlob(str(tweetText[i]))
        polarity += analysis.sentiment.polarity
        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
            positivetweets.append(username[i])
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
            positivetweets.append(username[i])
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
            positivetweets.append(username[i])
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
            negative += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1
    
    # finding average of how people are reacting
    positive = percentage(positive, n)
    wpositive = percentage(wpositive, n)
    spositive = percentage(spositive, n)
    negative = percentage(negative, n)
    wnegative = percentage(wnegative, n)
    snegative = percentage(snegative, n)
    neutral = percentage(neutral, n)
    polarity = polarity / len(tweetText)

    print("\nAnalyzing " +str( n) + " tweets on " + filename)
    print("General Report: ")

    if (polarity == 0):
        print("Neutral")
    elif (polarity > 0 and polarity <= 0.3):
        print("Weakly Positive")
    elif (polarity > 0.3 and polarity <= 0.6):
        print("Positive")
    elif (polarity > 0.6 and polarity <= 1):
        print("Strongly Positive")
    elif (polarity > -0.3 and polarity <= 0):
        print("Weakly Negative")
    elif (polarity > -0.6 and polarity <= -0.3):
        print("Negative")
    elif (polarity > -1 and polarity <= -0.6):
        print("Strongly Negative")

    print("\nDetailed Report: \n")
    print(str(positive) + "% people thought it was positive")
    print(str(wpositive) + "% people thought it was weakly positive")
    print(str(spositive) + "% people thought it was strongly positive")
    print(str(negative) + "% people thought it was negative")
    print(str(wnegative) + "% people thought it was weakly negative")
    print(str(snegative) + "% people thought it was strongly negative")
    print(str(neutral) + "% people thought it was neutral")
    temp=[positive, wpositive, spositive, negative, wnegative, snegative, neutral, n,hash_count,positivetweets]
    return temp

def percentage(part, whole):
#--Percentage conversion upto 2 decimal places--#    
    temp = 100 * float(part) / float(whole)
    return round(temp,2)
    #return format(temp, '.2f')
