
// Program to find layer compositions through unweighted and undirected graphs
// May 28, 2018: Edited the last parameter of the NOT List	

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <string>

#include <math.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>
#include <unistd.h>
 
using namespace std;

typedef unsigned long long timestamp_t;

static timestamp_t
get_timestamp ()
{
	struct timeval now;
	gettimeofday (&now, NULL);
	return  now.tv_usec + (timestamp_t)now.tv_sec * 1000000;
}



// A structure to represent an adjacency list node
struct AdjListNode
{
	int dest;
	struct AdjListNode* next;
};
 
// A structure to represent an adjacency list
struct AdjList
{
	int repVertex;	
	struct AdjListNode *head;  // pointer to head node of list
};
 
// A structure to represent a graph. A graph is an array of adjacency lists.
// Size of array will be V (number of vertices in graph)
struct Graph
{
	int V;
	struct AdjList* array;
};
 
// A utility function to create a new adjacency list node
struct AdjListNode* newAdjListNode(int dest)
{
	struct AdjListNode* newNode = (struct AdjListNode*) malloc(sizeof(struct AdjListNode));
	newNode->dest = dest;
	newNode->next = NULL;
	return newNode;
}
 
// A utility function that creates a graph of V vertices
struct Graph* createGraph(int V)
{
	struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
	graph->V = V;
 
	// Create an array of adjacency lists.  Size of array will be V
	graph->array = (struct AdjList*) malloc(V * sizeof(struct AdjList));
 
	// Initialize each adjacency list as empty by making head as NULL
	int i;
	for (i = 0; i < V; ++i)
	{
		graph->array[i].repVertex = -1;
		graph->array[i].head = NULL;
	}
 
	return graph;
}
 
// Adds an edge to an undirected graph
void addEdge(struct Graph* graph, int src, int dest)
{
	int srcIdx, destIdx;
	for (srcIdx = 0; srcIdx < graph->V; ++srcIdx)
	{
		if (src == graph->array[srcIdx].repVertex || (graph->array[srcIdx].repVertex == -1))
			break;
	}

	// vertex encountered for the first time. Add the ID to it
	if (graph->array[srcIdx].repVertex == -1)
			graph->array[srcIdx].repVertex = src;

/*	// each edge represented once
	for (destIdx = 0; destIdx < graph->V; ++destIdx)
	{
		if (dest == graph->array[destIdx].reVertex || (graph->array[srcIdx].reVertex == -1))
			break;
	}

	// vertex encountered for the first time. Add the ID to it
	if (graph->array[destIdx].reVertex == -1)
			graph->array[destIdx].reVertex = dest;
*/

	// Add an edge from src to dest.  A new node is added to the adjacency
	// list of src.  The node is added at the begining
	struct AdjListNode* newNode = newAdjListNode(dest);
	newNode->next = graph->array[srcIdx].head;
	graph->array[srcIdx].head = newNode;
 
/*
	// Since graph is undirected, add an edge from dest to src also
	newNode = newAdjListNode(src);
	newNode->next = graph->array[dest].head;
	graph->array[dest].head = newNode;
*/
}
 
// A utility function to print the adjacenncy list representation of graph
void printGraph(struct Graph* graph)
{
	int v;
	for (v = 0; graph->array[v].repVertex != -1 && v < graph->V; ++v)
	{
		struct AdjListNode* traverse = graph->array[v].head;
		printf("\n Adjacency list of vertex %d\n head ", graph->array[v].repVertex);
		while (traverse)
		{
			printf("-> %d", traverse->dest);
			traverse = traverse->next;
		}
		printf("\n");
	}
}
 
