# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 12:30:14 2020

@author: Mohit, Saloni
"""
import os
import networkx as nx
import matplotlib.pyplot as plt

def computeCentrailty(Vertices,Edges):
    G = nx.Graph()
    G.add_nodes_from(Vertices)
    for edge in Edges:
        #print(edge[2])
        G.add_edge(edge[0],edge[1],weight=edge[2])

        '''
        labels = []
        for e in G.edges.data():
            labels.append(e[2]['weight'])

        nx.draw(G,with_labels=True,edge_labels=labels)  # networkx draw()
        nx.draw(G,with_labels=True)
        plt.plot()
        '''
    betweeness_values=nx.betweenness_centrality(G,normalized=True,weight='weight')
    print("Betweeness",betweeness_values)

    eigen_centrality = nx.eigenvector_centrality(G)
    print("Eigen",eigen_centrality)
    #eigen_centrality2 = nx.eigenvector_centrality(G,max_iter=10000000000000000000000000000000)
    #comparing the 2
    #comparision = eigen_centrality == eigen_centrality2

    max_eigen = max(eigen_centrality.values())
    max_vertex = max(eigen_centrality, key=eigen_centrality.get) 

    max_between = max(betweeness_values.values())
    max_vertex_b = max(betweeness_values, key=eigen_centrality.get) 

    closeness_values = nx.closeness_centrality(G)

#Take input file. Defining as constant for now.

def parse_input(filename):
    with open(filename) as f:
        content = f.readlines()
        #Remove `\n` at the end of each line
        content = [x.strip() for x in content] 
        f.close()
    return content

dataFile="\BetweenessTest.txt"
path="\MLN-Analysis-Spring2020CSE6331\IMDB-Top-500-Actors\Layers" 
current_dir = os.path.dirname(os.path.realpath(__file__))
#Constant used. Might need to adjust if structure of folder is changed
target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])
path=target_dir+path+dataFile
print(path)  
data=parse_input(path)

#Assign sanity check as True
sanityCheck=True
nameOfAirline=data[0]
#Check if 1st line is name of airline
if not isinstance(nameOfAirline,str):
    sanityCheck=False
    print("First line should be name of airline company")

try:
    numberOfVertices=int(data[1])
except ValueError:
    print("Second line must be an integer with the number of vertices in the graph")
    sanityCheck=False
try:
    numberofEdges=int(data[2])
except ValueError:
    print("Second line must be an integer with the number of edges in the graph")
    sanityCheck=False
    
Edges=[]
Vertices=[]

tempVerticesCount=numberOfVertices
tempEdgesCount=numberofEdges

for i in range(3,3+numberOfVertices):
    #Check that there is only 1 vertex per line of the file
    if "," in data[i]:
        sanityCheck=False
        print("There are more than 1 vertices on line %d since they are separated by a comma" %(i+1))
        break
    Vertices.append(data[i])
    tempVerticesCount-=1

#Check if number of vertices mentioned is not more than input vertices
if tempVerticesCount>0:
    print("Input vertices are lesser than mentioned number of input vertices")
    sanityCheck=False

#if sanity check of vertices is passed, go to edges
if sanityCheck:    
    for i in range(3+numberOfVertices,len(data)):
        try:
            currentEdge=data[i].split(",")
            try:
                currentEdge[2]=float(currentEdge[2])
            except ValueError:
                print("Input weight must be a floating number. Error on line %d" %(i+1))
                print("Format of edge should be vertex1,vertex2,weight")
                sanityCheck=False
            vertex1Present=False
            vertex2Present=False
            #Check if both input vertices are present in the vertices given input above
            if currentEdge[0] in Vertices:
                vertex1Present=True
            if vertex1Present==False:
                print("Vertex 1 on line %d is not given in the input vertices" %(i+1))
                sanityCheck=False
                break
        
            if currentEdge[1] in Vertices:
                vertex2Present=True
            if vertex2Present==False:
                print("Vertex 2 on line %d is not given in the input vertices" %(i+1))
                sanityCheck=False
                break
        
            #If both present then add edge
            if vertex1Present and vertex2Present:
                Edges.append(currentEdge)
                tempEdgesCount-=1
            
        except IndexError:
            #In case number of vertices is more than specified number it will spill over to edges loop
            #We will get incorrect format for edge and it will come to this part of the code
            #If len of currentEdge is 1 we can assume it is a vertex
            if len(currentEdge)==1:
                print("The number of vertices has exceeded %d. Extra vertex on line %d" %(numberOfVertices,i+1))
            print("Format of edge on line %d is not correct. It should be vertex1,vertex2,weight" %(i+1))
            sanityCheck=False
            break
    
    #Check if number of edges mentioned is not equal to input edges
    if tempEdgesCount<0:
        print("Input edges are more than mentioned number of input vertices")
        sanityCheck=False
    
    if tempEdgesCount>0:
        print("Input edges are lesser than mentioned number of input vertices")
        sanityCheck=False
        
    if sanityCheck:
        computeCentrailty(Vertices,Edges)
