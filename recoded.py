import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import datetime
import emoji
import numpy as np
from collections import Counter
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.dates = []
        self.likes = []
        self.hash_tags = []
        self.top_hash = []
        self.retweet = []
        self.tweetid = []
        self.username = []
        self.polarityl = []
        self.day = []
        self.temp = ""
        self.temp1 = []
        
    def getTags(self, Twit):
        return re.findall(r"#(\w+)", Twit)
                        
    def free_text(self, text):
        allchars = [str for str in text]
        emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
        return clean_text

    def remUrl(self, Twit):
        return re.sub(r'https?:\/\/.*[\r\n]*', '', Twit, flags=re.MULTILINE) #r"https?://(www\.)?"

    def DownloadData(self):
        # authenticating
        consumerKey ='0q6yabp5VLtyKVpN39kLS86Lz'
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

        if(searchitem=='1'):
            self.tweets = tweepy.Cursor(api.search, searchTerm+" -filter:retweets", lang = "en").items(NoOfTerms)
        elif(searchitem=='2'):
            self.tweets = tweepy.Cursor(api.search, "To:"+searchTerm+" -filter:retweets", lang = "en").items(NoOfTerms)
        elif(searchitem=='3'):
            self.tweets = tweepy.Cursor(api.search, "From:"+searchTerm+" -filter:retweets",lang = "en").items(NoOfTerms)
    
        # Open/create a file to append data to
        csvFile = open('result'+str(datetime.datetime.now().strftime("%Y%m%d%H%M"))+'.csv', 'a', newline='',encoding="utf-8")

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetid.append(tweet.id)
            self.likes.append(tweet.favorite_count)
            self.username.append(tweet.user.screen_name)
            self.retweet.append(tweet.retweet_count)
            self.dates.append(tweet.created_at.date().strftime("%d-%m-%y"))
            self.day.append(tweet.created_at.date().strftime("%a"))
            self.temp=self.free_text(self.remUrl(self.cleanTweet((tweet.text))))
            self.tweetText.append(self.temp)
            self.hash_tags.append(self.getTags(self.temp))
            self.polarityl.append(TextBlob(self.temp).sentiment.polarity)
            
        for i in range(len(self.hash_tags)):
            self.temp1 += self.hash_tags[i]
        self.hash_count = Counter(self.temp1)
        #for key, value in {k: v for k, v in sorted(self.hash_count.items(), key=lambda x: x[1], reverse=True)}.items():
            #temp = [key,value]
            #self.top_hash.append(temp)
        
            
        csvWriter.writerow(['Tweet','username','hash-tags','Date','Day','tweet_id','likes','retweets','polarity'])
        for i in range(len(self.tweetText)):
            csvWriter.writerow([self.tweetText[i],self.username[i],self.hash_tags[i],self.dates[i],self.day[i],self.tweetid[i],self.likes[i],self.retweet[i],self.polarityl[i]])
        csvFile.close()


        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        n=len(self.tweetText)

        for text in range(len(self.tweetText)):

            analysis=TextBlob(self.tweetText[text])
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
        positive = self.percentage(positive, n)
        wpositive = self.percentage(wpositive, n)
        spositive = self.percentage(spositive, n)
        negative = self.percentage(negative, n)
        wnegative = self.percentage(wnegative, n)
        snegative = self.percentage(snegative, n)
        neutral = self.percentage(neutral, n)

        polarity = polarity / len(self.tweetText)

        print("\nAnalyzing " + str(n) + " tweets on "+searchTerm)
        print()
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

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, n)
        self.barGraphM(self.dates)
        self.barGraphD(self.day)
        self.cloud(self.hash_count)

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title("\nAnalyzing " + str(noOfSearchTerms) + " tweets on "+searchTerm)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def barGraphM(self, date):
        objects = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec')
        y_pos = np.arange(len(objects))
        x=[int(i[3:5]) for i in date]

        Jan=0
        Feb=0
        Mar=0
        Apr=0
        May=0
        Jun=0
        Jul=0
        Aug=0
        Sep=0
        Oct=0
        Nov=0
        Dec=0

        for i in range(len(x)):
            if(x[i]==1):
                Jan+=1
            elif(x[i]==2):
                Feb+=1
            elif(x[i]==3):
                Mar+=1
            elif(x[i]==4):
                Apr+=1
            elif(x[i]==5):
                May+=1
            elif(x[i]==6):
                Jun+=1
            elif(x[i]==7):
                Jul+=1
            elif(x[i]==8):
                Aug+=1
            elif(x[i]==9):
                Sep+=1
            elif(x[i]==10):
                Oct+=1
            elif(x[i]==11):
                Nov+=1
            elif(x[i]==12):
                Dec+=1

        performance = [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec]
        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Number of tweets')
        plt.xlabel('Time')
        plt.title('Tweets range month wise')
 
        plt.show()

    def barGraphD(self,day):
        objects = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat')
        y_pos = np.arange(len(objects))
        day_dict=Counter(day)
        performance=[]
        for i in range(len(objects)):
            performance.append(day_dict[objects[i]])

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Number of tweets')
        plt.xlabel('Time')
        plt.title('Tweets range day wise')
 
        plt.show()

    def cloud(self,hash):
        wc = WordCloud(background_color="white",relative_scaling=0.5).generate_from_frequencies(hash)
        plt.imshow(wc,interpolation='bilinear')
        plt.axis('off')
        plt.title('Frequent hashtags from Tweets fetched.',color='black')
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()