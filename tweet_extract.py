import tweepy,csv,re,datetime,emoji
from textblob import TextBlob
from collections import Counter

def DownloadData(searchitem,searchTerm,NoOfTerms,ui):
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
    ui.progress.setValue(30)
    if(searchitem == 1):
        tweets = tweepy.Cursor(api.search, searchTerm + " -filter:retweets", lang="en", tweet_mode="extended").items(NoOfTerms)
    elif(searchitem == 2):
        tweets = tweepy.Cursor(api.search, "To:" + searchTerm + " -filter:retweets", lang="en", tweet_mode="extended").items(NoOfTerms)
    elif(searchitem == 3):
        tweets = tweepy.Cursor(api.search, "From:" + searchTerm + " -filter:retweets", lang="en", tweet_mode="extended").items(NoOfTerms)
    
    # Open/create a file to append data to
    csvFile = open('result' + str(datetime.datetime.now().strftime("%Y%m%d%H%M")) + '.csv', 'a', newline='', encoding="utf-8")
    # Use csv writer
    csvWriter = csv.writer(csvFile)
    ui.progress.setValue(40)
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
    ui.progress.setValue(50)
    for i in range(len(tweetText)):
        csvWriter.writerow([tweetText[i], username[i], locations[i], hash_tags[i], dates[i], day[i], tweetid[i], likes[i], retweet[i], polarityl[i]])
    csvFile.close()
    ui.progress.setValue(60)
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
    ui.progress.setValue(70)
    # finding average of how people are reacting
    positive = percentage(positive, n)
    wpositive = percentage(wpositive, n)
    spositive = percentage(spositive, n)
    negative = percentage(negative, n)
    wnegative = percentage(wnegative, n)
    snegative = percentage(snegative, n)
    neutral = percentage(neutral, n)
    polarity = polarity / len(tweetText)
    ui.progress.setValue(80)
    output="Analyzing " + str(n) + " Tweets on " + searchTerm
    output+="\nGeneral Report: "
    
    if (polarity == 0):
        output+="Neutral"
    elif (polarity > 0 and polarity <= 0.3):
        output+="Weakly Positive"
    elif (polarity > 0.3 and polarity <= 0.6):
        output+="Positive"
    elif (polarity > 0.6 and polarity <= 1):
        output+="Strongly Positive"
    elif (polarity > -0.3 and polarity <= 0):
        output+="Weakly Negative"
    elif (polarity > -0.6 and polarity <= -0.3):
        output+="Negative"
    elif (polarity > -1 and polarity <= -0.6):
        output+="Strongly Negative"
    ui.progress.setValue(100)
    output+="\nDetailed Report: \n"
    output+=str(positive) + "% people thought it was positive\n"
    output+=str(wpositive) + "% people thought it was weakly positive\n"
    output+=str(spositive) + "% people thought it was strongly positive\n"
    output+=str(negative) + "% people thought it was negative\n"
    output+=str(wnegative) + "% people thought it was weakly negative\n"
    output+=str(snegative) + "% people thought it was strongly negative\n"
    output+=str(neutral) + "% people thought it was neutral"
    ui.display_label.setText(output)
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