#!/usr/bin/env python
# coding=utf-8
###################################################################
#  Project 3 - CS 325
#  Parker Howell
#  Solutions to TSP using Nearest Neighbor algorithm.
###################################################################

import sys
import math
import random
from timeit import default_timer as timer
import copy




###################################################################
#  APPROX - ratio needed to stop NNApproxEx function. 
#  *** WARNING ***  - may cause functions to loop infinitly if set
#                     too low.  Must be > 1 or will inf loop...
# BEST - amount of times to run nearNeighbor with which we will 
#        keep the shortest tour. 
#  *** WARNING ***  - will take a long time given inputs with many
#                     cities to evaluate.
###################################################################
APPROX = 1.25
BEST = 100




###################################################################
#  City - creates a city object
#  cityID - the ID number of the city.
#  x - the x coordinate value of the city.
#  y - the y coordinate value of the city.
###################################################################
class City(object):
	def __init__(self, cityID, x, y):
		self.cityID = cityID
		self.x = x
		self.y = y




###################################################################
#  dist
#  a - city object with x and y attributes.
#  b - city object with x and y attributes.
#  Basic Pythagorean Theorem, takes two city objects and returns 
#  their hypotenuse distance rounded to nearest integer.
###################################################################
def dist(a, b):
	return round(math.hypot(b.x-a.x, b.y-a.y))




###################################################################
#  getInput
#  inFileName - name of input file.
#  opens the file with the filename provided and processes it to
#  create and return a list of city objects to be evaluated in 
#  solving our TSP problems.
###################################################################
def getInput(inFileName):
	with open(inFileName, "r") as in_f:
		# remove leading and trailing white-space
		inputData = [line.strip() for line in in_f]
		cities = []
		for city in inputData:
			# split each line of data into 3 parts removing any extra white-space
			cityID, x, y = city.split()
			cities.append(City(int(cityID), int(x), int(y)))
	return cities




###################################################################
#  makeTour
#  inputCities - list of city objects.
#  inFileName - name of input file.
#  evaluates inFileName and calls the appropriate algoritm to run.
###################################################################
def makeTour(inputCities, inFileName):
	# if running on example problems then we only check for approximation conditions
	if (inFileName == "tsp_example_1.txt" 
	 or inFileName == "tsp_example_2.txt" 
	 or inFileName == "tsp_example_3.txt"):
		length, tour = NNApproxEx(inputCities, inFileName)

	# else check if running for approximation or time conditions
	elif(inFileName == "test-input-1.txt" or inFileName == "test-input-2.txt" 
	  or inFileName == "test-input-3.txt" or inFileName == "test-input-4.txt" 
	  or inFileName == "test-input-5.txt" or inFileName == "test-input-6.txt"
	  or inFileName == "test-input-7.txt"):
		
		# confirm which to run for
		print "Enter a 1 or 2"
		testCase = 3
		while (testCase != 1 and testCase != 2):
			testCase = int(raw_input("Are we running for? 1) Approximation Ratio or 2) Time constraint"))

		# run selection
		if testCase == 1:
			length, tour = NNApprox(inputCities)
		else:
			length, tour = NNTime(inputCities)

	else:
		print "\nError: The input file name DOES NOT match expected file names.\n"

	return length, tour




###################################################################
#  makeOutput
#  length - the length of the tour.
#  tour - list of visited city objects in the order visited.
#  inFileName - name of input file.
#  Creates an output file based on the name of the input file and 
#  then writes the length of the tour followed by each city of the
#  tour to that output file.
###################################################################
def makeOutput(length, tour, inFileName):
	outFileName = inFileName + ".tour"
	with open(outFileName, "w") as out_f:
		out_f.write(str(int(length)) + "\n")
		for city in tour:
			out_f.write(str(city.cityID) + "\n")




