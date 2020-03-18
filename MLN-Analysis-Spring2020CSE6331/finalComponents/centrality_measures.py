# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 12:47:23 2020

@author: salon
"""
import os
import networkx as nx
import matplotlib.pyplot as plt
import operator

class CentralityMeasure(object):
    def __init__(self,edge_input,centrality):
        self.sanityCheck = True
        self.vertices = []
        self.edges = []
        self.edge_input = edge_input
        self.centrality = centrality
        self.dataset = '' 
    
    def set_dataset(self, ds_name):
        self.dataset = ds_name
        return None
    
    def get_dataset_name(self):
        return self.dataset
    
    def parse_input(self,filename):
        with open(filename) as f:
            content = f.readlines()
            #Remove `\n` at the end of each line
            content = [x.strip() for x in content] 
            f.close()
        return content
    
    def computeCentrality(self):
        
        self.sanity_check(self.edge_input);
        
        if self.sanityCheck == True:
            G = nx.Graph()
            G.add_nodes_from(self.vertices)
            for edge in self.edges:
                #print(edge[2])
                G.add_edge(edge[0],edge[1],weight=edge[2])
                '''
                labels = []
                for e in G.edges.data():
                    labels.append(e[2]['weight'])
                    
                    nx.draw(G,with_labels=True)  # networkx draw()
                    plt.plot()'''
                    
            if self.centrality.lower() == 'between'.lower():
                betweeness_values=nx.betweenness_centrality(G,normalized=True,weight='weight')
                max_between = dict(sorted(betweeness_values.items(), key=operator.itemgetter(1), reverse=True))
                #print("Max Betweeness vertices",max_between)
                return max_between
            else:
                if self.centrality.lower() == 'eigen'.lower():
                  eigen_centrality = nx.eigenvector_centrality(G)
                  max_eigen = dict(sorted(eigen_centrality.items(), key=operator.itemgetter(1), reverse=True))
                  #print("Max Eigen vertices",max_eigen)
                  return max_eigen 
            
        else:
            print("Error: Sanity Check did not pass")
            
    
    def sanity_check(self,edge_input):
        #edge_input="\centralityTestData\Spirit.txt"
        #path="\MLN-Analysis-Spring2020CSE6331\IMDB-Top-500-Actors\Layers" 
        #current_dir = os.path.dirname(os.path.realpath(__file__))
        #Constant used. Might need to adjust if structure of folder is changed
        #target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])
        #path=target_dir+path+edge_input
        #print(path) 
        data=self.parse_input(filename=edge_input)
               
        nameOfAirline=data[0]
        print("name of the airline: ",nameOfAirline)
        self.set_dataset(nameOfAirline)
        
        #Check if 1st line is name of airline
        if not isinstance(nameOfAirline,str):
            self.sanityCheck=False
            print("First line should be name of airline company")

        try:
            numberOfVertices=int(data[1])
            print("numberOfVertices: ",numberOfVertices)
        except ValueError:
            print("Second line must be an integer with the number of vertices in the graph")
            self.sanityCheck=False
        try:
            numberofEdges=int(data[2])
            print("numberofEdges: ",numberofEdges)
        except ValueError:
            print("Second line must be an integer with the number of edges in the graph")
            self.sanityCheck=False
                    
       
        tempVerticesCount=numberOfVertices
        tempEdgesCount=numberofEdges
        
        for i in range(3,3+numberOfVertices):
            #Check that there is only 1 vertex per line of the file
            if "," in data[i]:
                self.sanityCheck=False
                print("There are more than 1 vertices on line %d since they are separated by a comma" %(i+1))
                break
            self.vertices.append(data[i])
            tempVerticesCount-=1
            
        #Check if number of vertices mentioned is not more than input vertices
        
        if tempVerticesCount>0:
            print("Input vertices are lesser than mentioned number of input vertices")
            self.sanityCheck=False
                
                #if sanity check of vertices is passed, go to edges
        if self.sanityCheck:
            for i in range(3+numberOfVertices,len(data)):
                
                try:
                    currentEdge=data[i].split(",")
                    
                    try:
                        currentEdge[2]=float(currentEdge[2])
                    except ValueError:
                            print("Input weight must be a floating number. Error on line %d" %(i+1))
                            print("Format of edge should be vertex1,vertex2,weight")
                            self.sanityCheck=False
                    vertex1Present=False
                    vertex2Present=False
                    
                    #Check if both input vertices are present in the vertices given input above
                    if currentEdge[0] in self.vertices:
                        
                        vertex1Present=True
                    if vertex1Present==False:
                        print("Vertex 1 on line %d is not given in the input vertices" %(i+1))
                        self.sanityCheck=False
                        break
                                
                    if currentEdge[1] in self.vertices:
                        
                        vertex2Present=True
                    if vertex2Present==False:
                        print("Vertex 2 on line %d is not given in the input vertices" %(i+1))
                        self.sanityCheck=False
                        break
                    
                    #If both present then add edge
                    if vertex1Present and vertex2Present:
                    
                        self.edges.append(currentEdge)
                        tempEdgesCount-=1
                        
                except IndexError:
                        #In case number of vertices is more than specified number it will spill over to edges loop
                        #We will get incorrect format for edge and it will come to this part of the code
                        #If len of currentEdge is 1 we can assume it is a vertex
                        if len(currentEdge)==1:
                            print("The number of vertices has exceeded %d. Extra vertex on line %d" %(numberOfVertices,i+1))
                        print("Format of edge on line %d is not correct. It should be vertex1,vertex2,weight" %(i+1))
                        self.sanityCheck=False
                        break
            #Check if number of edges mentioned is not equal to input edges
           
            if tempEdgesCount<0:
               print("Input edges are more than mentioned number of input vertices")
               self.sanityCheck=False
              
            if tempEdgesCount>0:
                print("Input edges are lesser than mentioned number of input vertices")
                self.sanityCheck=False
                        
                    
                                                                            