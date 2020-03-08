# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 19:53:01 2020

@author: saloni
"""
import sys
import os.path
import json
import csv

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
                        
                        cm = CentralityMeasure(edge_input=mlnFilePaths[i.strip()],centrality=Centrality)
                        C_values = cm.computeCentrality()
                        
                        
                       
                        #Writing the output to the output directory
                        if count in outputDir.keys():
                           
                            fileString = str(outputDir[count])
                            filename = i+"_"+Centrality+".csv"
                            directory_path = fileString + "\\" + "expression"+str(count)
                            print("writing the output to ",directory_path+filename)
                            try:
                                os.path.exists(directory_path) 
                            except FileNotFoundError:
                                os.makedirs(directory_path)
                            
                            try:
                                len(C_values)>0
                                with open(directory_path+filename,'w+') as f:
                                    writer = csv.writer(f)
                                    for key, value in C_values.items():
                                        writer.writerow([key, value])
                            except:
                                print("Error! no centrality results found")
                
                    
            
            
if __name__== "__main__":
    main()            