import tweet_extract as te
import graph_plot as gp
from PyQt5 import QtWidgets
from slider import Ui_MainWindow #this is your generated .py file 
import sys
import networkx as nx
import matplotlib.pyplot as plt
# #-------------BEGIN INVOKING MODULES------------##

class MainWindow(QtWidgets.QMainWindow):
    H = nx.Graph()
    npostweets = []
    ntotaltweets = []
    nodelist=[]
    files = ['Congress','BJP' ,'TMC', 'CPIM','AAP','RJD','BSP','Samajwadi']
    pos = []
    neg = []
    nums = []
    
    def __init__(self):
            
        print("\n\tDownloading Data")

        for names in MainWindow.files:
            try:
                te.downloadcsv(names)
            except:
                pass
        print("\n\tData Downloaded\n\tAnalyzing Data and Plotting Graphs")
        for names in MainWindow.files:
            temp = te.readfromcsv(names)
            gp.plotPieChart(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], names, temp[7],temp[8])
            #gp.cloud(temp[8])
            MainWindow.ntotaltweets.append(temp[7])
            MainWindow.npostweets.append(len(temp[9]))
            MainWindow.pos.append(temp[0] + temp[1] + temp[2])
            MainWindow.neg.append(temp[3] + temp[4] + temp[5])
            MainWindow.nums.append(names + '\n' + 'with' +'\n' + str(temp[7]) + '\n' + 'tweets')
            MainWindow.H = gp.plottest(MainWindow.H, temp[9], names)
        
        #for i in range(len(MainWindow.npostweets)):
            #MainWindow.npostweets[i]=te.percentage(MainWindow.npostweets[i],MainWindow.ntotaltweets[i])
 
        gp.barGraphP(MainWindow.pos,MainWindow.neg,MainWindow.nums)
        super(MainWindow,self).__init__() #This is the parent window object
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.kcore)
        def get_key(val):
            for key, value in res.items():
                if val == value :
                    return key
        res = nx.degree_centrality(MainWindow.H)
        temp = []
        for names in MainWindow.files:
            temp.append(res[names])

        print("From calculating the degrees of centrality for the corresponding parties, we find that with ", round(float(max(temp)),3))
        print(" degree of centrality, "+get_key(max(temp))+" has a probable chance of winning.")
        
        
    def kcore(self):
        self.ui.kvalue.setText(str(self.ui.slider.value()))
        G=MainWindow.H.copy()
        self.ui.pushButton.setDisabled(True)
        self.ui.progressBar.setValue(60)
        self.ui.progressBar.setValue(80)
        to_del = [n for n in G if G.degree(n) < self.ui.slider.value()]
        G.remove_nodes_from(to_del)
        nodes=dict(G.degree)
        for v in nodes.values():
            if v<10:
                MainWindow.nodelist.append(v*50)
            else:
                MainWindow.nodelist.append(500)

        nx.draw(G, node_size=MainWindow.nodelist, with_labels=True,alpha=0.8)
        plt.savefig('Network Graph.png',dpi=200)
        plt.show()
        self.ui.progressBar.setValue(100)
        self.ui.pushButton.setDisabled(False)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())