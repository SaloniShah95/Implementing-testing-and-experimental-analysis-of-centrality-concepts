# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 19:53:01 2020

@author: saloni
"""
import sys
import os.path
import json
import csv
import operator

from finalComponents.centrality_measures import CentralityMeasure

def main():
    with open(sys.argv[1], 'r') as mlnFile:
        
        mlnFilePaths = {}
        #MLN file contaning data set is processed
        for line in mlnFile:
            if line[0] == "#" or line[0] == "/":
                continue
            else:
                layers = line.strip().split("=")
                if layers[0].strip() == 'BASE':
                    break;
                mlnFilePaths[layers[0].strip()] = layers[1].strip()
        BASE_DIR = layers[1].strip()

        for line in mlnFile:
            if line[0] == "#" or line[0] == "/":
                continue
            else:
                layers = line.strip().split("=")
                mlnFilePaths[layers[0].strip()] = BASE_DIR + layers[1].strip()

        if 'HeMLN' in mlnFilePaths:
            mlnStructure = mlnFilePaths['HeMLN'].split(",")

        
        
    with open(sys.argv[2], 'r') as analysisFile:
        count = 0
        flag = 0
        outputDir = {}
            
        lines = (line.rstrip() for line in analysisFile)
        
        for line in lines:
            #comments are ignored
            
            if (line[0] == "#" or line[0]=="/"):
                continue
            else:
                if line[0] == "O":
                    count = count+1
                    temp= line.strip().split("=")
                    outputDirString = temp[1]
                    outputDir[count] = outputDirString.strip()
                    
                else:
                    equation = line.strip().split(",")
                    
                    if "-" in equation[1]:
                        analysisObjective = equation[1].strip().split("-")
                    else:
                        analysisObjective = equation[1].strip()
                    numberOfLayers = len(analysisObjective)
                                        
                    if "-" in equation[1]:
                        layers = set(equation[1].strip().split("-"))
                    else:
                        layers = set(equation[1].strip())
                        #print("***layers", layers)
                        #print("**exp", analysisObjective)
                        numberOfLayers = len(layers)
                        #print("number of layers in analysis: ", numberOfLayers)
                    
                    #checking for algorithm
                    Centrality = equation[0]
                                        
                    #creating a centrality object
                    for i in layers:
                        print("Centrality: ",Centrality)
                        hubs = {}
                        cm = CentralityMeasure(edge_input=mlnFilePaths[i.strip()],centrality=Centrality)
                        C_values = cm.computeCentrality()
                        c_count = 0
                        _sum = 0
                        for key in C_values:
                            c_count += 1
                            _sum += C_values[key]
                        average = _sum/c_count 
                        hubs = dict((k,v) for k,v in C_values.items() if v >= average )
                        x = len(hubs)
                        y = len(C_values)
                        max_V = max(hubs.items(), key=operator.itemgetter(1))[0]
                        min_V = min(hubs.items(), key=operator.itemgetter(1))[0]
                        sum_V = sum(hubs.values())
                        nameOfDataset = cm.dataset
                        
                        #Writing the output to the output directory
                        if count in outputDir.keys():
                            
                            fileString = str(outputDir[count])
                            filename1 = i+"_"+Centrality+".txt"
                            filename2 = i+"_"+Centrality+"_hubs.txt"
                            directory_path = fileString + "\\" + "expression"+str(count)
                            print("writing the output to ",directory_path+filename1)
                            try:
                                os.path.exists(directory_path) 
                            except FileNotFoundError:
                                os.makedirs(directory_path)
                            
                            try:
                                len(C_values)>0
                                with open(directory_path+filename1,'w+') as f:
                                    f.write(nameOfDataset+'\n\n')
                                    for key, value in C_values.items():
                                        f.write('%s\t%s\n'%(key, value))
                                    
                                    '''writer = csv.writer(f)
                                    writer.writerow(nameOfDataset)
                                    for key, value in C_values.items():
                                        writer.writerow([key, value])'''
                                        
                                print("writing the hubs to ",directory_path+filename2)
                                with open(directory_path+filename2,'w+') as f2:
                                    f2.write(nameOfDataset)
                                    f2.write('\nx = Number of hubs'+
                                             '\ny = Total number of nodes'+
                                             '\nx/y = %s/%s'%(x,y)+
                                             '\nAverage Value, Min Value, Max Value, Sum'+
                                             '\n%s, %s, %s, %s\n\n'%(average,min_V,max_V,sum_V))
                                    for key, value in hubs.items():
                                        f2.write('%s %s\n'%(key, value))
                            except:
                                print("Error! no centrality results found")
                            
                            
                            
                            
                
                    
            
            
if __name__== "__main__":
    main()            