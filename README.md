# Directions-Generator

Hello, and thank you for checking out my Directions Generator application! This program can be used to obtain dynamically generated, shortest-path directions between any two locations entered into the application's GUI! The application's The GUI provides comfortable, dynamic resizing.

All data is pulled from the Open Street Map (OSM) open source database using the OSMNX API. Discover more about the Open Street Map project at these locations:

• https://en.wikipedia.org/wiki/OpenStreetMap

• https://www.openstreetmap.org

## Program Functionality

* Uses Geopy to geocode addresses to latitude / longitude coordinates.
* Uses the OSMNX api to pull street information from the Open Street Map database.
* Parses data from the database and stores it in my own Graph data structure  implementation, which contains street and intersection information.
	* Intersections are equivalent to vertices.
	* Streets are equivalent to edges (and edge weights are street lengths).
* Uses Depth First Search to verify connectivity between the start and destination locations.
* Uses Djikstra's Algorithm to determine the absolute shortest path between the start and destination locations.
* Uses algorithms and logic to determine the direction of a street, as well as the direction that you must turn to reach that street.
* Dynamically builds sentences using an array of randomly selected sub-templates. 

## Sample Directions Search

From Markville Mall, Markham, Ontario to Yorkdale Mall, Toronto, Ontario

![alt text](https://github.com/mitchelltmarino/Directions-Generator/blob/master/Assets/Directions%20Sample.PNG?raw=true "Directions Sample")


  
## Help Page (and about Mitchell!)

Explains how to use the program as intended, and also goes into moderate depth explaining functionality.

![alt text](https://github.com/mitchelltmarino/Directions-Generator/blob/master/Assets/Help%20Sample.PNG?raw=true "Help Frame")

## How it works: Under the hood

* **Pulling data from the OSM database**
	* The program uses the geopy geocoder to convert the start and end addresses to latitude/longitude coordinates.
	* Then, a bounding box of latitude/longitude coordinates is calculated that bounds the location between the start and destination points plus a 1km buffer north/south/east/west of the location and destination points.
		* The 1km area is calculated using a 'dirty conversion' for estimating latitude/longitude to km.
	* Then, the bounding box is then used as a parameter to pull the information of all streets within its area from the Open Street Map Database.

* **The Graph data structure**
	*	The data from the database is parsed and placed into my own implementation of a Graph data structure. The structure has a list of nodes (nodes are their own separate object) and both the graph and node object classes have functions for accessing and manipulating their information. 
		*	Intersections are analogous to vertices.
		*	Streets are analogous to edges, and their weight is the street length.

* **Depth First Search**
	* Depth First Search is used to determine if the destination vertex can be reached from the start vertex. If the start vertex is not connected to the end vertex on the graph, then DFS will discover this and the user will be notified.
	* The reason I decided to use DFS instead of BFS is because it will be much more efficient at discovering the end vertex. This is due to the nature of the data set that the graph holds:
		* The bounding box grows in relation to the distance of the start and destination locations, with each being on opposite ends of the box.
		* Therefore, since DFS excels at discovering deep vertices first whereas BFS excels at discovering shallow ones first, DFS was the obvious choice.
	* A simple proof of concept for the DFS implementation is as follows:
		* Address1 --> 23 Garden Rd, Parson's Pond, Newfoundland
		* Address2 --> 22 Avenue Jacques Cartier, Blanc-Sablon, Quebec
	* If you try searching the above two addresses using the application, then the program will inform you that there is no path between them. The reason that these two addresses are not connected because they are separated by a body of water (the Gulf of St. Lawrence) in Eastern Canada. They are on different masses of land.

* **Djikstra's Aglorithm**
	* If the two paths are found to be connected by DFS, then Djikstra's algorithm is used to calculate the absolute shortest path.
	* I used Python's native heapqueue implementation in my Djikstra's algorithm for a time complexity of O(|E|+|V|log|V|).

* **Directions Generation**
	* **Polar direction determination (North/South/East/West)**
		* The direction of a street is calculated by tracking and logically comparing the change in latitude and longitude on the end points of the subsection of the street traversed in the route.
	* **Turn direction  determination**
		* The "polar" direction (north/south/east/west) is calculated by comparing the latitude / longitude coordinate of the final location that is traversed on the previous street to the latitude/longitude coordinate of the first location that is traversed on the current street.
		* The previous polar direction is then logically compared to the immediate polar direction following the turn to determine the direction required for the turn. For example, changing direction from (North-bound to East-bound requires a right turn)
			* If the latitudinal/longitudinal data provided by the OSM database is not accurate enough to determine the polar direction, then the particular turn is omitted from the directions description.
	*	**Dynamic sentence generation**
		*	Sentences are built using a list of templates.
		*	They are generated randomly, so that every sentence feels fresh and the instructions do not feel dull or repetitive!
		*	I have a list of sentence starts, sentence middle, and sentence end strings.
		*	Depending on the index of the instruction in the sequence, a combination of sentence templates are randomly selected and pieced together where the former selection generally determines the latter.
			*	For instance, if the  first piece of the sentence includes the direction of the street (north/south/east/west) , then the second sentence will ensure to include another piece of relevant data instead, such as the distance until the next turn or the street name.
		*	The sentence templates have "placeholders" which will eventually be replaced by real and meaningful values after the full sentence is dynamically constructed.

* **Additional Notes**
	* My application relies very much on consistency on the OSM database. In some locations, such as downtown Toronto, I find that the data supplied by OSM is quite inconsistent and variable so directions may not be able to be successfully generated. 
	* For instance, I have found that some roads do not register as roads that vehicles can drive on, but rather paths that are exclusively for trams although this is simply not the case in the real world.
	* Unfortunately, since my application deals with only roads that are defined as roadways that vehicles can drive on by OSM, little anomalies like the one described above can be an obstacle for the proper or successful calculation of shortest path.

**THANK YOU!**

If you have gotten this far, thank you very much for reading as you have shown genuine interest in my project. Overall, I found this project to be really fun and I learned a lot.  If you have any inquiries about me or my project I welcome you to contact me at mitchelltmarino@gmail.com!
