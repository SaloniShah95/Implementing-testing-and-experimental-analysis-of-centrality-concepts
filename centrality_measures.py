# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 12:30:14 2020

@author: MOHIT, Saloni
"""
import os
import networkx as nx
import matplotlib.pyplot as plt
import operator

#Take input file. Defining as constant for now.

def parse_input(filename):
    with open(filename) as f:
        content = f.readlines()
        #Remove `\n` at the end of each line
        content = [x.strip() for x in content] 
        
        f.close()
    return content

dataFile="\American"
path="\MLN-Analysis-Spring2020CSE6331\IMDB-Top-500-Actors\Layers" 
current_dir = os.path.dirname(os.path.realpath(__file__))
#Constant used. Might need to adjust if structure of folder is changed
target_dir = os.path.sep.join(current_dir.split(os.path.sep))
path=target_dir+path+dataFile
print(path)
data=parse_input(path)

nameOfAirline=data[0]
numberOfVertices=int(data[1])
numberofEdges=int(data[2])
Edges=[]
Vertices=[]

for i in range(3,3+numberOfVertices):
    Vertices.append(data[i])
    
for i in range(3+numberOfVertices,3+numberOfVertices+numberofEdges):
    currentEdge=data[i].split(",")
    currentEdge[2]=float(currentEdge[2])
    Edges.append(currentEdge)
    
G = nx.DiGraph()
G.add_nodes_from(Vertices)
for edge in Edges:
    #print(edge[2])
    G.add_edge(edge[0],edge[1],weight=edge[2])


labels = []
for e in G.edges.data():
    labels.append(e[2]['weight'])
#print(labels)

betweeness_values=nx.betweenness_centrality(G)

eigen_centrality = nx.eigenvector_centrality(G)
#eigen_centrality2 = nx.eigenvector_centrality(G,max_iter=10000000000000000000000000000000)
#comparing the 2
#comparision = eigen_centrality == eigen_centrality2

max_eigen = max(eigen_centrality.values())
max_vertex = max(eigen_centrality, key=eigen_centrality.get) 

max_between = max(betweeness_values.values())
max_vertex_b = max(betweeness_values, key=eigen_centrality.get) 

closeness_values = nx.closeness_centrality(G)
'''
nx.draw(G,with_labels=True,edge_labels=labels)  # networkx draw()
plt.plot()'''