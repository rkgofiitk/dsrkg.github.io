## Readme for Graph Algorithms 

The current folder contains one folder that contains all files.The folder contains four files:
- graph_core.py: Python code for graph operations.
- flsk_app_backend.py: Python code for application backend
- graph.js: Script file containing functions for animation
- index.html: It is the HTML file that triggers the script for the front end

The file <tt>graph_core.py</tt> handles the random generation of an undirected graph. It takes three input parameters to create a graph: the number of nodes, the maximum number of connections per node, and the average connections per node. Once specified, it generates a graph by adding nodes and edges. Edges are assigned a weight randomly. However, DFS and BFS do not use edge weights. We created a generalized edge-weighted graph that can also be used for shortest-path computation. 

The file <tt>flask_app_backend.py</tt> contains the route to the frontend. We have a route for graph generation, DFS, BFS, and graph reset. 
