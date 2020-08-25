# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:27:59 2020

@author: Mohit and Saloni
"""

import os
import networkx as nx
from networkx.algorithms import approximation as apxa
import sys
from finalComponents.centrality_measures import CentralityMeasure
import operator
import pandas as pd

def parse_input(filename):
    
    with open(filename) as f:
        content = f.readlines()
        #Remove `\n` at the end of each line
        content = [x.strip() for x in content] 
        f.close()
    return content

def sanityCheck(filename):
    #change the path according to the input file given in as input parameters

    #change to name of the directory these files reside in
    dataFile=filename
    #set "path" to the path to the aforementioned directory
    path="\CSE6331_project\Final_Submission\Data\Layers" 
    current_dir = os.path.dirname(os.path.realpath(__file__))
    #Constant used. Might need to adjust if structure of folder is changed
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])
    path=target_dir+path+"\\"+dataFile
      
    data=parse_input(path)


    #Assign sanity check as True
    sanityCheck=True
    print(data[0])
    nameOfAirline=data[0]
    #Check if 1st line is name of airline
    if not isinstance(nameOfAirline,str):
        sanityCheck=False
        print("First line should be name of layer")
    
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
            return Vertices,Edges,numberOfVertices

def get_subgraph_diameter(Vertices, Edges):
    G = nx.Graph()
    G.add_nodes_from(Vertices)
    for edge in Edges:
        if edge[0] in Vertices and edge[1] in Vertices:
            G.add_edge(edge[0],edge[1],weight=edge[2])
    return nx.diameter(G)   
def get_subgraph_asp(Vertices, Edges):
    G = nx.Graph()
    G.add_nodes_from(Vertices)
    for edge in Edges:
        if edge[0] in Vertices and edge[1] in Vertices:
            G.add_edge(edge[0],edge[1],weight=edge[2])
    return nx.average_shortest_path_length(G)  
    

def main():
    avg_betweenness = {}
    graph_diameter = {}
    graph_radius = {}
    graph_avg_distance = {}
    avg_closeness = {}
    avg_eccentricity = {}
    avg_degree = {} 
    graph_density = {}
    avg_eigen = {}
    avg_graph_clustering={}
    assortivity_coefficient={}
    no_bridges = {}
    number_of_nodes = {}
    eigen_hubs = {}
    
    
    for i in range (1, len(sys.argv)-1):
        #iterating through files
        filename=sys.argv[i]
        #change to name of the directory these files reside in
        dataFile=filename
        #set "path" to the path to the aforementioned directory
        path="S:\course work\Adv topics in databases\gitrepo\CSE6331_project\Final_Submission\Data\Layers"    

        #last input is the name of the output file        
        outputfile = sys.argv[-1]
        
        Vertices,Edges,number_of_verts=sanityCheck(filename) 
        #generating a graph        
        G = nx.Graph()
        G.add_nodes_from(Vertices)
        for edge in Edges:
            G.add_edge(edge[0],edge[1],weight=edge[2])

       #calculating average betweeness centrality of the current layer 
        c_count= 0
        _sum = 0
        cm = CentralityMeasure(edge_input=path+"\\"+dataFile,centrality='Between')
        C_values,time = cm.computeCentrality()
        for key in C_values:
            c_count += 1
            _sum += C_values[key]
        average_betweeness = _sum/c_count

        #calculating average closeness centrality of the current layer
        _sum = 0                    
        c_count = 0
        cm = CentralityMeasure(edge_input=path+"\\"+dataFile,centrality='close')
        C_values,time = cm.computeCentrality()
        for key in C_values:
                c_count += 1
                _sum += C_values[key]
        average_closeness = _sum/c_count
        
        
       #calculating average degree centrality of the current layer
        _sum = 0                    
        c_count = 0
        cm = CentralityMeasure(edge_input=path+"\\"+dataFile,centrality='degree')
        C_values,time = cm.computeCentrality()
        for key in C_values:
                c_count += 1
                _sum += C_values[key]
        average_degree = _sum/c_count 
        
        #calculating average eigen centrality of the current layer
        _sum = 0                    
        c_count = 0
        cm = CentralityMeasure(edge_input=path+"\\"+dataFile,centrality='eigen')
        C_values,time = cm.computeCentrality()
        eigen_hubs_list,average = cm.get_hubs(C_values);
        for key in C_values:
                c_count += 1
                _sum += C_values[key]
        average_eigen = _sum/c_count
        
        
        f = open(path+"\\"+dataFile,"r")
        Lines = f.readlines() 
        layer_name = Lines[0].strip()

        #calculating diameter of connected graphs
        #if the graph is not connected then find the maximum of diameter among all the components
        diams = []
        avg_short_path = []
        if(nx.is_connected(G)):
            graph_diameter[layer_name] = nx.diameter(G)
            graph_avg_distance[layer_name] = nx.average_shortest_path_length(G)
        else:
            
            diams = []
            avg_short_path = []
            components = (nx.connected_components(G))
            
            for c in components:
                diams.append(get_subgraph_diameter(c,Edges))
                avg_short_path.append(get_subgraph_asp(c,Edges))
            graph_diameter[layer_name]=max(diams)
            graph_avg_distance[layer_name] = max(avg_short_path)
            
        
        
        avg_betweenness[layer_name] = average_betweeness              
        avg_closeness[layer_name] = average_closeness        
        avg_degree[layer_name] = average_degree
        graph_density[layer_name] = nx.density(G)
        avg_eigen[layer_name] = average_eigen
        avg_graph_clustering[layer_name] = nx.average_clustering(G)
        assortivity_coefficient[layer_name] = nx.degree_assortativity_coefficient(G)
        number_of_nodes[layer_name] = len(Vertices)
        eigen_hubs[layer_name] = len(eigen_hubs_list)

    #sorting the dictionaries containing centrality values             
    sorted_eigen = dict(sorted(avg_eigen.items(), key=operator.itemgetter(1), reverse=True)) 
    sorted_betweeness = dict(sorted(avg_betweenness.items(), key=operator.itemgetter(1), reverse=True))
    sorted_closeness = dict(sorted(avg_closeness.items(), key=operator.itemgetter(1), reverse=True))
    sorted_degree = dict(sorted(avg_degree.items(), key=operator.itemgetter(1), reverse=True)) 

    #writing calculated graph characteristics to file containing output for betweenness centrality    
    betweenness_list = []
    for graph, value in sorted_betweeness.items():
            key = graph

            b_list = []
            b_list.append(key)
            b_list.append(number_of_nodes[key])
            b_list.append(avg_betweenness[key]) 
            b_list.append(graph_diameter[key])
            b_list.append(avg_graph_clustering[key])
            betweenness_list.append(b_list)
            
    
    betweenness_df = pd.DataFrame(betweenness_list,columns = ["Layer","No. of nodes","avg_betweenness","graph diameter","clustering coefficient"])
    #set output_path to the path to the output directory
    output_path = "S:\\course work\\Adv topics in databases\\gitrepo\CSE6331_project\\Final_Submission\\Data\\Layers\\SingleLayer-TestData\\Outputs\\"
    print("Writing all outputs to "+output_path+outputfile)
     
    betweenness_df.to_csv(output_path+outputfile+"_between.csv")                    

    #writing calculated graph characteristics to file containing output for closeness centrality
    closeness_list = []    
    for graph, value in sorted_closeness.items():
            key = graph
           
            
            c_list = []
            c_list.append(key)
            c_list.append(number_of_nodes[key])
            c_list.append(avg_closeness[key])
            c_list.append(graph_avg_distance[key])
            c_list.append(graph_diameter[key])
            c_list.append(avg_graph_clustering[key])
            closeness_list.append(c_list)
    
    closeness_df = pd.DataFrame(closeness_list,columns = ["Layer","No. of nodes","avg_closeness","graph_avg_distance","graph diameter","clustering coefficient"])    
    closeness_df.to_csv(output_path+outputfile+"_close.csv")                    

   #writing calculated graph characteristics to file containing output for degree centrality
    degree_list=[]
    for graph, value in sorted_degree.items():
            key = graph
            
            d_list = []
            d_list.append(key)
            d_list.append(number_of_nodes[key])
            d_list.append(avg_degree[key])
            d_list.append(graph_density[key]) 
            d_list.append(assortivity_coefficient[key])
            d_list.append(graph_diameter[key])   
            d_list.append(avg_graph_clustering[key])
            degree_list.append(d_list)
        
    degree_df = pd.DataFrame(degree_list,columns = ["Layer","No. of nodes","avg_degree","density","assortivity_coefficient","graph diameter","clustering coefficient"])    
    degree_df.to_csv(output_path+outputfile+"_degree.csv")                    

    #writing calculated graph characteristics to file containing output for eigen centrality
    eigen_list = []
    for graph, value in sorted_eigen.items():
            key = graph
            
            e_list = []
            e_list.append(key)
            e_list.append(number_of_nodes[key])
            e_list.append(avg_eigen[key]) 
            e_list.append(assortivity_coefficient[key])
            e_list.append(eigen_hubs[key])
            e_list.append(avg_graph_clustering[key])
            eigen_list.append(e_list)
    eigen_df = pd.DataFrame(eigen_list,columns = ["Layer","No. of nodes","avg_eigen","assortivity_coefficient","number of hubs","clustering coefficient"])    
    eigen_df.to_csv(output_path+outputfile+"_eigen.csv")                    
       

        
if __name__== "__main__":
    main()   
