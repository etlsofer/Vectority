# Vectority

##Finding flow circuits in the velocity vector field
#introduction
To be able to work with Open Source it is necessary to know the following data for the images taken: the time between the images, the window size, scale, width.
The open-source I use is written to the velocity vector data file as follows: The location of the coordinates (X, Y) of each vector and its length when the length is subject to the width parameter (ie divided by it) and the positive direction is to the positive axis (two-dimensional right axis system)
In this work, I will suggest a method that uses the above file to find flow circuits.
Brief method:
After reading the file containing the coordinates and directions of the vectors, I produce a graph which is the above vectors. That is, the direction of the vector in the direction of the arc and at both ends, some nodes are the nodes in the graph.
I then set the Dist parameter which is the minimum distance between nodes. Any node that is closer than the above distance to another node is merged and becomes one node whose incoming and outgoing arcs become the same node (and so all the nodes entering the above nodes enter the same node).
In the end, a graph is obtained. In the above graph, I check for each node in how many circles it participates. After I finish going I return all the nodes that participate too many times. When it means shooting from time to time is the matter that my data structure investigates.
Parameters
A minimum number of nodes - if I returned each node participating in the circle I could get a huge number of nodes. This makes it very difficult to investigate the circuits. Besides, not every circle closing in a graph is necessarily a flow vortex, for this purpose a large number of circles must be identified in the same area so I am looking for the same node to appear in more than one circle. To find the above nodes I set a minimum number of nodes that the algorithm will return. This is at the discretion of the user.
Finding the above number increases the complexity of the algorithm since it tries to calculate the size of the counter for each node.
Minimum distance - the minimum distance between nodes from which all nodes at a small distance will be merged. The optimal size for this parameter should be investigated and efficiency and correctness considerations should be used.
Widtm - This is the order of magnitude of the vector in the coordinate system (due to the use of open source there is no point in expanding on it here).
