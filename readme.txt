For this assignment I implemented a modified Nearest Neighbor solution to the Traveling Salesperson problem. The solution can be ran with a preference towards time, the best solution of X amount of iterations, or reaching an approximation ratio threashold when the tour length is known or can be guessed to some degree of accuracy. The benefit of each of these solutions is that they provide relatively quick solutions to TSP while returning results that are fairly close to (~125% of) optimal.  

Running the program on the input files: 
tsp_example_X.txt  
will result in the program running until a Approximation Ratio APPROX (currently 1.25) is met. 

Running the program against 
test-input-X.txt 
files will allow the user to choose between running the program as fast as possible or running it BEST (currently 100) times.

either way, to run copy the provided files and type:
$ python Project3.py <inputfilename>

The output will be stored in <inputfilename>.tour in the current directory