###################################################################
#  findNext
#  origin - city to compare other city distances to.
#  remainingCities - list of cities to compare to origin.
#  Compares each city in remainingCities to the origin, saving and
#  returning the city closest to the origin, and the distance 
#  between them.
###################################################################
def findNext(origin, remainingCities):
	currShort = float("inf")
	for city in remainingCities:
		currDist = dist(origin, city)
		if currDist < currShort:
			currCity = city
			currShort = currDist
	return currCity, currShort




###################################################################
#  NNApproxEx
#  inputCities - list of city objects.
#  inFileName - name of input file.  
#  Based on input file, takes the inputcities list and repetedly 
#  calls nearNeighbor until it finds a tour with an approximation
#  ratio less than the constant APPROX - set at top of this file
###################################################################
def NNApproxEx(inputCities, inFileName):
	# set the denominatior based on input file
	length = float("inf")
	if (inFileName == "tsp_example_1.txt"):
		denom = 108159.0
	elif (inFileName == "tsp_example_2.txt"):
		denom = 2579.0
	elif (inFileName == "tsp_example_3.txt"):
		denom = 1573084.0

	# run NN on input until desired APPROX ration reached
	while (round(length/denom, 2) >= APPROX):
		tempList = copy.deepcopy(inputCities) 
		length, tour = nearNeighbor(tempList)
		print ("Current tour Ratio: %.2f" % (round(length/denom, 2)))

	return length, tour




###################################################################
#  NNApprox
#  inputCities - list of city objects
#  Loops the nearNeighbor funciton a constant BEST amount of 
#  times, keeping the tour of shortest length. 
###################################################################
def NNApprox(inputCities):
	length = float("inf")
	
	for num in xrange(0, BEST):
		# copy the input list so we can alter it and then still have orig list
		tempList = copy.deepcopy(inputCities) 
		tempLength, tempTour = nearNeighbor(tempList)

		if tempLength < length:
			length = tempLength
			tour = tempTour
			print ("Found a better tour of length %d" % (length))

	return length, tour




###################################################################
#  NNTime
#  inputCities - list of city objects
#  Simply runs nearNeighbor once and returns the first solution
#  found.
###################################################################
def NNTime(inputCities):
	start = timer()
	length, tour = nearNeighbor(inputCities)
	end = timer()
	total = end - start
	print ("Running Time: ~%f seconds with a length of %d" % (total, length))
	
	return length, tour




###################################################################
#  nearNeighbor
#  inputCities - list of cities to evaluate
#  This function takes a list of cities and attempts to effeciently
#  solve the TSP for the list. At each step of the algorithm we 
#  evaluate, and go to the nearest neighbor of the current city.
#  Different starting locatins may result in differnt length tours.
#  function returns the length of the tour, and a in-order list of  
#  visited cities.
###################################################################
def nearNeighbor(inputCities):
	length = 0
	tour = []
	# find a random starting city
	curr = inputCities[random.randrange(0, len(inputCities))]
	tour.append(curr)
	inputCities.remove(curr)
	
	# until every city has been used in the tour
	while inputCities:
		# find the closest neighbor to the current city
		next, trav = findNext(curr, inputCities)
		tour.append(next)
		inputCities.remove(next)
		length += trav
		curr = next

	# add in the distance from the last city back to the first
	length += dist(tour[0], tour[len(tour) - 1])

	return length, tour




###################################################################
#  main
#  inFileName - name of the input file
#  First we process the input data and store that as inputCities.
#  We thne use inputcities adn inFileName to find the length and 
#  order of the appropriate tour based on the input file and if any 
#  optins are selected by the user. Finally we take the returned 
#  lenght and tour and create an output file to store the info.
###################################################################
def main(inFileName):
	inputCities = getInput(inFileName)
	length, tour = makeTour(inputCities, inFileName)
	makeOutput(length, tour, inFileName)




###################################################################
#  calls main with the name of the file to run TSP on
###################################################################
if __name__ == '__main__':
   main(sys.argv[1])