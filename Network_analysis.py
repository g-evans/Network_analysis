#%% Environment initaition
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 10:23:57 2022

@author: guyevans
"""

import csv
import os
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.
import visdcc
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output, State

os.chdir('/Volumes/GE_2022/Network_analysis/')


#%% Ingest data
with open('quakers_nodelist.csv', 'r') as nodecsv: # Open the file
    nodereader = csv.reader(nodecsv) # Read the csv
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][1:]

node_names = [n[0] for n in nodes] # Get a list of only the node names

with open('quakers_edgelist.csv', 'r') as edgecsv: # Open the file
    edgereader = csv.reader(edgecsv) # Read the csv
    edges = [tuple(e) for e in edgereader][1:] # Retrieve the data
 
#%% Initialise graph
G = nx.Graph() # Initialize a Graph object
G.add_nodes_from(node_names) # Add nodes to the Graph
G.add_edges_from(edges) # Add edges to the Graph
print(nx.info(G)) # Print information about the Graph

#%% 
# Create an empty dictionary for each attribute
hist_sig_dict = {}
gender_dict = {}
birth_dict = {}
death_dict = {}
id_dict = {}

for node in nodes: # Loop through the list of nodes, one row at a time
    hist_sig_dict[node[0]] = node[1] # Access the correct item, add it to the corresponding dictionary
    gender_dict[node[0]] = node[2]
    birth_dict[node[0]] = node[3]
    death_dict[node[0]] = node[4]
    id_dict[node[0]] = node[5]

# Add each dictionary as a node attribute to the Graph object
nx.set_node_attributes(G, hist_sig_dict, 'historical_significance')
nx.set_node_attributes(G, gender_dict, 'gender')
nx.set_node_attributes(G, birth_dict, 'birth_year')
nx.set_node_attributes(G, death_dict, 'death_year')
nx.set_node_attributes(G, id_dict, 'sdfb_id')

# Loop through each node, to access and print all the "birth_year" attributes
for n in G.nodes():
    print(n, G.nodes[n]['birth_year'])
    
    
density = nx.density(G)
print("Network density:", density)


#%% Dashboard 
nodes_for_dash = [{'id': i[5],'label': i[0],'shape': 'dot', 'size': 7}
         for i in nodes]
edges_for_dash = [{'id': id_dict.get(i[0])+'__'+id_dict.get(i[1]),'from': id_dict.get(i[0]),'to': id_dict.get(i[1]), 'width': 2}
         for i in edges]
# Create app
app = dash.Dash()

# define layout
app.layout = html.Div([
        visdcc.Network(id= 'net',
                       data = {'nodes': nodes_for_dash, 'edges': edges_for_dash},
                       options = dict(height= '600px', width= '100%')),
        dcc.RadioItems(id='color',
                       options=[{'label':'Red'      ,'value':'#ff0000'},
                                {'label':'Green'    ,'value':'#00ff00'},
                                {'label':'Blue'     ,'value':'#0000ff'} ],
                       value='Red') 
])

# define callback
@app.callback(
    Output('net','options'),
    [Input('color','value')])

def update_network(x):
    
    return {'nodes':{'colour':x}}    

# define main calling
if __name__=='__main__':
    app.run_server(debug=True)
    

















