'''
Name: Mitchell Marino
Date: 2018-02-20
Program: Data_Structures.py
Description: Includes my implementation of Graph and Node data structures
             which are used to determine shortest path. The graph data structure
             also includes my implementations of Depth First Search and Djikstra's 
             Algorithm which play cruical parts in determining connectivity and shortest
             path in my program.

PLEASE NOTE: Nodes are analogous to vertices in my implementation.
'''

#Imports
import geopy.distance as geopy
import heapq

class Graph(object):
    '''My graph implementation'''

    def __init__(self, start_street, start_node, end_street, end_node):
        ''' 
        Initialization for the graph.
        -----------------------------
        Inputs:
            - start_treet --> Name of starting street.
            - start_node --> Node that representslocation of starting address.
            - end_street --> Name of ending street
            - end_node --> Node that represents location of ending address.
        '''
        self.node_list = {}                 #A dictionary of nodes. (Intersections)
        self.start_street = start_street    #Initialize start street.
        self.end_street = end_street        #Initialize end street.
        self.start_node = start_node        #Initialize start node.
        self.end_node = end_node            #Initialize end node.

    def add_node(self, osm_id, latitude, longitude):
        ''' 
        Adds a node to the graph.
        --------------------------
        Inputs:
            - osm_id --> The unique OSM (Open Street Map) ID of the intersection.
                         Use 0 or negative numbers for custom nodes.
                         Note for my implementation:
                            Start node id = -1
                            End node id = -2
            - latitude  --> Latitude coordinate of the intersection.
            - longitude --> Longitude coordinate of the intersection.
        '''
        #Create a new node.
        node = Node(osm_id, latitude, longitude)
        #Add a node list to dictionary with the OSM id as a key.
        #This enables very fast look-up time for a node.
        self.node_list[osm_id] = node

    def add_edge(self, start_id, end_id, way):
        '''
        Adds an edge between two nodes in the graph.
        --------------------------------------------
        Inputs
            - start_id --> The id of the starting node.
            - end_id   --> The id of the ending node.
            - way --> A tuple of (edge_length, street_name)

        Note: way is the OSM terminology for a street.
        '''
        #Index the node with id of start id.
        node = self.node_list[start_id]
        #Add an edge from the start node to the end node with the properties of way.
        node.add_edge(self.node_list[end_id], way)
    
    def add_critical_edge(self, start_id, way):
        '''
        Takes a way with a street name that is the same as that of the start or end node.
        In this case, there are two conditions:
        -------------------------------------------------------------
        Condition 1: Street name is same as start node's street name.
        Action: Create edge from start node to current node.
        -------------------------------------------------------------
        Condition 2: Street name is same as end node's street name.
        Action: Create edge from current node to end node.
        -------------------------------------------------------------
        '''
        #Index the node with id of start id.
        node = self.node_list[start_id]
    
        #Cond1: Street name is same as start node's street name:
        if (way[1].lower() == self.start_street.lower()):
            #Calc distance in meters between them.
            distance = longlat_to_metres(node, self.start_node)
            #Then add an edge from start node to node with start_id.
            self.start_node.add_edge(self.node_list[start_id], (distance, way[1]))
    
        #Cond2: Street name is same as end node's street name.
        if (way[1].lower() == self.end_street.lower()):
            #Calc longitude latitude distance between them.
            distance = longlat_to_metres(node, self.end_node)
            #Then add an edge from node with start_id to end node.
            self.node_list[start_id].add_edge(self.end_node, (distance, way[1]))
    
    def node_exists(self, node_id):
        '''Determine if a node with given ID already exists in the graph.'''
        if node_id in self.node_list:
            #If node exists, return True
            return True 
        #If node does not exist, return False.
        return False

    def dfs(self):
        '''
        Performs a depth first search of the graph to determine if the start node and end node are connected.
        Note: Uses Python's implementation of queue.

        I chose DFS as I thought it would be more efficient than a BFS implementation. This is due to the nature 
        of the bounding box of which the intersections are pulled from; the destination node is very likely to be
        deep in the graph, since the destination and start nodes are on opposite sides of the bounding box.
        -----------------------------------------------------------------------------------------------------
        Returns:
        True  --> if start node and end node are connected.
        False --> if start node and end node are not connected.
        -----------------------------------------------------------------------------------------------------
        Proof of concept:
        
        Test case for not connected:
        Address1 --> 23 Garden Rd, Parson's Pond, Newfoundland
        Address2 --> 22 Avenue Jacques Cartier, Blanc-Sablon, Quebec

        Explanation:
        The above two addresses are not connected because they are separated by a body of water
        (the gulf of st. lawrence) in Eastern Canada. They are on different masses of land.
        -----------------------------------------------------------------------------------------------------
        '''
        #Dictionary of booleans indicating whether a node with given ID has been discovered yet.
        discovered = {}

        #Initialize discover array as false.
        for key, node in self.node_list.items():
            discovered[node.get_id()] = False

        discovered[-1] = False #Start node discovered = false.
        discovered[-2] = False #End node discovered = false

        stack = [] #Using a list as a stack

        #Append the start node to the list.
        stack.append(self.start_node)

        #Perform DFS while the stack is not empty..
        while stack != []:
            #Pop top node from stack.
            u = stack.pop()
            #Get u's edgelist.
            edge_list = u.get_edgelist()
            #For all nodes adjacent to u...
            for key, edge in edge_list.items():
                v = edge[0]          #Define the destination node of the edge as v.
                if v.get_id() == -2: #If the node is the end node,
                    #Return true since start node and end node are connected.
                    return True
                if discovered[v.get_id()] == False: #If node is not yet discovered..
                    discovered[v.get_id()] =True #Set discovered to true.
                    #Append the node to the stack.
                    stack.append(v)
                
        return False


    def djikstra(self):
        '''
        Performs a variant of Djikstra's algorithm to find the shortest path between nodes.
        --------------------------------------------------------------------------------------------------
        Note:  Uses Python's implementation of heap queue to get a time complexity of O(|E|+|V|*|logV|).
        '''
        #List for heapqueue.
        heapqueue = []
        
        '''
        #---Start Node---# 
        Note: Previous node and street will always be null / "" respectively.
        '''
        self.start_node.set_distance(0)            #Initialize distance to source node as 0.
        heapq.heappush(heapqueue, self.start_node) #Push it to the heapqueue.

        #Initialize values for each node in the Graph node list. (Excluses start and end nodes)
        for key, node in self.node_list.items():
            node.set_distance(40075000)         #Set distance to diameter of earth in meters. (max distance)
            node.set_previous(None)             #Set previous to None. (null)
            node.set_prev_street("")            #Previous street --> non-existant.
            heapq.heappush(heapqueue, node)     #Push the node to the heapqueue.
        
        #--End Node--#
        self.end_node.set_distance(40075000)     #Diameter of earth in meters (max distance)
        self.end_node.set_previous(None)         #Previous node to None. (null)
        self.end_node.set_prev_street("")        #Previous street --> non-existant.
        heapq.heappush(heapqueue, self.end_node) #Push the node to the heapqueue.
        
        #While heapqueue is not empty...
        while(heapqueue != []):
            #Pop node with smallest distance.
            u = heapq.heappop(heapqueue)
            #Get the latitude/longitude values from the node popped.
            t1, t2= u.get_latlong()
            #Get the edgelist from the node popped.
            edge_list = u.get_edgelist()

            #For each edge in the edge list..
            for key, edge in edge_list.items():
                v = edge[0]         #v --> Node (i.e. intersection) that the edge (i.e. street) leads to.
                weight = edge[1]    #weight --> Distance in metres from u (node popped) to v.
                street = edge[2]    #street --> Name of street.
                #Temp = the distance to v from node u.
                temp = u.get_distance() + weight    
                if temp < v.get_distance():
                    '''
                    If the distance to node u from node v is less than the v's current distance...

                    Update every attribute of node v to indicate that node u is the previous node
                    to v in regards to shortest path to v from the very start node.
                    '''
                    v.set_distance(temp)        #Set the distance to temp.
                    v.set_previous(u)           #Set the previous node to u.
                    v.set_prev_street(street)   #Set the previous street name to street.

            #Heapify the heapqueue after dealing with each node.
            heapq.heapify(heapqueue)

        '''
        After Djikstra's has completed...
        Reverse-build the shortest path from end node to start node.
        '''
        #Start at last node.
        node = self.end_node
        #List to build shortest path.
        shortest_path = []
        #While the previous node is not equal to none.. (i.e. not equal to the very start node)
        while(node != None):
            latitude, longitude = node.get_latlong()
            #Ignore start node because we are only interested in previous edges. (Start node previous = null)
            if(node.get_previous() != None):
                #Calculate distance from previous node to current node. (current_dist - prev_dist)
                distance = node.get_distance() - node.get_previous().get_distance()
                #Insert to front of list a list that includes [lat, long, prev_street, and distance]
                shortest_path.insert(0, [latitude, longitude, node.get_prev_street(), distance])

            #Move to previous node of current node.
            node = node.get_previous()
    
        #Return the list of edges in shortest path.
        return shortest_path

        
