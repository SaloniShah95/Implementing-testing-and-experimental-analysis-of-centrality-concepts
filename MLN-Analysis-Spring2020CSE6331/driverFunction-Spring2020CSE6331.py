import sys
import os.path
import operator
#import different components for computation
from finalComponents.densityWeightedBipartiteGraphGenerator import *
from finalComponents.participatingHubsBipartiteGraphGenerator import *
from finalComponents.edgeWeightBipartiteGaphGenerator import *
from finalComponents.maximalWeightedMatchingGenerator import *
from finalComponents.maximalWeightedBipartiteCouplingGenerator import *
from finalComponents.maximalWeightedMatchingWithTiesGenerator import *
from finalComponents.maximalWeightedPerfectMatchingGenerator import *
from finalComponents.edgeFractionWeightBipartiteGraphGenerator import *
from finalComponents.participationWeightedBipartiteGraphGenerator import *
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

        
        #for i in mlnFilePaths:
        #    print(i, mlnFilePaths[i])
            
    with open(sys.argv[2], 'r') as analysisFile:
        count = 1
        
        outputDir = {}
        for line in analysisFile:
            #comments are ignored
            if (line[0] == "#" or line[0]=="/"):
                continue
            else:
                if line[0] == "O":
                    temp= line.strip().split("=")
                    #print(temp)
                    outputDirString = temp[1]
                    outputDir[count] = outputDirString.strip()
                    #print(outputDir)
                elif line[0] == "S":
                    equation = line.strip().split(",")
                    
                    if "-" in equation[2]:
                        analysisObjective = equation[2].strip().split("-")
                    else:
                        analysisObjective = equation[2].strip()
                    numberOfLayers = len(analysisObjective)
                                        
                    if "-" in equation[2]:
                        layers = set(equation[2].strip().split("-"))
                    else:
                        layers = set(equation[2].strip())
                        #print("***layers", layers)
                        #print("**exp", analysisObjective)
                        numberOfLayers = len(layers)
                        #print("number of layers in analysis: ", numberOfLayers)
                    
                    #checking for algorithm
                    Centrality = equation[1]
                                        
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
                                             '\nx/y = %s\t/%s'%(x,y)+
                                             '\nAverage Value, Min Value, Max Value, Sum'+
                                             '\n%s, %s, %s, %s\n\n'%(average,min_V,max_V,sum_V))
                                    for key, value in hubs.items():
                                        f2.write('%s %s\n'%(key, value))
                            except:
                                print("Error! no centrality results found")
                    
                else:
                    equation = line.strip().split(",")
                    #print(equation)
                    #print(equation[3].strip().split("-"))
                    analysisObjective = equation[3].strip().split("-")#[char for char in (equation[3])]
                    numberOfBipartiteLayers = len(analysisObjective)-1
                    layers = set(equation[3].strip().split("-"))
                    print("***layers", layers)
                    print("**exp", analysisObjective)
                    print("**number of bipartite", numberOfBipartiteLayers)
                    numberOfLayers = len(layers)
                    print("number of layers in analysis: ", numberOfLayers)
                    #---------------------------------------------------------------------------
                    #computing comunities in the multilayer graph
                    communityDetectionAlgo = equation[0].lower()
                    for i in range(0, numberOfLayers):
                        communityFileName = analysisObjective[i]+communityDetectionAlgo
                        print("community File Name: ", communityFileName)
                        if communityDetectionAlgo == "louvain":
                            print("louvain")
                            fileString = BASE_DIR + "Layers\\communityFiles\\"+communityFileName+".clu"
                            print(fileString)
                            if  os.path.exists(fileString):
                                mlnFilePaths[communityFileName] = fileString
                            else:
                                print("Call Louvain")
                        elif communityDetectionAlgo == "infomap":
                            print("infomap")
                            fileString = BASE_DIR + "Layers\\communityFiles\\"+communityFileName+".clu"
                            if os.path.exists(fileString):
                                mlnFilePaths[communityFileName] = fileString
                            else:
                                #call informap with mlnFilePath[mlnstructure[i]]
                                print("Call Infomap")
                        else:
                            print("Please enter the correct community detection algorithm")
                    #---------------------------------------------------------------------------
                    #generating bipartite graphs
                    weightMetrics =equation[1].lower()
                    for i in range(0, numberOfBipartiteLayers):
                        layer1 = mlnFilePaths[analysisObjective[i]]
                        layer2 = mlnFilePaths[analysisObjective[i+1]]
                        interlayer12 = mlnFilePaths[analysisObjective[i]+analysisObjective[i+1]]
                        layer1CommFile = mlnFilePaths[analysisObjective[i]+communityDetectionAlgo]
                        layer2CommFile = mlnFilePaths[analysisObjective[i+1] + communityDetectionAlgo]
                        #print("**OD = ",outputDir)
                        if count in outputDir.keys():
                            fileString = str(outputDir[count])
                            resultFileStringwe = fileString + "/" + "expression"+str(count)+ "/"+"bipartiteFiles/" + analysisObjective[i]+analysisObjective[i+1]+"_"+"we.bg"
                        else:
                            resultFileStringwe = "expression"+str(count)+"/"+"bipartiteFiles/"+analysisObjective[i]+analysisObjective[i+1]+"_"+"we.bg"
                        #print("** exp path", resultFileStringwe)
                        if not os.path.exists(resultFileStringwe):
                            edgeWeightBipartiteGraphGenerator(layer1CommFile,
                                                      layer2CommFile,
                                                      interlayer12,
                                                      resultFileStringwe)
                        mlnFilePaths[("we", analysisObjective[i]+analysisObjective[i+1])] = resultFileStringwe

                        if weightMetrics == "we":
                            print("Simpler bipartite graph generator")

                        elif weightMetrics == "wf":
                            if count in outputDir.keys():
                                fileString = outputDir[count]
                                resultFileStringwf = fileString + "/" + "expression"+str(count)+ "/"+"bipartiteFiles/" + analysisObjective[i]+analysisObjective[i+1]+"_"+ "wf.bg"
                            else:
                                resultFileStringwf = "expression" +str(count) + "/" + "bipartiteFiles/" + analysisObjective[
                                    i] + analysisObjective[i + 1] + "_" + "wf.bg"

                            print("edge fraction")
                            layer1CommunityFile = mlnFilePaths[analysisObjective[i]+communityDetectionAlgo]
                            layer2CommunityFile = mlnFilePaths[analysisObjective[i+1] + communityDetectionAlgo]
                            simpleEdgeBipartiteFile = mlnFilePaths[("we", analysisObjective[i]+analysisObjective[i+1])]


                            if not os.path.exists(resultFileStringwf):
                                edgeFractionWeightedBipartiteGraphGenerator(layer1CommunityFile,
                                                                            layer2CommunityFile,
                                                                            simpleEdgeBipartiteFile,
                                                                            resultFileStringwf)
                            mlnFilePaths[(weightMetrics, analysisObjective[i] + analysisObjective[i + 1])] = resultFileStringwf


                        elif weightMetrics == "wd":
                            if count in outputDir.keys():
                                fileString = outputDir[count]
                                resultFileStringwd = fileString + "/" + "expression"+str(count)+ "/"+"bipartiteFiles/" + analysisObjective[i]+analysisObjective[i+1]+"_"+ "wd.bg"
                            else:
                                resultFileStringwd = "expression" + str(count) + "/" +"bipartiteFiles/" + analysisObjective[i] + analysisObjective[
                                    i + 1] + "_" + "wd.bg"
                            print("density bipartite graph generator")
                            simpleBipartiteGraph = mlnFilePaths[("we", analysisObjective[i]+analysisObjective[i+1])]

                            layer1CommFile = mlnFilePaths[analysisObjective[i] + communityDetectionAlgo]
                            layer2CommFile = mlnFilePaths[analysisObjective[i + 1] + communityDetectionAlgo]
                            if not os.path.exists(resultFileStringwd):
                                densityWeightedBipartiteGraphGenerator(layer1CommFile,
                                                                    layer2CommFile,
                                                                     layer1,
                                                                     layer2,
                                                                     simpleBipartiteGraph,
                                                                     resultFileStringwd)
                            mlnFilePaths[(weightMetrics,analysisObjective[i] + analysisObjective[i + 1] )] = resultFileStringwd

                        elif weightMetrics == "wp":
                            if count in outputDir.keys():
                                fileString = outputDir[count]
                                resultFileStringwp = fileString + "/" + "expression"+str(count)+ "/"+"bipartiteFiles/" + analysisObjective[i]+analysisObjective[i+1]+"_"+ "wp.bg"
                            else:
                                resultFileStringwp = "expression" + str(count) + "/" + "bipartiteFiles/" + analysisObjective[
                                    i] + analysisObjective[i + 1] + "_" + "wp.bg"
                            print("Simpler bipartite graph generator")
                            simpleBipartiteGraph = mlnFilePaths[("we", analysisObjective[i] + analysisObjective[i + 1])]
                            layer1CommFile = mlnFilePaths[analysisObjective[i] + communityDetectionAlgo]
                            layer2CommFile = mlnFilePaths[analysisObjective[i + 1] + communityDetectionAlgo]
                            if not os.path.exists(resultFileStringwp):
                                participationBipartiteGraphGenerator(layer1CommFile,
                                                                         layer2CommFile,
                                                                         layer1,
                                                                         layer2,
                                                                         interlayer12,
                                                                         simpleBipartiteGraph,
                                                                         resultFileStringwp)
                            mlnFilePaths[(weightMetrics,analysisObjective[i] + analysisObjective[i + 1] )] = resultFileStringwp


                        elif weightMetrics == "wh":
                            if count in outputDir.keys():
                                fileString = outputDir[count]
                                resultFileStringwh = fileString + "/" + "expression"+str(count)+ "/"+"bipartiteFiles/" + analysisObjective[i]+analysisObjective[i+1]+"_"+ "wh.bg"
                            else:
                                resultFileStringwh = "expression"+str(count)+"/"+"bipartiteFiles/"+analysisObjective[i]+analysisObjective[i+1]+"_"+"wh.bg"
                            simpleBipartiteGraph = mlnFilePaths[("we", analysisObjective[i] + analysisObjective[i + 1])]
                            layer1CommFile = mlnFilePaths[analysisObjective[i] + communityDetectionAlgo]
                            layer2CommFile = mlnFilePaths[analysisObjective[i + 1] + communityDetectionAlgo]
                            if not os.path.exists(resultFileStringwh):
                                participatingHubsBipartiteGraphGenerator(layer1CommFile,
                                                                         layer2CommFile,
                                                                         layer1,
                                                                         layer2,
                                                                         interlayer12,
                                                                         simpleBipartiteGraph,
                                                                         resultFileStringwh)
                            mlnFilePaths[(weightMetrics,analysisObjective[i] + analysisObjective[i + 1] )] = resultFileStringwh

                        else:
                            print("Please enter the correct weight metrics")
                    #--------------------------------------------------------------------------
                    #applying matching algorithm
                    matchingAlgorithm = equation[2].lower()
                    processedLayers = [analysisObjective[0]]
                    processedLayersFilePath = {}
                    for i in range(0, numberOfBipartiteLayers):
                        if matchingAlgorithm == "mwm":
                            print("MWM")
                            if i != 0:# and analysisObjective[i] in processedLayers:
                                string = ""
                                for j in range(0, i):
                                    string += analysisObjective[j]
                                if i == numberOfBipartiteLayers -1:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwm = fileString + "/" + "expression"+str(count)+"/"+"MWM/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwm"
                                    else:

                                        resultFileStringmwm = "expression"+str(count)+"/"+"MWM/FinalResults/"  + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwm"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwm = fileString + "/" + "expression"+str(count)+"/"+ "MWM/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwm"
                                    else:
                                        resultFileStringmwm = "expression"+str(count)+"/"+"MWM/" +string+analysisObjective[i] +\
                                                       analysisObjective[i + 1] +\
                                                        "_"+weightMetrics+\
                                                       "_" + communityDetectionAlgo+\
                                                       ".mwm"
                                if not os.path.exists(resultFileStringmwm):
                                    print("processed layers: ", processedLayers)
                                    if analysisObjective[i+1] in processedLayers: # check if both layers have been processed
                                        print("same layer", analysisObjective[i+1])
                                        for j in range(0, i-1):
                                            if analysisObjective[j] == analysisObjective[i+1]:
                                                break
                                        maximalWeightedMatchingExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwm, j)
                                    else:
                                        maximalWeightedMatchingExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwm, -1)
                                mlnFilePaths[(
                                matchingAlgorithm, analysisObjective[i] + analysisObjective[i + 1])] = resultFileStringmwm

                            else:
                                if i == numberOfBipartiteLayers -1:
                                    string = ""
                                    for j in range(0, i):
                                        string += analysisObjective[j]
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwm = fileString + "/" + "expression"+str(count)+"/" +"MWM/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwm"
                                    else:
                                        resultFileStringmwm = "expression"+str(count)+"/"+"MWM/FinalResults/" + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwm"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwm = fileString + "/" + "expression"+str(count)+"/" +"MWM/FinalResults/" + \
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwm"
                                    else:
                                        resultFileStringmwm = "expression"+str(count)+"/"+"MWM/"+analysisObjective[i]+\
                                                       analysisObjective[i+1]+ \
                                                       "_" + weightMetrics + \
                                                       "_" + communityDetectionAlgo + \
                                                       ".mwm"
                                if not os.path.exists(resultFileStringmwm):
                                    maximalWeightedMatchingGenerator(mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                    resultFileStringmwm)
                                mlnFilePaths[(matchingAlgorithm, analysisObjective[i]+analysisObjective[i+1])] = resultFileStringmwm
                            processedLayers.append(analysisObjective[i+1])
                            processedLayersFilePath[analysisObjective[i+1]] = resultFileStringmwm

                        elif matchingAlgorithm == "mwbc":
                            print("MWBC")
                            if i != 0: #analysisObjective[i] in processedLayers:
                                string = ""
                                for j in range(0, i):
                                    string += analysisObjective[j]
                                if i == numberOfBipartiteLayers -1:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwbc = fileString + "/" + "expression"+str(count)+"/" +"MWBC/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwbc"
                                    else:

                                        resultFileStringmwbc = "expression"+str(count)+"/"+"MWBC/FinalResults/"  + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwbc"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwbc = fileString + "/" + "expression"+str(count)+"/" + "MWBC/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwbc"
                                    else:
                                        resultFileStringmwbc = "expression"+str(count)+"/"+"MWBC/" +string+analysisObjective[i] +\
                                                       analysisObjective[i + 1] +\
                                                        "_"+weightMetrics+\
                                                       "_" + communityDetectionAlgo+\
                                                       ".mwbc"
                                if not os.path.exists(resultFileStringmwbc):
                                    print("processed layers: ", processedLayers)
                                    if analysisObjective[i+1] in processedLayers: # check if both layers have been processed
                                        print("same layer", analysisObjective[i+1])
                                        for j in range(0, i-1):
                                            if analysisObjective[j] == analysisObjective[i+1]:
                                                break
                                        maximumWeightBipartiteCouplingExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwbc, j)
                                    else:
                                        maximumWeightBipartiteCouplingExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwbc, -1)
                                mlnFilePaths[(
                                matchingAlgorithm, analysisObjective[i] + analysisObjective[i + 1])] = resultFileStringmwbc

                            else:
                                if i == numberOfBipartiteLayers -1:
                                    string = ""
                                    for j in range(0, i):
                                        string += analysisObjective[j]
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwbc = fileString + "/" + "expression"+str(count)+"/" +"MWBC/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwbc"
                                    else:
                                        resultFileStringmwbc = "expression"+str(count)+"/"+"MWBC/FinalResults/" + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwbc"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwbc = fileString + "/" + "expression"+str(count)+"/" +"MWBC/FinalResults/" + \
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwbc"
                                    else:
                                        resultFileStringmwbc = "expression"+str(count)+"/"+"MWBC/"+analysisObjective[i]+\
                                                       analysisObjective[i+1]+ \
                                                       "_" + weightMetrics + \
                                                       "_" + communityDetectionAlgo + \
                                                       ".mwbc"
                                if not os.path.exists(resultFileStringmwbc):
                                    maximumWeightBipartiteCouplingGenerator(mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                    resultFileStringmwbc)
                                mlnFilePaths[(matchingAlgorithm, analysisObjective[i]+analysisObjective[i+1])] = resultFileStringmwbc
                            processedLayers.append(analysisObjective[i+1])
                            processedLayersFilePath[analysisObjective[i+1]] = resultFileStringmwbc
                            #print(processedLayers)
                        elif matchingAlgorithm == "mwpm":
                            print("MWPM")
                            if i != 0: #analysisObjective[i] in processedLayers:
                                string = ""
                                for j in range(0, i):
                                    string += analysisObjective[j]
                                if i == numberOfBipartiteLayers -1:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwpm = fileString + "/" + "expression"+str(count)+"/" +"MWPM/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwpm"
                                    else:

                                        resultFileStringmwpm = "expression"+str(count)+"/"+"MWPM/FinalResults/"  + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwpm"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwpm = fileString + "/" + "expression"+str(count)+"/" + "MWPM/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwpm"
                                    else:
                                        resultFileStringmwpm = "expression"+str(count)+"/"+"MWPM/" +string+analysisObjective[i] +\
                                                       analysisObjective[i + 1] +\
                                                        "_"+weightMetrics+\
                                                       "_" + communityDetectionAlgo+\
                                                       ".mwpm"
                                if not os.path.exists(resultFileStringmwpm):
                                    print("processed layers: ", processedLayers)
                                    if analysisObjective[i+1] in processedLayers: # check if both layers have been processed
                                        print("same layer", analysisObjective[i+1])
                                        for j in range(0, i-1):
                                            if analysisObjective[j] == analysisObjective[i+1]:
                                                break
                                        maximalWeightedPerfectMatchingExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwpm, j)
                                    else:
                                        maximalWeightedPerfectMatchingExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwpm, -1)
                                mlnFilePaths[(
                                matchingAlgorithm, analysisObjective[i] + analysisObjective[i + 1])] = resultFileStringmwpm

                            else:
                                if i == numberOfBipartiteLayers -1:
                                    string = ""
                                    for j in range(0, i):
                                        string += analysisObjective[j]
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwpm = fileString + "/" + "expression"+str(count)+"/" +"MWPM/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwpm"
                                    else:
                                        resultFileStringmwpm = "expression"+str(count)+"/"+"MWPM/FinalResults/" + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwpm"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwpm = fileString + "/" + "expression"+str(count)+"/" +"MWPM/FinalResults/" + \
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwpm"
                                    else:
                                        resultFileStringmwpm = "expression"+str(count)+"/"+"MWPM/"+analysisObjective[i]+\
                                                       analysisObjective[i+1]+ \
                                                       "_" + weightMetrics + \
                                                       "_" + communityDetectionAlgo + \
                                                       ".mwpm"
                                if not os.path.exists(resultFileStringmwpm):
                                    maximalWeightedPerfectMatchingGenerator(mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                    resultFileStringmwpm)
                                mlnFilePaths[(matchingAlgorithm, analysisObjective[i]+analysisObjective[i+1])] = resultFileStringmwpm
                            processedLayers.append(analysisObjective[i+1])
                            processedLayersFilePath[analysisObjective[i+1]] = resultFileStringmwpm
                            #print(processedLayers)
                        elif matchingAlgorithm == "mwmt":
                            print("MWMT")
                            if i != 0: #analysisObjective[i] in processedLayers:
                                string = ""
                                for j in range(0, i):
                                    string += analysisObjective[j]
                                if i == numberOfBipartiteLayers -1:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwmt = fileString + "/" + "expression"+str(count)+"/" +"MWMT/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwmt"
                                    else:

                                        resultFileStringmwmt = "expression"+str(count)+"/"+"MWMT/FinalResults/"  + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwmt"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwmt = fileString + "/" + "expression"+str(count)+"/" + "MWMT/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwmt"
                                    else:
                                        resultFileStringmwmt = "expression"+str(count)+"/"+"MWMT/" +string+analysisObjective[i] +\
                                                       analysisObjective[i + 1] +\
                                                        "_"+weightMetrics+\
                                                       "_" + communityDetectionAlgo+\
                                                       ".mwmt"
                                if not os.path.exists(resultFileStringmwmt):
                                    print("processed layers: ", processedLayers)
                                    if analysisObjective[i+1] in processedLayers: # check if both layers have been processed
                                        print("same layer", analysisObjective[i+1])
                                        for j in range(0, i-1):
                                            if analysisObjective[j] == analysisObjective[i+1]:
                                                break
                                        maximalWeightedMatchingWithTiesExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwmt, j)
                                    else:
                                        maximalWeightedMatchingWithTiesExtender(processedLayersFilePath[analysisObjective[i]],
                                                                    mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                   resultFileStringmwmt, -1)
                                mlnFilePaths[(
                                matchingAlgorithm, analysisObjective[i] + analysisObjective[i + 1])] = resultFileStringmwmt

                            else:
                                if i == numberOfBipartiteLayers -1:
                                    string = ""
                                    for j in range(0, i):
                                        string += analysisObjective[j]
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwmt = fileString + "/" + "expression"+str(count)+"/" +"MWMT/FinalResults/" + \
                                                          string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwmt"
                                    else:
                                        resultFileStringmwmt = "expression"+str(count)+"/"+"MWMT/FinalResults/" + \
                                                           string+\
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwmt"
                                else:
                                    if count in outputDir.keys():
                                        fileString = str(outputDir[count])
                                        resultFileStringmwmt = fileString + "/" + "expression"+str(count)+"/" +"MWMT/FinalResults/" + \
                                                          analysisObjective[i] \
                                                          + analysisObjective[i + 1] + \
                                                          "_" + weightMetrics + \
                                                          "_" + communityDetectionAlgo + \
                                                          "_" + ".mwmt"
                                    else:
                                        resultFileStringmwmt = "expression"+str(count)+"/"+"MWMT/"+analysisObjective[i]+\
                                                       analysisObjective[i+1]+ \
                                                       "_" + weightMetrics + \
                                                       "_" + communityDetectionAlgo + \
                                                       ".mwmt"
                                if not os.path.exists(resultFileStringmwmt):
                                    maximalWeightedMatchingWithTiesGenerator(mlnFilePaths[(weightMetrics,analysisObjective[i]+analysisObjective[i+1])],
                                                                    resultFileStringmwmt)
                                mlnFilePaths[(matchingAlgorithm, analysisObjective[i]+analysisObjective[i+1])] = resultFileStringmwmt
                            processedLayers.append(analysisObjective[i+1])
                            processedLayersFilePath[analysisObjective[i+1]] = resultFileStringmwmt
                            #print(processedLayers)
                        else:
                            print("Please enter the correct matching algorithm")
                    count += 1


#result <10(A),20(D),30(M); pathname of bipartite file of 10-20(A-D), pathname of bipartite file of 20-30(D-M)>


if __name__== "__main__":
    main()
