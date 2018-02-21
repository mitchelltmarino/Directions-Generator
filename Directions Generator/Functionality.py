'''
Name: Mitchell Marino
Date: 2018-02-20
Program: Functionality.py
Description: Includes the main functions that provide functionality to the 
             Directions Generator application. This includes pulling information 
             from the Open Street Map database, using geopy to resolve addresses,
             and using my own implementation of Graph, BFS, Djikstra's algorithm,
             etc. to determine connectivity and calculate the shortest route.
             This module also randomly generates dynamic sentences for each step
             of the route to provide more engaging directions.
'''

#Imports
import math
import geopy
import random
import osmnx as ox
import Data_Structures as ds

def resolve_address(address):
    '''
    Attempt to resolve a given address.
    This is done by determining if it can be found by geolocator.
    If the address cannot be resolved then an AttributeError exception will be thrown.
    '''
    #Geolocator object
    geolocator = geopy.Nominatim()
    #Throws error if address not resolved:
    #Obtain full addresses from geolocator. 
    #The replacement is just to remove the comma after street number for more standard appearance.
    full_address = geolocator.geocode(address).address.replace(",","",1)

    return full_address
    
def generate_bounding_box(address1, address2):
    '''
    Generate a bounding box determined by two addresses.
    This bounding box is a determinant for all street info that is pulled from the OSM database.
    Only streets located within the bounding box will be fetched.
    --------------------------------------------------------------------------------------------
    The bounding box is generated as such:
        - The bounding box area includes both addresses, plus a 1 kilometre buffer area
            surrounding them.
        - It is determined by 4 latitude longitude coordinates; one for each side of the box.
    '''
    #Geolocator to convert address to longitude / latitude locations.
    geolocator = geopy.Nominatim()
    location1 = geolocator.geocode(address1)
    location2 = geolocator.geocode(address2)

    #North, south, east, west bounds for the bounding box.
    north = max(location1.latitude, location2.latitude)     #Northern-most point.
    south = min(location1.latitude, location2.latitude)     #Southern-most point.
    east = max(location1.longitude, location2.longitude)    #East-most point.
    west = min(location1.longitude, location2.longitude)    #West-most point.

    #Add approximately 1 km of distance to each parameter of the bounding box.
    #(1 kilometer is converted to longitude/latitude degrees)
    north = north + (1 / 111.321543)
    south = south - (1 / 111.321543)
    east = east + abs((1 / (math.cos(east) * 111.321543)))
    west = west - abs((1 / (math.cos(east) * 111.321543)))

    #Return the bounding box coordinates.
    return north, south, east, west

def generate_endpoint_nodes(address1, address2):
    '''
    Generate start and destination nodes for the pathfinder.
    Also, parse the data from geolocator to return the endpoint street names.
    '''
    #Geolocator to convert address to latitude/longitude locations.
    geolocator = geopy.Nominatim()
    location1 = geolocator.geocode(address1)
    location2 = geolocator.geocode(address2)

    #Address returned by geolocator is of format: 00, street, city, ... etc
    #So by splitting by ', ' and indexing point 1, obtain the street of each endpoint.
    start_street = location1.address.split(", ")[1]
    end_street = location2.address.split(", ")[1]

    #Create nodes for start point and end point.
    start_node = ds.Node(-1, location1.latitude, location1.longitude)
    end_node = ds.Node(-2, location2.latitude, location2.longitude)
    
    #Return the street names and enpoint nodes.
    return start_street, start_node, end_street, end_node

