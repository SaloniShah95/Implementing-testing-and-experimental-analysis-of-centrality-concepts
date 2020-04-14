# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 02:41:06 2020

@author: salon
"""
import sys
import matplotlib.pyplot as plt

def parse_file(filename):
        with open(filename) as f:
            content = f.readlines()
            #Remove `\n` at the end of each line
            content = [x.strip() for x in content] 
            f.close()
        return content
    
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3
   
#def main():
#    between_file = (sys.argv[1])
#    eigen_file = (sys.argv[2])
#    close_file = (sys.argv[3])
#    degree_file = (sys.argv[4])
between_file = "Facebook_output\\expression1F414_Between_hubs.txt"
eigen_file = ("Facebook_output\\expression1F414_Eigen_hubs.txt")
close_file = ("Facebook_output\\expression1F414_Close_hubs.txt")
degree_file = ("Facebook_output\\expression1F414_Degree_hubs.txt")

between_hubs_nodes=[]
between_hubs_vals=[]
eigen_hubs_nodes=[]
eigen_hubs_vals=[]
close_hubs_nodes=[]
close_hubs_vals=[]
degree_hubs_nodes=[]
degree_hubs_vals=[]
    
path = "S:\\course work\\Adv topics in databases\\gitrepo\\CSE6331_project\\MLN-Analysis-Spring2020CSE6331\\IMDB-Top-500-Actors\\Analysis\\"
between_content = parse_file(path+between_file)
eigen_content = parse_file(path+eigen_file)
close_content = parse_file(path+close_file)
degree_content = parse_file(path+degree_file)

n_bhubs = between_content[3].split('=')[1].split('/')[0]
n_ehubs = eigen_content[3].split('=')[1].split('/')[0]
n_chubs = close_content[3].split('=')[1].split('/')[0]
n_dhubs = degree_content[3].split('=')[1].split('/')[0]

for i in range(7,int(n_bhubs)):
        a = between_content[i].split()
        between_hubs_nodes.append(between_content[i].split()[0])
        between_hubs_vals.append(between_content[i].split()[1])

for i in range(7,int(n_ehubs)):
        a = eigen_content[i].split()
        eigen_hubs_nodes.append(eigen_content[i].split()[0])
        eigen_hubs_vals.append(eigen_content[i].split()[1])

for i in range(7,int(n_chubs)):
        a = close_content[i].split()
        close_hubs_nodes.append(close_content[i].split()[0])
        close_hubs_vals.append(close_content[i].split()[1])

for i in range(7,int(n_dhubs)):
        a = degree_content[i].split()
        degree_hubs_nodes.append(degree_content[i].split()[0])
        degree_hubs_vals.append(degree_content[i].split()[1])

plt.plot(between_hubs_nodes,between_hubs_vals,color='skyblue')     
plt.plot(eigen_hubs_nodes,eigen_hubs_vals,color='red')     
plt.plot(close_hubs_nodes,close_hubs_vals,color='green')     
plt.plot(degree_hubs_vals,degree_hubs_vals,color='yellow')   
        
#intersection with betweenness
be = intersection(between_hubs_nodes,eigen_hubs_nodes)
bc = intersection(between_hubs_nodes,close_hubs_nodes)
bd = intersection(between_hubs_nodes,degree_hubs_nodes)

#intersection with closeness
ce = intersection(close_hubs_nodes,eigen_hubs_nodes)
cb = intersection(close_hubs_nodes,between_hubs_nodes)

cd = intersection(close_hubs_nodes,degree_hubs_nodes)
cde = intersection(cd,eigen_hubs_nodes)
bde = intersection(bd,eigen_hubs_nodes)
bce = intersection(cb,eigen_hubs_nodes)
bcd = intersection(bc,degree_hubs_nodes)


#intersection with closeness
ec = intersection(close_hubs_nodes,eigen_hubs_nodes)
eb = intersection(eigen_hubs_nodes,between_hubs_nodes)
ed = intersection(eigen_hubs_nodes,degree_hubs_nodes)

bcde = intersection(bc,ed)        

'''
if __name__== "__main__":
    print("Please enter the file names in the following format: <between_hubs> <eigen_hubs> <close_hubs> <degree_hubs>")
    print("path set: S:\course work\Adv topics in databases\gitrepo\CSE6331_project\MLN-Analysis-Spring2020CSE6331\IMDB-Top-500-Actors\Analysis")
    main()'''   