import tweepy,csv,re,datetime,emoji
from textblob import TextBlob
from collections import Counter

def DownloadData():
#--Authenticate ,download , filter,analyse tweet data --#    
    # authenticating
    consumerKey = '0q6yabp5VLtyKVpN39kLS86Lz'
    consumerSecret = '8zeZjTzytBhyxu3YfBPgInXhBFWG9j9fyIOtQMNDBdG9EC4eoV'
    accessToken = '1068212262945472512-tJN49MDY6TJCyMy3t4I34cIOzYt6pU'
    accessTokenSecret = 'a3Kf2rOyCTecWfwGUwfgOLj2WE8NSNgdBSFSV24lTZuBY'
    try:
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
    except: 
        print("Error: Authentication Failed")
    # input for term to be searched and how many tweets to search
    searchitem= input("Please select the type of search:\n1.Keyword/Tag\n2.Tweeted to a person\n3.Tweets from a person.\nEnter:")
    searchTerm = input("Enter Keyword/Tag to search about: ")
    NoOfTerms = int(input("Enter how many tweets to search: "))
        
    if(searchitem == '1'):
        tweets = tweepy.Cursor(api.search, searchTerm + " -filter:retweets", lang="en", tweet_mode="extended").items(NoOfTerms)
    elif(searchitem == '2'):
        tweets = tweepy.Cursor(api.search, "To:" + searchTerm + " -filter:retweets", lang="en", tweet_mode="extended").items(NoOfTerms)
    elif(searchitem == '3'):
        tweets = tweepy.Cursor(api.search, "From:" + searchTerm + " -filter:retweets", lang="en", tweet_mode="extended").items(NoOfTerms)
    
    # Open/create a file to append data to
    csvFile = open('result' + str(datetime.datetime.now().strftime("%Y%m%d%H%M")) + '.csv', 'a', newline='', encoding="utf-8")
    # Use csv writer
    csvWriter = csv.writer(csvFile)
    tweetText = []
    dates = []
    likes = []
    locations=[]
    hash_tags = []
    retweet = []
    tweetid = []
    username = []
    polarityl = []
    day = []
    temp = ""
    temp1 = []    
    for tweet in tweets:
        # Append to temp so that we can store in csv later. I use encode UTF-8
        tweetid.append(tweet.id)
        likes.append(tweet.favorite_count)
        username.append(tweet.user.screen_name)
        locations.append(tweet.user.location)
        retweet.append(tweet.retweet_count)
        dates.append(tweet.created_at.date().strftime("%d-%m-%y"))
        day.append(tweet.created_at.date().strftime("%a"))
        temp = free_text(remUrl(cleanTweet((tweet.full_text))))
        tweetText.append(temp)
        hash_tags.append(getTags(temp))
        polarityl.append(TextBlob(temp).sentiment.polarity)

    for i in range(len(hash_tags)):
        for j in range(len(hash_tags[i])):
            hash_tags[i][j] = hash_tags[i][j].lower()
            
    for i in range(len(hash_tags)):
        temp1 += hash_tags[i]
    hash_count = Counter(temp1)
    #for key, value in {k: v for k, v in sorted(hash_count.items(), key=lambda x: x[1], reverse=True)}.items():
        # temp = [key,value]
        # top_hash.append(temp)
    csvWriter.writerow(['tweet', 'username', 'location', 'hash-tags', 'Date', 'Day', 'tweet_id', 'likes', 'retweets', 'polarity'])
    for i in range(len(tweetText)):
        csvWriter.writerow([tweetText[i], username[i], locations[i], hash_tags[i], dates[i], day[i], tweetid[i], likes[i], retweet[i], polarityl[i]])
    csvFile.close()
    
    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    n = len(tweetText)
        
    for text in range(len(tweetText)):

        analysis = TextBlob(tweetText[text])
        polarity += analysis.sentiment.polarity
            
        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
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

    print("\nAnalyzing " + str(n) + " tweets on " + searchTerm)
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

    print()
    print("Detailed Report: ")
    print(str(positive) + "% people thought it was positive")
    print(str(wpositive) + "% people thought it was weakly positive")
    print(str(spositive) + "% people thought it was strongly positive")
    print(str(negative) + "% people thought it was negative")
    print(str(wnegative) + "% people thought it was weakly negative")
    print(str(snegative) + "% people thought it was strongly negative")
    print(str(neutral) + "% people thought it was neutral")
    temp=[positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, n,dates,day,hash_count,hash_tags,temp1]
    return temp

def percentage(part, whole):
#--Percentage conversion upto 2 decimal places--#    
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

def cleanTweet(tweet):
#--Filter tweet based on reg ex.--#    
    # Remove Links, Special Characters etc from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

def getTags(Twit):
#--Get tweets based on reg. ex.--#
    return re.findall(r"#(\w+)", Twit)
                       
def free_text(text):
#--Extract text from graphical content--#     
    allchars = [str for str in text]  # @ReservedAssignment
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])  # @ReservedAssignment
    return clean_text

def remUrl(Twit):
#--Remove URL from Tweets--#    
    return re.sub(r'https?://\S+', '', Twit, ) #r"https?://(www.)?"
#removed flags=re.MULTILINE 