def determine_direction(latlng1, latlng2):
    '''
    Input: 
    latlng1, latlng2 are tuples of latitude/longitude degrees.
    latlng1 = Starting coordinate.
    latlng2 = Ending coordinate.
    ----------------------------------------------------------
    Output:
    The direction of travel to traverse from ltlng1 to latlng2.
    Examples:
        ("North","South","East","West")
        ("North-East","North-West","South-East","South-West")
    '''
    #Define temporary variables for easier readability.
    lat1 = latlng1[0]
    lat2 = latlng2[0]
    lng1 = latlng1[1]
    lng2 = latlng2[1]

    #Variable to store return value.
    direction = ""

    if(lat1 < lat2):
        #If lat2 is greater than lat1, direction --> North.
        direction1 = "North"
    else:
        #If lat2 is greater than lat1, direction --> South.
        direction1 = "South"
        
    if(lng1 < lng2):
        #If lng2 is greater than lng1, direction --> East.
        direction2 = "East"
    else:
        #If lng1 is greater than lng2, direction --> West.
        direction2 = 'West'
   
    '''
    Direction is determined by change in latitude / longitude.
    North, South, East, West --> When latitude / longitude is evidently dominant.
    N-E, N-W, S-E, S-W       --> When there the ratio is somewhat split evenly.
    '''
    if lng1-lng2 == 0:
        #If the denominator of ratio is 0, ratio is latitude dominant.
        ratio = .71
    else:
        #Ratio of change in latitude / change in longitude.
        ratio = abs(lat1-lat2)/abs(lng1-lng2)
    
    if ratio >= .30 and ratio <= .70:
        #Evenly split qualifies for one of: N-E, N-W, S-E, S-W.
        direction = "%s-%s" %(direction1, direction2)
    elif ratio > .70:
        #latitude dominant qualifies for: "North" or "South"
        direction = direction1
    else:
        #longitude dominant qualifies for "East" or "West"
        direction = direction2

    #Return the direction.
    return direction

def deterimine_turn(direction1, direction2):
    '''
    Logically determines which turn would have to be made in order to change 
    facing direction from direction1 to direction 2.
    ---
    For example:
    To change from facing North to facing East, you would make a right turn.
    ---------------------------------------------------------------------------
    Input: 
    direction1 --> Initial facing direction.
    direction2 --> End facing direction.
    ---------------------------------------------------------------------------
    Output:
    The turn that would need to be made to face direction2 from direction1
        Either "Right", "Left",
        OR "Unknown" in the case of insufficient information.
    '''
    #Unknown is returned if coordinates from database are not sufficient to determine turn direction.
    turn = "Unknown"

    '''
    In the case that one or both of the directions is mixed.. (For example "North-East")
    Some logical splitting needs to be done to break the directions into dominant directions 
    used for decision making.
    '''
    if '-' in direction1:
        if direction2.lower() == "north" or direction2.lower() == "south":
            direction1 = direction1.split('-')[1]
        else:
            direction1 = direction1.split('-')[0]
    if '-' in direction2:
        if direction1.lower() == "north" or direction1.lower() == "south":
            direction2 = direction2.split('-')[1]
        else:
            direction2 = direction2.split('-')[0]

    #Case: North starting position.
    if direction1.lower() == "north":
        if direction2.lower() == "east":
            turn = "Right"
        elif direction2.lower() == "west":
            turn = "Left"
    #Case: South starting position.
    elif direction1.lower() == "south":
        if direction2.lower() == "east":
            turn = "Left"
        elif direction2.lower() == "west":
            turn = "Right"
    ##Case: East starting position.
    elif direction1.lower() == "east":   
        if direction2.lower() == "north":
            turn = "Left"
        elif direction2.lower() == "south":
            turn = "Right"
    #Case: West starting position.
    elif direction1.lower() == "west":
        if direction2.lower() == "north":
            turn = "Right"
        elif direction2.lower() == "south":
            turn = "Left"

    #Return the turn direction.
    return turn
    
def simplify_streetname(street):
    '''
    Simplifies the name of a street to account for experienced inconsistency
    in the OSM database. This is done by removing "north", "south", "east", or
    "west" from the end of a street name.
    ---------------------------------------------------------------------------------
    Reasoning for this:
        I experienced that the OSM street name results have a habit of changing from, 
        for example, "King Street West", to "King Street", back to "King Street West"
        depending on the section of the street. To avoid confusion, it is easier to 
        just simplify the street names.
    '''
    #Split the street by whitespace.
    street_split = street.split()
    #List of directions to look for in the street name.
    direction_list = ["north","south","east","west"]

    #If the street name ends with one of the directions,
    #Rebuild the street name and exclude the direction at the end.
    if street_split[len(street_split)-1].lower() in direction_list:
        street = ""
        for i, word in enumerate(street_split):
            if word.lower() not in direction_list:
                street += word + " "
    
    #Return street, split of whitespace.
    return street.strip()

