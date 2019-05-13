from wordcloud import WordCloud
import matplotlib.pyplot as plt
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

def barGraphP(npositivet,files):
    objects=files
    index=np.arange(len(objects))
    plt.bar(index,npositivet,align="center",alpha=0.5,color=['mediumblue','darkorange','lightseagreen','red','green','lime','midnightblue','darkred'])
    plt.ylabel("Percent of positive tweets")
    plt.xlabel("Parties")
    plt.xticks(index, objects)
    plt.title("Positive percent of tweets per party")
    plt.show()


def cloud(hash):  # @ReservedAssignment
#--Create word cloud--#    
    wc = WordCloud(background_color="white", relative_scaling=0.5).generate(hash)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Frequent hashtags from Tweets fetched.', color='black')
    plt.show()


def plottest(Gr,nodelist,mainnode):
    nodelist=list(dict.fromkeys(nodelist))
    Gr.add_nodes_from(nodelist)
    for i in range(len(nodelist)):
        Gr.add_edge(nodelist[i],mainnode)
    return Gr


