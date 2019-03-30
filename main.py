import tweet_extract as te
import graph_plot as gp

##-------------BEGIN INVOKING MODULES------------##
temp=te.DownloadData()
gp.plotPieChart(temp[0],temp[1], temp[2], temp[3],temp[4], temp[5], temp[6], temp[7], temp[8])
gp.barGraphM(temp[9])
gp.barGraphD(temp[10])
gp.cloud(temp[11])
gp.plotgraph(temp[12], temp[13])
##--------------------- END----------------------##