def build_sentence(i, steps, point_a, point_b):
    '''
    Dynamically and randomly constructs a sentence for the directions to be shown
    to the user.
    ------------------------------------------------------------------------------
    Input:
        steps --> Total number of steps in the directions.
        Both points are lists of [street,length,direction,turn]
        Point_a --> The beginning of one street. 
        point_b --> The beggining of a street reachable from point_a.
    ------------------------------------------------------------------------------
    Output:
        A string instruction of how to get from point_a to point_b. 
    '''
    #Sentence pieces that can be used to dynamically and randomly generate a sentence template:

    #Beginning strings mainly relevant for the very beginning instruction.
    beginnings = ("Drive |nsew|", "Head |nsew|", "Travel |nsew|", "Go |nsew|")

    #Beginning strings relevant for all instuctions after the very beginning.
    sentence_starts = ("Follow |cs|", "Travel along |cs|", "Travel on |cs|", "Drive along |cs|", 
                       "Drive on |cs|", "Drive |nsew|", "Continue |nsew|", "Head |nsew|", "Go |nsew|")
    
    #Strings used to build the middle of the sentence.
    sentence_middle = {}
    sentence_middle['nsew'] = (", heading |nsew| for |dist|", ", and head |nsew| for |dist|",
                               " and go |nsew| for |dist|")
    sentence_middle['cs'] = (" along |cs| for |dist|", " on |cs| for |dist|")

    #Strings used to build the end of the sentence.
    sentence_ends = {}
    sentence_ends['lr known'] = (". Then turn |lr| onto |ns|.", " before turning |lr| onto |ns|.", " and turn |lr| onto |ns|.",
                                 " and then turn |lr| onto |ns|.")
    sentence_ends['lr unknown'] = (". Then head |nnsew| on |ns|.", " before heading |nnsew| on |ns|.", ". Then turn onto |ns|.",
                                   " and head |nnsew| on |ns|.", " and turn onto |ns|.")

    '''
    SENTENCE TEMPLATE PLACEHOLDERS:
        |cs| = current street.
        |ns| = next street.
        |lr| = left or right.
        |dist| = distance.
        |nsew| = direction. (north/south/east/west or combination)
        |nnsew| = nsew of next street.
    '''

    #Generate sentence template depending on multiple conditions:
    if i == 0:
        #For very beginning steps.
        sentence = random.choice(beginnings).lower()
        sentence += random.choice(sentence_middle['cs'])
    elif i < steps:
        #For all other steps.
        sentence = random.choice(sentence_starts)
        if "|cs|" in sentence:
            sentence += random.choice(sentence_middle['nsew'])
        else:
            sentence += random.choice(sentence_middle['cs'])
    if i < steps-1:
        #If not the final step.. attempt to include instruction for turning.
        if point_b[3] != "Unknown":
            #If turn is known, include instruction on how to turn.
            sentence += random.choice(sentence_ends['lr known'])
        else:
            #If turn is not known, include generic instruction to indicate a street change.
            sentence += random.choice(sentence_ends['lr unknown'])
    
    #Lambda function to add the word "bound" in order to make instructions sound more appealing.
    #For example, instead of "drive North", say "drive North-bound"
    add_bound = lambda s: s+"-bound" if not '-' in s else s 

    distance = point_a[1]
    #If distance is greater than 1000 Metres, convert it to Kilometres
    if distance  >= 1000:
        distance = distance / 1000
        distance = ("%.1f Kilometres" %(distance)).replace(".0","")
    else:
        #If distance is less than 1000 Metres, round to nearest whole Metre.
        distance = str(int(distance))+" Metres"

    #Replace the placeholders with their respective vairables.
    sentence = sentence.replace("|cs|", point_a[0]).replace("|dist|", distance).replace("|nsew|", add_bound(point_a[2]))
    if point_b != None:
        sentence = sentence.replace("|ns|", point_b[0]).replace("|nnsew|", add_bound(point_b[2])).replace("|lr|", point_b[3].lower())

    #Return the instruction.
    return sentence


