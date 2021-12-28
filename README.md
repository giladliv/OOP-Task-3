# OOP-Task-3
This is the task 3 of the OOP course, and it is about Directed Weighted Graph
we have a simulator that we build for ourselfves

## UML
first we show you the UML of the Project
![umlDig](/Ex3/pics/UML.png)

### Explenatin about the classes
each class has its own porpuse:
- ![GraphInterface.py](/Ex3/src/GraphInterface.py) - the interface of the directed wheighted Graph
- ![GraphAlgoInterface.py](/Ex3/src/GraphAlgoInterface.py) - the interface ot the algoritms that can be performed on the graph
- ![DiGraph.py](Ex3/DiGraph.py) - the implementation of ![GraphInterface.py](/Ex3/src/GraphInterface.py), this is the usable directed graph, includes adding removeing of nodes and edges
- ![GraphAlgo.py](Ex3/GraphAlgo.py)- the implementation of ![GraphAlgoInterface.py](/Ex3/src/GraphAlgoInterface.py), this is the usable the class alows to load and save directed wheighted graphs, perform of them the following algorithms: TSP, Shortest path between 2 nodes, Find the center of a graph
- ![EnterWindow.py](/Ex3/Simulator/EnterWindow.py) - lets us to enter data according to our needs, remember to set the lebels for the inputs, you can also guide with it the user on what is needed to be done
- ![SimulatorGraph.py](Ex3/Simulator/SimulatorGraph.py) - the beating heart of the simulator - this is the the GUI that the user can enjoy its powers and to anlyise the behavoiurs of some graphs
- the Package ![pygame_ui](/Ex3/pygame_ui) - this pakage was given for us to present buttons and menues in the most comfuterable ways, that also we can do the assignment with the best tools and also guide us and save us some time, you are more then welcome to examine it

## Simulator
please note the main file: ![mainfile](/Ex3/src/main.py)
there you can enjoy multipule graphs, and also upload your graphs as well
the graphs is presentes in when the function 'plot_graph' is activated

example of the Simulator:
![simWind](/Ex3/pics/graphExm.png)

### GUI window
the window has the options below:
 - Load graph from existing json file
 - Save Graph to json file
 - Find the shortest path between 2 nodes
 - Presenting the center of the graph
 - Perform TSP on several nodes in graph (find the shortest path, thet contains all of the requested nodes)
 - Refresh the Graph

#### Load graph
after pressing the button, select the json file that presents the Graph
after opening it the graph will be updated


#### Shortest path
enter to the window that presented to you the src and dest nodes,
after done choosing click on the button to perform the shortest path,
Then only the nodes and edges that involved will be shown, to the user.
Pressing on any button will refresh the graph to the origins
this is applied by the Dijiakstra algorithm

*Runtime = O(|V|+|E|)*


#### Center of graph
the center of the graph will be shown.

*Runtime = O(|V|x(|V|+|E|))*

#### TSP
similar to selecting the Shortest path, after done selecting it will show only the nodes and edges that involved.

*Runtime = O(|V| x (|V|+|E|)^2)*

#### Refresh
when pressing on this button the graph will be refreshed and prersented before any other algorithms preformed


## Run Times
this is the comparison of the diffrent Assignments:
![rtPic](/Ex3/pics/rt.png)