class Node(object):
    '''My node implementation'''

    def __init__(self, osm_id, latitude, longitude):
        ''' 
        Initialization for the node.
        -----------------------------
        Inputs:
            - osm_id  -->   The unique id for the node. The unique OSM (Open Street Map) id.
            - latitude  --> The latitude coordinate of the node / intersection.
            - longitude --> The longitude coordinate of the node / intersection.
        '''
        self.id = osm_id            
        self.latitude = latitude    
        self.longitude = longitude
        #edge_list is a dictionary of edges which allows fast look up of nodes based on destination node id.
        self.edge_list = {}      
        '''Variables for Djikstra's implementation'''
        self.distance = 40075000   #Diameter of earth in meters (max distance)
        self.previous = None       #Previous node = none. (null)
        self.prev_street = ""      #Previous street --> Non existant.

    def __lt__(self, other):
        '''
        "less than" method.
        Allows comparison of nodes for use in the Djikstra heapqueue.
        '''
        #Nodes are ordered by distance. (Less distance < More distance)
        return self.distance < other.distance  

    def add_edge(self, destination_node, way):
        '''
        Adds an edge to the edgelist of the node.
        ------------------------------------------
        Input:
        destination_node --> The node which the edge leads to.
        way --> Holds information about the edge that connects the current node to
                the destination node.
        ------------------------------------------
        Output:
        Adds an entry to edgelist with the key of the destination node's id.
            - This entry is a tuple of (destination_node, edge_length, street_name)
        '''
        self.edge_list[destination_node.get_id()] = (destination_node, way[0], way[1])
    
    def set_distance(self, weight):
        '''
        Sets the distance attribute of the node.
        distance is the shortest known distance from the start node to the current node.
        '''
        self.distance = weight
    
    def set_previous(self, node):
        '''
        Sets the previous attribute of the node.
        previous is the previous node which the current node was traversed from in shortest path.
        '''
        self.previous = node
    
    def set_prev_street(self, street_name):
        '''
        Sets the prev_street attribute of the node.
        prev_street is the previous street name which the current node was traversed from in shortest path.
        '''
        self.prev_street = street_name

    def get_distance(self):
        '''
        Gets the distance attribute of the node.
        distance is the shortest known distance from the start node to the current node.
        '''
        return self.distance
    
    def get_previous(self):
        '''
        Gets the previous attribute of the node.
        previous is the previous node which the current node was traversed from in shortest path.
        '''
        return self.previous
    
    def get_prev_street(self):
        '''
        Sets the prev_street attribute of the node.
        prev_street is the previous street name which the current node was traversed from in shortest path.
        '''
        return self.prev_street

    def get_latlong(self):
        '''
        Returns the latitude longitude coordinates of the current node.
        Example: latitude, longitude = node.get_latlong()
        '''
        return self.latitude, self.longitude

    def get_edgelist(self):
        '''
        Returns the edge list of the current node.
        Example: edgelist = node.get_edgelist()
        '''
        return self.edge_list

    def get_id(self):
        '''
        Returns the unique id of the current node.
        Example: id = node.get_id()
        '''
        return self.id


def longlat_to_metres(node1, node2):
    '''
    Calculate the distance between two nodes based on latitude/longitude coordinates.
    ---------------------------------------------------------------------------------
    Input:  Two nodes.
    Output: The distance between the two nodes in metres.
    '''
    lat1, long1 = node1.get_latlong()
    lat2, long2 = node2.get_latlong()
    #Use a geopy function to calculate the distance between the two nodes, and then manually convert to metres.
    distance = (geopy.vincenty((lat1, long1), (lat2, long2)).km * 1000)
    #Return the distance.
    return distance