def generate_directions(start_address, end_address, route):
    '''
    Generates an array of instructional sentences for the route given.
    ------------------------------------------------------------------------------
    Input:
        start_address --> The address of which the route is to begin from.
        end_address --> The address of which the route is to end at.
    ------------------------------------------------------------------------------
    Output:
        An array of sentences.
            Each sentence is a step in the instructions of the route 
            for traversing from start_address to end_address.
    '''

    #Initialization
    route_information = [] #Basic information on the route.
    prev_end = None        #The end coordinates of the previous street.
    i = 0                  #Increment variable.

    #While loop that runs until the route has been fully described.
    while i < len(route):
        '''
        This while loop constructs simple paths from a series of latitude/longitude coordinates
        along with the street names that correspond to those coordinates.
        '''
        #Initial variables for current street.
        length = 0                                  #Length of street.
        street = simplify_streetname(route[i][2])   #Street name.
        startlatlng = (route[i][0], route[i][1])    #Start coordinates.
        turn = "Unknown"                            #Turn to get onto this street.

        while i < len(route) and simplify_streetname(route[i][2]) == street:
            #While path is not ended, and still on this street...
            #Continuously add to length and increment the incrementor.
            length += route[i][3] 
            i += 1

        endlatlng = (route[i-1][0], route[i-1][1])  #Make note of end latlng of previous street.

        if prev_end == None:
            #If it is the very first street.
            #Determine direction facing based on start of current street and current street end.
            direction = determine_direction(startlatlng, endlatlng)
            
        else:
            #If it is not the very first street.
            #Determine direction facing based on end of previous street and current street end.
            direction = determine_direction(prev_end, endlatlng)
            turn = deterimine_turn(route_information[len(route_information)-1][2], determine_direction(prev_end, startlatlng))
        
        #Define previous end at the end latitude longitude of the previous street.
        prev_end = endlatlng

        end_index = len(route_information) - 1

        if end_index > 0 and route_information[end_index][0] == street:
            #Helps deal with streets that are connected by round-abouts, etc.
            route_information[end_index][1] += length
        elif not "_" in street:
            #Ignore "secondary_links" and other links that connect two streets.
            route_information.append([street,length,direction,turn])
        elif "_" in street:
            #Add the length of the secondary link to the previous street to increase distance accuracy
            route_information[end_index][1] += length
            
    #A list of directions. (An itinerary)
    itinerary = []

    #Number of steps needed to address the route completely.
    steps = len(route_information) #Had to be recalculated (incase route_information had another index appended to it)

    #Loop through route_information, generating a dynamic instructional sentence for each step.
    for i, street in enumerate(route_information):
        if i < steps-1:
           instruction = build_sentence(i, steps, street, route_information[i+1])
           if i == 0:
               #If the very beginning step.
               instruction = "Starting at your location %s, %s" %(start_address, instruction)
        else:
            #If the very end step.
            instruction = build_sentence(i, steps, street, None)
            instruction = "%s and you will have arrived at your destination at %s." %(instruction, end_address)
        
        #Append each instruction to the itinerary.
        itinerary.append(instruction)
    
    #Return the list of instructional sentences.
    return itinerary


