# Discrete-Optimization
This repository contains a variety of algorithms to solve descrete optimization problems

Ford Fulkerson Algorithm can be used to solve maximum flow problems in graph theory. It's an iterative method through which we tend to traverse the graph (network) nodes to find a path from the source node to the sink node. Afterward, we should find the minimum capacity along this path and subtract it from the capacity of all the edges of the path. This minimum flow should be held on one hand as the maximum flow of the network to be updated in the next iteration by addition. To put it another way, it means that if you have calculated the min flow of the first path as mf1 and the second path as mf2, and you have visited the sink node, the maximum flow of the network is mf1+mf2.

In this algorithm, you can choose between DFS or BFS traversal methods. If you choose BFS, the algorithm tends to consider the node that has stayed in the queue the longest. On the other hand, if you select the DFS method, the algorithm will consider the node added last.

About the time the original ford-fulkerson algorithm takes to solve the maximum flow problem: each iteration of the algorithm icludes finding a path, which refers to "Reachability" problem. Finding a path takes O(n^2) time. On the other hand, this algorithm comprises nC iterations in the worst case scenario where "n" is number of the nodes (except the source and the sink) and "C" is the maximum capacity of edges. Therefore, it takes the algorithm O(Cn^3) to solve the max flow problem.

The maximum flow in the example graph is 15.0
