# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 16:40:03 2020

@author: Mohit and Saloni
"""
import sys
from statistics import mean
import time
from CtoPython import runANDCompCode
from centrailty_measures import sanityCheck
from centrailty_measuresv3 import sanityCheckv3

#variables to store file names from command line input
file1=sys.argv[1]
file2=sys.argv[2]

#function to find ground truth
def groundTruth():
    runANDCompCode()
    filename=file1+"_AND_"+file2
    print("Finding ground truth for "+str(filename))
    return sanityCheck(filename)

#Find the betweenness for a layer    
def layerBetweeness(file):
    return sanityCheck(file)

#Find the intersection of 2 lists
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

#Find the union of 2 lists   
def Union(lst1, lst2): 
    final_list = lst1 + lst2 
    return final_list 


#Ground truth calculation
#Start clock time
start = time.time()

#Calculate betweenness in AND composition which is the ground truth
betweeness_ground_truth=groundTruth()
#Calculate mean of all betweenness values
mean_bet_gt=mean(betweeness_ground_truth[k] for k in betweeness_ground_truth)

#find out the hubs
hubs_gt=[]
for k,v in betweeness_ground_truth.items():
   if v>mean_bet_gt:
        hubs_gt.append(k)

#end clock time      
end = time.time()
gt_time=(end-start)/60
print("Average betweeness of ground truth",mean_bet_gt)
print("Time for ground truth calculation",gt_time)
print("#hubs in ground truth",len(hubs_gt))
print("Ground truth hubs",hubs_gt)

with open('ground_truth.txt', 'w+') as f:
    f.write("Layer 1 %s\n" %(file1))
    f.write("Layer 1 %s\n" %(file2))
    f.write("\n")
    f.write("Average betweenness for ground truth %.3f\n" %(mean_bet_gt))
    f.write("\n")
    f.write("The Ground truth hubs are:\n")
    for item in hubs_gt:
        f.write("Hub:%s Betweenness:%.3f\n" % (item,betweeness_ground_truth[item]))
#----------------------Naive AND-------------------------
#Start clock time
start = time.time()

#Calculate betweeness values for layer 1
layer1_betweeness=layerBetweeness(file1)
#Calculate mean of all betweenness values
mean_bet_l1=mean(layer1_betweeness[k] for k in layer1_betweeness)

#Calculate hubs for layer 1
hubs_l1=[]
for k,v in layer1_betweeness.items():
    if v>mean_bet_l1:
        #print("Hub %s:Value %f" %(k,v))
        hubs_l1.append(k)

#Do the same for layer 2
layer2_betweeness=layerBetweeness(file2)
mean_bet_l2=mean(layer2_betweeness[k] for k in layer2_betweeness)

hubs_l2=[]
for k,v in layer2_betweeness.items():
    if v>mean_bet_l2:
        #print("Hub %s:Value %f" %(k,v))
        hubs_l2.append(k)
        

#Find intersection of the 2 lists of hubs from layer 1 and layer 2
hubs_naiveAND=intersection(hubs_l1, hubs_l2)
end = time.time()
print("Mean betweeness layer 1 "+str(file1)+" is "+str(mean_bet_l1))
print("Mean betweeness layer 2 "+str(file2)+" is "+str(mean_bet_l2))
print("#Hubs in "+str(file1)+" is "+str(len(hubs_l1)))
print("#Hubs in "+str(file2)+" is "+str(len(hubs_l2)))
print("Naive AND: Number of hubs calculated by the heuristic",len(hubs_naiveAND))
heu_time=end-start
print("Naive AND: Time for heuristic to run",heu_time/60)
intersection = len(list(set(hubs_naiveAND).intersection(hubs_gt)))
union = (len(hubs_naiveAND) + len(hubs_gt)) - intersection
print("Naive AND: Jaccard",float(intersection) / union)

false_positives=0
false_negatives=0     
for hub in hubs_naiveAND:
    if hub not in hubs_gt:
        false_positives+=1
        
for hub in hubs_gt:
    if hub not in hubs_naiveAND:
        false_negatives+=1
  
fpa=100*false_positives/len(hubs_naiveAND)
fna=100*false_negatives/len(hubs_gt)
print("Naive AND: Precision",100-fpa)
print("Naive AND: Recall",100-fna)
print("NAIVE AND hubs",hubs_naiveAND)

with open('naive_and.txt', 'w+') as f:
    f.write("Layer 1 %s\n" %(file1))
    f.write("Layer 1 %s\n" %(file2))
    f.write("\n")
    f.write("The Ground truth hubs are:\n")
    for item in hubs_gt:
        f.write("%s\n" % item)
    f.write("\n")
    f.write("The Naive AND hubs are:\n")
    for item in hubs_naiveAND:
        f.write("%s\n" % item)
f.close()
#-----------------------Min Heuristic----------------------
#Start clock time
start = time.time()
#Calculate betweeness values for layer 1
layer1_betweeness=layerBetweeness(file1)

#Calculate betweeness values for layer 2
layer2_betweeness=layerBetweeness(file2)

#Get the intersection of nodes from both layers
common_keys=layer1_betweeness.keys() & layer2_betweeness.keys()

min_betweeneess_layers = {}
#For each node do betweennes=min(betweeness layer 1,betweeness layer 2)
for key in common_keys:
    min_betweeneess_layers[key]=min(layer1_betweeness[key],layer2_betweeness[key])

#Find the mean of these mins
mean_bet=mean(min_betweeneess_layers[k] for k in min_betweeneess_layers)

#Calculate the hubs
hubs1_heuristic=[k for k,v in min_betweeneess_layers.items() if v>mean_bet]

#End clock time
end = time.time()
time_intersection=(end-start)/60
print("Min Heuristic: Time for heuristic",time_intersection)
print("Min Heuristic: Average betweenness value",mean_bet)
print("Min Heuristic: #estimated hubs ",len(hubs1_heuristic))

#Calculate precision,recall and jaccard
false_positives=0
false_negatives=0     
for hub in hubs1_heuristic:
    if hub not in hubs_gt:
        false_positives+=1
        
for hub in hubs_gt:
    if hub not in hubs1_heuristic:
        false_negatives+=1

list1=hubs1_heuristic
list2=hubs_gt

intersection = len(list(set(list1).intersection(list2)))
union = (len(list1) + len(list2)) - intersection
jaccardi=float(intersection) / union
print("Min Heuristic: Jaccard",jaccardi)
fpi=100*false_positives/len(hubs1_heuristic)
fni=100*false_negatives/len(hubs_gt)
print("Min Heuristic: Precision",100-fpi)
print("Min Heuristic: Recall",100-fni)
print("Min heuristic hubs",hubs1_heuristic)

with open('min_heuristic.txt', 'w+') as f:
    f.write("Layer 1 %s\n" %(file1))
    f.write("Layer 1 %s\n" %(file2))
    f.write("Average betweenness for ground truth %.3f\n" %(mean_bet_gt))
    f.write("The Ground truth hubs are:\n")
    for item in hubs_gt:
        f.write("Hub:%s Betweenness:%.3f\n" % (item,betweeness_ground_truth[item]))
    f.write("\n")
    f.write("Average betweenness for min heuristic %.3f\n" %(mean_bet))
    f.write("The Min Heuristic hubs are:\n")
    for item in hubs1_heuristic:
        f.write("Hub:%s Betwenness:%.3f\n" % (item,min_betweeneess_layers[item]))
f.close()
#----------------Avg heuristic--------------------------------

#Start clock time
start = time.time()

#Calculate betweeness values for layer 1
layer1_betweeness=layerBetweeness(file1)
#Calculate betweeness values for layer 2
layer2_betweeness=layerBetweeness(file2)

#Calculate average betweennes values for every node=((betweeness layer 1+betweeness layer 2)/2)
avg_betweeneess_layers = {}
for key in layer1_betweeness:
    avg_betweeneess_layers[key]=(layer1_betweeness[key]+layer2_betweeness[key])/2

#Calculate the average for these averages for all nodes
mean_bet=mean(avg_betweeneess_layers[k] for k in avg_betweeneess_layers)

#Calculate hubs
hubs1_heuristic=[k for k,v in avg_betweeneess_layers.items() if v>mean_bet]

#End clock
end = time.time()
time_intersection=(end-start)/60
print("Avg heuristic: Time for heuristic",time_intersection)
print("Avg heuristic: Average betweeness value",mean_bet)
print("Avg heuristic #estimated hubs ",len(hubs1_heuristic))

#Calculate Jaccrad, Precision, recall
false_positives=0
false_negatives=0     
for hub in hubs1_heuristic:
    if hub not in hubs_gt:
        false_positives+=1
        
for hub in hubs_gt:
    if hub not in hubs1_heuristic:
        false_negatives+=1

list1=hubs1_heuristic
list2=hubs_gt
intersection = len(list(set(list1).intersection(list2)))
union = (len(list1) + len(list2)) - intersection
jaccardi=float(intersection) / union
print("Avg heuristic: Jaccard",jaccardi)
fpi=100*false_positives/len(hubs1_heuristic)
fni=100*false_negatives/len(hubs_gt)
print("Avg heuristic: Precision",100-fpi)
print("Avg heuristic: Recall",100-fni)
print("Avg heuristic hubs",hubs1_heuristic)

with open('avg_heuristic.txt', 'w+') as f:
    f.write("Layer 1 %s\n" %(file1))
    f.write("Layer 1 %s\n" %(file2))
    f.write("\n")
    f.write("Average betweenness for ground truth %.3f\n" %(mean_bet_gt))
    f.write("The Ground truth hubs are:\n")
    for item in hubs_gt:
        f.write("Hub:%s Betweenness:%.3f\n" % (item,betweeness_ground_truth[item]))
    f.write("\n")
    f.write("Average betweenness for avg heuristic %.3f\n" %(mean_bet))
    f.write("The Avg Heuristic hubs are:\n")
    for item in hubs1_heuristic:
        f.write("Hub:%s Betwenness:%.3f\n" % (item,avg_betweeneess_layers[item]))
f.close()
#--------------- Edge betweeness------------------------------

#Start clock
start1 = time.time()
#Calculate edge betweeness for layer 1 and layer 2
layer1=sanityCheckv3(file1)
layer2=sanityCheckv3(file2)

#Find the intersection of edges from layer 1 and layer 2
common_keys=layer1.keys() & layer2.keys()

#For each edge do betweennes=min(betweeness layer 1,betweeness layer 2)
min_betweeneess_layers = {}
for key in common_keys:
    min_betweeneess_layers[key]=min(layer1[key],layer2[key])

#Find the average of these mins
mean_bet=mean(min_betweeneess_layers[k] for k in min_betweeneess_layers if min_betweeneess_layers[k]>0)

#print("Edge betweeness Mean betweeness of heuristic",mean_bet)

#Find the edges that are hubs
edge_hubs=[]
for k,v in min_betweeneess_layers.items():
    if v>mean_bet*0.7:
        edge_hubs.append(k)

#Find the count of nodes from the edge hubs
node_count={}
for edge in edge_hubs:
    try:
        node_count[edge[0]]+=1
    except:
        node_count[edge[0]]=1
    try:
        node_count[edge[1]]+=1
    except:
        node_count[edge[1]]=1

#Eliminate the nodes that have count==1 
hubs=[k for k,v in node_count.items() if v>1]
end1 = time.time()

print("Mohit's heuristic: number of predicted hubs",len(hubs))
print("Mohit's heuristic: Time for heuristic",(end1-start1)/60)

#Find Jaccard, Precision, Recall
false_positives=0
false_negatives=0     
for hub in hubs:
    if hub not in hubs_gt:
        false_positives+=1
        
for hub in hubs_gt:
    if hub not in hubs:
        #print(hub)
        false_negatives+=1

list1=hubs
list2=hubs_gt

intersection = len(list(set(list1).intersection(list2)))
union = (len(list1) + len(list2)) - intersection
jaccard=float(intersection) / union
print("Mohit's heuristic: Jaccard",jaccard)
        
fp=100*false_positives/len(hubs)
fn=100*false_negatives/len(hubs_gt)
print("Mohit's heuristic: Precision",100-fp)
print("Mohit's heuristic: Recall",100-fn)
print("Mohit's heuristic hubs",hubs)

with open('mohit_heuristic.txt', 'w+') as f:
    f.write("Layer 1 %s\n" %(file1))
    f.write("Layer 1 %s\n" %(file2))
    f.write("\n")
    f.write("The Ground truth hubs are:\n")
    for item in hubs_gt:
        f.write("%s\n" % item)
    f.write("\n")
    f.write("The Mohit's heuristic hubs are:\n")
    for item in hubs:
        f.write("%s\n" % item)
f.close()