def generate_route(start_address, end_address):
    '''
    The main function of this module which uses most other functions inside of it.
    Attempts to determine a route from start_address to end_address. Based on the
    route, specific directions will be generated.
    ------------------------------------------------------------------------------
    Input:
        start_address --> The address of which the route is to begin from.
        end_address --> The address of which the route is to end at.
    ------------------------------------------------------------------------------
    Output:
        An array of sentences.
            Each sentence is a step in the instructions of the route 
            for traversing from start_address to end_address.
    '''

    #Generate the bounding box of which to pull coordinates from.
    north, south, east, west = generate_bounding_box(start_address, end_address)

    #Pull a custom graph data structure using the OSMNX api. 
    #This is relaible and preferable as it considers many variables such as 1 way streets, etc.
    G = ox.graph_from_bbox(north=north, south=south, east=east, west=west, network_type='drive', simplify=True, truncate_by_edge=True, timeout=30)

    #Generate start street name, end street name, and their respective nodes.
    start_street, start_node, end_street, end_node = generate_endpoint_nodes(start_address, end_address)

    #Create my own graph, initializing with start and end nodes.
    intersections = ds.Graph(start_street, start_node, end_street, end_node)

    #u --> Start vertex
    #v --> End vertex
    #weight --> Length of street.
    for u, v, keys, weight in G.edges(data='weight', keys=True):

        if intersections.node_exists(u) == False:
            #If the u node does not exist, add it. (y=lat, x=long)
            intersections.add_node(u, G.node[u]['y'], G.node[u]['x'])
        if intersections.node_exists(v) == False:
            #If node v does not exist, add it. (y=lat, x=long)
            intersections.add_node(v, G.node[v]['y'], G.node[v]['x'])
        
        #way_list --> List of minimum paths.
            #Way is analogous to street. (It is OSM terminology; thought it would be more consistent)
        way_list = []

        #Loop through street adjacency lists to find paths between intersection u and intersection v.
        for key, way in G.adj[u][v].items():

            '''
            Note for future implementation:
                #way['maxspeed'] gets speed of way. Can use this for fastest path implementation
                Such as: time = way['maxspeed]/way['length']
            '''

            if 'name' in way:
                #If way has a name (some do not have 'name' attributes)
                if type(way['name']) is list:
                    #If it is a list of names (Some have multiple names)
                    for name in way['name']:
                        #Append them all because one street may be equivalent to that start/end address.
                        way_list.append((way['length'], name))
                else:
                    way_list.append((way['length'], way['name']))
            elif 'highway' in way:
                if type(way['highway']) is list:
                    #If it qualifies of different types of ways.
                    way_list.append((way['length'], way['highway'][0]+"_")) #_ Helps conclude that path has no name.
                else:
                    #Append highway type instead.
                    way_list.append((way['length'], way['highway']+"_")) #_ Helps conclude that path has no name.

            #A list of critical ways. (Ways that connect to start point / end point)
            critical_list = []

            for way in way_list:
                #For each way in way list, append it to critical list if it matches start or end street names.
                try:
                    if way[1].lower() == start_street.lower() or way[1].lower() == end_street.lower():
                        critical_list.append(way)
                except:
                    continue #Catch anomalies
            
            for way in critical_list:
                #For each way in the critical list (if there are any), add the critical edge to node u's edgelist.
                intersections.add_critical_edge(u,way)

            #Sort the way list and then take the smallest index. (The smallest value... time complexity nlogn)
            way_list.sort(key=lambda t: t[0])
            way = way_list[0]
            
            #Add the minimum weight edge between intersections u and v to my graph implementation.
            intersections.add_edge(u,v,way)

    '''
    Use the intersections Graph's function djikstra() to determine if the graph's start node
    and the graph's end node are connected.
        - intersections.dfs() = True if connected.
        -                     = False if not connected.

    Proof of concept / a test case for disconnected graphs can be found in the datastructures.py module
    under the BFS function.
    '''
    if intersections.dfs() == False:
        return "Disconnected"
    
    '''
    Use the intersections Graph's function djikstra() to obtain the shortest route path between
    the Graph's predefined start and end nodes. (Nodes are analogous to vertices)

    The shortest path route will be a list of lists in format:
        [latitude, longitude, street_name, distance]
    
    Notes:
        - latitude/longitude = the coordinates of the node / intersection referred to.
        - Street_name  = Street that is being traversed to reach that intersection.
        - distance = distance in meters.
    '''
    route = intersections.djikstra()

    #Generate a list of directions using generate_directions function call.
    itinerary = generate_directions(start_address, end_address, route)

    #Return the list of directions.
    return itinerary