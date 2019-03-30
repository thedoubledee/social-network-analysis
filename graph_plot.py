from collections import Counter
from itertools import combinations
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def plotPieChart(positive, wpositive, spositive, negative, wnegative,snegative, neutral, searchTerm, noOfSearchTerms):
#--Create pie chart--#
    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]', 'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
    plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(labels, loc="best") #Changes to code from plt.legend(patches, labels, loc="best")
    plt.title("\nAnalyzing " + str(noOfSearchTerms) + " tweets on " + searchTerm)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def barGraphM(date):
#--Create month-wise bar graph--#    
    objects = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
    y_pos = np.arange(len(objects))
    x = [int(i[3:5]) for i in date]
    Jan = 0
    Feb = 0
    Mar = 0
    Apr = 0
    May = 0
    Jun = 0
    Jul = 0
    Aug = 0
    Sep = 0
    Oct = 0
    Nov = 0
    Dec = 0
    for i in range(len(x)):
        if(x[i] == 1):
            Jan += 1
        elif(x[i] == 2):
            Feb += 1
        elif(x[i] == 3):
            Mar += 1
        elif(x[i] == 4):
            Apr += 1
        elif(x[i] == 5):
            May += 1
        elif(x[i] == 6):
            Jun += 1
        elif(x[i] == 7):
            Jul += 1
        elif(x[i] == 8):
            Aug += 1
        elif(x[i] == 9):
            Sep += 1
        elif(x[i] == 10):
            Oct += 1
        elif(x[i] == 11):
            Nov += 1
        elif(x[i] == 12):
            Dec += 1

    performance = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of tweets')
    plt.xlabel('Time')
    plt.title('Tweets range month wise')
    plt.show()

def barGraphD(day):
#--Create day-wise bar graph--#    
    objects = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
    y_pos = np.arange(len(objects))
    day_dict = Counter(day)
    performance = []
    for i in range(len(objects)):
        performance.append(day_dict[objects[i]])
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of tweets')
    plt.xlabel('Time')
    plt.title('Tweets range day wise')
    plt.show()

def cloud(hash):  # @ReservedAssignment
#--Create word cloud--#    
    wc = WordCloud(background_color="white", relative_scaling=0.5).generate_from_frequencies(hash)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Frequent hashtags from Tweets fetched.', color='black')
    plt.show()

def graphedges(hashlist):
#--Create edge graph--#    
    comb=()
    temp2 = []
    for i in range(len(hashlist)):
        comb = combinations(hashlist[i], 2)
        for j in list(comb):
            temp2.append(list(j))
    return temp2

def plotgraph(hashtag, nodelist):
#--Create edge graph chart--#
    hashcomb=graphedges(hashtag)
    nodelist=list(dict.fromkeys(nodelist))
    G=nx.Graph()
    G.add_nodes_from(nodelist)
    G.add_edges_from(hashcomb)
    nx.draw(G, with_labels=True)
    plt.show()
