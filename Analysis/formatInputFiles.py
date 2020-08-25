# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:12:34 2020

@author: Saloni
"""
import pandas as pd
import sys
import numpy as np

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3
 
def main():
    #file containing list of edges 
    data_file = (sys.argv[1])
    #change the path to the directory that has input files
    path = "S:\\course work\\Adv topics in databases\\gitrepo\\CSE6331_project\\Final_Submission\\Data\\Layers\\"

    #take separator as input 
    separator = (sys.argv[3])
    print("separator: ",separator)
    if separator.lower() == "space".lower():
        data = pd.read_csv(path+data_file, sep=" ", header=None)
    elif separator.lower == "comma":
        print("it's a comma!")
        data = pd.read_csv(path+data_file, sep=",", header=None)
    else: 
        print("Please enter a valid separator: (space/comma)")
        data = pd.read_csv(path+data_file, sep=",", header=None)
    
    data.columns = ["V1","V2"]

    number_of_edges = len(data)
    weights = np.ones(number_of_edges,)

    list_v1 = data.V1.unique()
    list_v2 = data.V2.unique()

    concatenated = list(list_v1)+list(list_v2)
    nodes = set(concatenated)
    nodes = list(nodes)
    
    number_of_nodes = len(nodes)

    
    data['V3'] = weights.tolist()
    #Name of the layer
    dataset_name = (sys.argv[2])
    print("DATASET: ",dataset_name)
    
    print("Writing output in "+path+dataset_name+".txt    .....")
    with open(path+dataset_name+".txt",'w+') as f:
        f.write(dataset_name+"\n"+str(number_of_nodes)+"\n"+str(number_of_edges))
        for i in range(number_of_nodes):
            f.write('\n%s'%(nodes[i]))
        for i in range(number_of_edges):
            f.write('\n%s,%s,%s'%(data.V1[i], data.V2[i], data.V3[i]))
    f.close()

if __name__== "__main__":
    main()            