// Driver program to test above functions
int main()
{
	// set up the parameters
	FILE *f = fopen("layerComposerConfiguration", "r");
	char info[500];

	char compositionType[10];

	char layer1[100];
	struct Graph* graph1;
	struct AdjListNode* layer1List;

	// if applicable
	char layer2[100]; 
	struct Graph* graph2;
	struct AdjListNode* layer2List;

	// other DS
	char layerID[2][100], *temp;
	int numberOfEdges[3], found, found2, i, j;
	double edge[3];


	fgets(info, 499, f);

	// the composition Type
	fgets(info, 499, f);
	fgets(compositionType, 9, f);	
	compositionType[strlen(compositionType) - 1] = '\0'; 

	// layer 1 file name
	fgets(info, 499, f);
	fgets(layer1, 99, f);	
	layer1[strlen(layer1) - 1] = '\0';

	if (strcmp(compositionType, "NOT") != 0)
	{
		// layer 2 file name
		fgets(info, 499, f);
		fgets(layer2, 99, f);	
		layer2[strlen(layer2) - 1] = '\0';
		int numberOfLayer2Edges;
	}

	fclose(f);
	// reading and storing the layer 1 graph in the adjacency list

	f = fopen(layer1, "r");
	
	// ID for 1st layer	
		fgets(info, 499, f);
		info[strlen(info) - 1] = '\0';
		sprintf(layerID[0], "%s", info);

	// creating layer 1 graph
	graph1 = createGraph(atoi(fgets(info, 499, f))); // number of vertices

	int vertexSet[graph1->V];
	for (i = 0; i < graph1->V; i++)
		vertexSet[i] = -1;
	
	numberOfEdges[0] = atoi(fgets(info, 499, f));
	
	// storing vertices
	for (i = 0; i < graph1->V; i++)
		vertexSet[i] = atoi(fgets(info, 499, f));
	
	// reading edges
	fgets(info, 499, f);
	while(!feof(f))
	{
		i = 0;
		temp = strtok(info, ",");
		while(temp != NULL)
		{
			edge[i] = atof(temp); // src dest weight	
			temp = strtok(NULL, ",");
			++i;
		}

// new addition - April 17, 2018 for undirected
		if ((int)edge[0] < (int)edge[1])
			addEdge(graph1, (int)edge[0], (int)edge[1]);
		else
			addEdge(graph1, (int)edge[1], (int)edge[0]);

//		addEdge(graph1, (int)edge[1], (int)edge[0]);


/*		// check if vertex is present in vertex set
		for (j = 0; vertexSet[j] != -1; j++)
		{
			if (vertexSet[j] == (int)edge[0])
				break;
		}
		if (vertexSet[j] == -1)
			vertexSet[j] = (int)edge[0];
		
		for (j = 0; vertexSet[j] != -1; j++)
		{
			if (vertexSet[j] == (int)edge[1])
				break;
		}
		if (vertexSet[j] == -1)
			vertexSet[j] = (int)edge[1];

*/	
	
		fgets(info, 499, f);
		info[strlen(info) - 1] = '\0';
	}
	
	fclose(f);

//printGraph(graph1);



	if (strcmp(compositionType, "NOT") != 0)
	{

		// reading and storing the layer 2 graph in the adjacency list
		f = fopen(layer2, "r");

		// ID for 2nd layer	
		fgets(info, 499, f);
		info[strlen(info) - 1] = '\0';
		sprintf(layerID[1], "%s", info);
		
		// creating layer 2 graph
		graph2 = createGraph(atoi(fgets(info, 499, f))); // number of vertices
		
		numberOfEdges[1] = atoi(fgets(info, 499, f));
	
		// dummy for vertices
		for (i = 0; i < graph2->V; i++)
			atoi(fgets(info, 499, f));


		// reading edges
		fgets(info, 499, f);
		while(!feof(f))
		{
			i = 0;
			temp = strtok(info, ",");
			while(temp != NULL)
			{
				edge[i] = atof(temp); // src dest weight	
				temp = strtok(NULL, ",");
				++i;
			}
	
// new addition - April 17, 2018 for undirected
		if ((int)edge[0] < (int)edge[1])
			addEdge(graph2, (int)edge[0], (int)edge[1]);
		else
			addEdge(graph2, (int)edge[1], (int)edge[0]);

		
			fgets(info, 499, f);
			info[strlen(info) - 1] = '\0';
	
		}
		fclose(f);
//		printGraph(graph2);
	}


// start timer: 

	timestamp_t t1 = get_timestamp();

 
	char info1[500];
	if (strcmp(compositionType, "AND") == 0)
	{
		sprintf(info1, "%s_%s_%s", layerID[0], compositionType, layerID[1]);
		f = fopen(info1, "w");

		// adding the verices in the beginning
		for (i = 0; i < graph1->V; i++)
		{
			sprintf(info, "%d\n", vertexSet[i]);
			fputs(info, f);
		}	


		numberOfEdges[2] = 0;

//		printGraph(graph1);
//		printGraph(graph2);

		for (i = 0; graph1->array[i].repVertex != -1 && i < graph1->V; i++)
		{
			layer1List = graph1->array[i].head;
			found = 0;
			// searching for the same head in layer 2 list
			for (j = 0; graph2->array[j].repVertex != -1 && j < graph2->V; j++)
			{
				if (graph2->array[j].repVertex == graph1->array[i].repVertex)
				{
//					cout<<graph1->array[i].repVertex<<"\n";
					found = 1;
					break;
				}
			}
			if (found == 1)
			{
				while (layer1List)
				{
					found = 0;
					layer2List = graph2->array[j].head;
					while (layer2List)
					{
						if (layer1List->dest == layer2List->dest)
						{
							found = 1;
							break;
						}
						layer2List = layer2List->next;
					}
					if (found == 1)
					{
						++numberOfEdges[2];
						sprintf(info, "%d,%d,%f\n", graph1->array[i].repVertex, layer2List->dest, 1.0);
						fputs(info, f);
					}
					layer1List = layer1List->next;
				}
			}
		}
		fclose(f);

		sprintf(info, "sed -i '1s/^/%s_%s_%s\\n%d\\n%d\\n/' %s_%s_%s", layerID[0], compositionType, layerID[1], graph1->V, numberOfEdges[2], layerID[0], compositionType, layerID[1]);
		system(info);

	}
	else if (strcmp(compositionType, "OR") == 0)
	{
		sprintf(info1, "%s_%s_%s", layerID[0], compositionType, layerID[1]);
		f = fopen(info1, "w");
cout<<layerID[0]<<" "<<layerID[1];
		// adding the vertices in the beginning
		for (i = 0; i < graph1->V; i++)
		{
			sprintf(info, "%d\n", vertexSet[i]);
			fputs(info, f);
		}	

		numberOfEdges[2] = 0;

		// matching rep vertices only of both layers and layer 1 complete (A and A int B)
		for (i = 0; graph1->array[i].repVertex != -1 && i < graph1->V; i++)
		{

			layer1List = graph1->array[i].head;
			found = 0;
			// searching for the same head in layer 2 list
			for (j = 0; graph2->array[j].repVertex != -1 && j < graph2->V; j++)
			{
				if (graph2->array[j].repVertex == graph1->array[i].repVertex)
				{
		//	cout<<graph1->array[i].repVertex<<"\n";
					found = 1;
					break;
				}
			}
			if (found == 1)
			{
				// prints all edges for layer 2
				layer2List = graph2->array[j].head;
				while (layer2List)
				{
					++numberOfEdges[2];
					sprintf(info, "%d,%d,%f\n", graph2->array[j].repVertex, layer2List->dest, 1.0);
					fputs(info, f);
					layer2List = layer2List->next;
				}				

				// prints only those edges from layer 1 that are not present in layer 2
				while (layer1List)
				{
					layer2List = graph2->array[j].head;
					found = 0;
					while (layer2List)
					{
						if (layer1List->dest == layer2List->dest)
						{
							found = 1;
							break;
						}
						layer2List = layer2List->next;
					}
					if (found == 0)
					{
						++numberOfEdges[2];
						sprintf(info, "%d,%d,%f\n", graph1->array[i].repVertex, layer1List->dest, 1.0);
						fputs(info, f);
					}
					layer1List = layer1List->next;
				}
			}
			else // lists only in layer 1
			{
				while (layer1List)
				{
					++numberOfEdges[2];
					sprintf(info, "%d,%d,%f\n", graph1->array[i].repVertex, layer1List->dest, 1.0);
					fputs(info, f);
					layer1List = layer1List->next;
				}				
			}
		}

		// Lists only in Layer 2
		for (i = 0; graph2->array[i].repVertex != -1 && i < graph2->V; i++)
		{
			layer2List = graph2->array[i].head;
			found = 0;

			// searching for the same head in layer 1 list
			for (j = 0; graph1->array[j].repVertex != -1 && j < graph1->V; j++)
			{
				if (graph1->array[j].repVertex == graph2->array[i].repVertex)
				{
//					cout<<graph1->array[i].repVertex<<"\n";
					found = 1;
					break;
				}
			}
			if (found == 0)
			{
				while (layer2List)
				{
					++numberOfEdges[2];
					sprintf(info, "%d,%d,%f\n", graph2->array[i].repVertex, layer2List->dest, 1.0);
					fputs(info, f);
					layer2List = layer2List->next;
				}				
			}
		}
		fclose(f);
		
		sprintf(info, "sed -i '1s/^/%s_%s_%s\\n%d\\n%d\\n/' %s_%s_%s", layerID[0], compositionType, layerID[1], graph1->V, numberOfEdges[2], layerID[0], compositionType, layerID[1]);
		system(info);

	}

	else if (strcmp(compositionType, "NOT") == 0)
	{
		// for each find all vertices that are not a part of that list
		sprintf(info1, "%s_%s", compositionType, layerID[0]);

		f = fopen(info1, "w");

		// adding the verices in the beginning
		for (i = 0; i < graph1->V; i++)
		{
			sprintf(info, "%d\n", vertexSet[i]);
			fputs(info, f);
		}	

		numberOfEdges[2] = 0;
		int k;

//		printGraph(graph1);

		for (i = 0; i < graph1->V; i++)
		{
			// searching for the correct location
			found2 = 0;
			for (k = 0; graph1->array[k].repVertex != -1 && k < graph1->V; k++)
			{
				if (vertexSet[i] == graph1->array[k].repVertex)
				{
//					cout<<graph1->array[k].repVertex<<"\n";
					found2 = 1;
					break;
				}
			}

			for (j = i+1; j < graph1->V; j++)
			{
				if (found2 == 1)
				{
					// check whether the edge is present in ith adjacency list
					layer1List = graph1->array[k].head;
					found = 0;
					while (layer1List)
					{
						if (vertexSet[j] == layer1List->dest)
						{
//		cout<<layer1List->dest<<"\n";
							found = 1;
							break;
						}
						layer1List = layer1List->next;
					}

/*				if (found == 0)	// not found in ith, check for jth
				{
					layer1List = graph1->array[j].head;
					found = 0;
					while (layer1List)
					{
						if (vertexSet[i] == layer1List->dest)
						{
							found = 1;
							break;
						}
						layer1List = layer1List->next;
					}
				}
*/
				}
				
				if (found == 0 || found2 == 0) // edge definitely not present
				{
					++numberOfEdges[2];
					sprintf(info, "%d,%d,%f\n", vertexSet[i], vertexSet[j], 1.0);
					fputs(info, f);
				}
			}
		}
		fclose(f);
// May 28, 2018: Edited the last parameter of the NOT List	
		sprintf(info, "sed -i '1s/^/%s_%s\\n%d\\n%d\\n/' %s_%s", compositionType, layerID[0], graph1->V, numberOfEdges[2], compositionType, layerID[0]);
		system(info);

	}

	timestamp_t t2 = get_timestamp();

		cout<<"\n Generation Time : "<<(t2 - t1)/1000000.0L<<" seconds";

		cout<<"\n Average Degree for "<<info1<<" = "<<((double)2 * (double)numberOfEdges[2])/(double)graph1->V;
		cout<<"\n"<<numberOfEdges[2];
		cout<<"\n Average Density for "<<info1<<" = "<<((double)2 * (double)numberOfEdges[2])/((double)graph1->V * (double)(graph1->V - 1))<<"\n";

    return 0;
}

