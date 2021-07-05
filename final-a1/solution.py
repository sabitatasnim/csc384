#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os

from scipy.optimize.optimize import wrap_function #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems
import math
import csv
import numpy as np
# from scipy.optimize import linear_sum_assignment

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    # Define Manhattan distance total sum 
    manhattan_dist = 0

    #Must iterate through all the boxes to find nearest storage point
    for box in state.boxes:  # Go through all the boxes
      all_distances = []
      if box not in state.storage: # check if box is not already in storage
        for storage in state.storage: # go through the storage spots as well
          all_distances.append(abs(box[0] - storage[0]) + abs(box[1] - storage[1]))
        
        all_distances.sort() # Sort to find the min value
        manhattan_dist += all_distances[0] # Get the manhattan distance sums from the first value in the array

    return manhattan_dist


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count
    

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''

    total_manhattan = 0 

    # Define all the constant variables
    INF = float('inf')

    # convert all the items in the state to a list for easier use 
    boxes = list(state.boxes)
    storages = list(state.storage)
    obstacles = list(state.obstacles)

    # Get a set of all boxes and obstacles to check for corners with boxes and obstacles 
    box_and_obs = boxes + obstacles
    #box_and_obs = list(box_and_obs)

    # Need this to help pass certain cases where we need to check if certain storage coordinates are blocked
    storage_x = []
    storage_y = []

    # NEED SEPERATE COORDINATES FOR EDGES 
    for storage in storages:
      x, y = storage
      storage_x.append(x)
      storage_y.append(y)

    # NEED TO KEEP TRACK OF ALL THE USED STORAGE SPACES SO WE DON'T USE IT AGAIN
    used_storage = []
    
    for box in boxes:
      box_and_obs.remove(box)
      box_to_goal_dist = {}
      rob_to_box_dist = []

      # DEFINE THE WALL COORDINATES
      left_wall = box[0] == 0
      right_wall = box[0] == state.width - 1
      top_wall = box[1] == 0
      bottom_wall = box[1] == state.height - 1


      # CHECK IF BOX AT EDGE AND A STORAGE SPOT ISNT AT AN EDGE
      if(left_wall and (0 not in storage_x)):
        return INF
      elif(right_wall and(state.width - 1 not in storage_x)):
        return INF
      elif(top_wall and (0 not in storage_y)):
        return INF
      elif(bottom_wall and (state.height - 1 not in storage_y)):
        return INF

      # DEFINE THE OBSTACLES/BOXES IN THE X DIRECTIONS AND Y DIRECTIONS
      x_dir = (box[0] - 1, box[1]) in box_and_obs or (box[0] + 1, box[1]) in box_and_obs
      y_dir = (box[0], box[1] - 1) in box_and_obs or (box[0], box[1] + 1) in box_and_obs

      # Define the vertical or horizontal items regardless of it being a wall or obstacle next to the box
      x_items = left_wall or right_wall or x_dir
      y_items = top_wall or bottom_wall or y_dir

      #CHECK CORNERS TO CHECK IF WE HAVE CORNERS WITH BOXES/OBSTACLES/WALLS
      if(x_items and y_items and box not in storages):
        return INF
      
      # GET DISTANCES FROM STORAGE SPOTS TO BOXES AND ENSURE STORAGE NOT TAKEN
      for storage in storages:
        if(storage not in used_storage):
          box_to_goal_dist[storage] = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
      
      # GET THE SHORTEST DISTANCE STORAGE LOCATION FROM THE CURRENT BOX AND THEN ADD TO TAKEN STORAGE LOCATIONS
      closest_key = min(box_to_goal_dist, key=box_to_goal_dist.get)
      used_storage.append(closest_key)

      # GET DISTANCES FROM THE ROBOTS TO THE BOX TO TAKE THE DISTANCE TRAVELLED FROM ROBOT TO BOX BEFORE PUSHING
      for robot in state.robots:
        rob_to_box_dist.append(abs(box[0] - robot[0]) + abs(box[1] - robot[1]))
      rob_to_box_dist.sort()
      
      # added smallest distances to the min distance between either the robot to box distance or the box to goal distance and then multiply by 0.6 it to ensure admisabllity
      total_manhattan += (box_to_goal_dist[closest_key] + min(box_to_goal_dist[closest_key], rob_to_box_dist[0])*0.6)
      
      box_and_obs.append(box)
  
    return total_manhattan
        
def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the standard form of weighted A* (i.e. g + w*h)

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight*sN.hval

def fval_function_XUP(sN, weight):
#IMPLEMENT
    """
    Another custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the XUP form of weighted A* 

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    # f(node) = (1/(2*w))*(g(node) + h(node) + sqrt((g(node)+h(node))2 + 4*w*(w-1)*h(node)2 ))
    xup = (1/(2*weight))*(sN.gval + sN.hval + math.sqrt((sN.gval + sN.hval)**2 + 4*weight*(weight-1)*sN.hval**2))
    return xup

def fval_function_XDP(sN, weight):
#IMPLEMENT
    """
    A third custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the XDP form of weighted A* 

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    #f(node) = (1/(2*w))*(g(node)+(2*w-1)*h(node)+sqrt((g(node)-h(node))2 +4*w*g(node)*h(node))
    xdp = (1/(2*weight))*(sN.gval + (2*weight - 1)*sN.hval + math.sqrt((sN.gval - sN.hval)**2 + 4*weight*sN.gval*sN.hval))
    return xdp

def compare_weighted_astars():
#IMPLEMENT
    '''Compares various different implementations of A* that use different f-value functions'''
    '''INPUT: None'''
    '''OUTPUT: None'''
    """
    This function should generate a CSV file (comparison.csv) that contains statistics from
    4 varieties of A* search on 3 practice problems.  The four varieties of A* are as follows:
    Standard A* (Variant #1), Weighted A*  (Variant #2),  Weighted A* XUP (Variant #3) and Weighted A* XDP  (Variant #4).  
    Format each line in your your output CSV file as follows:

    A,B,C,D,E,F

    where
    A is the number of the problem being solved (0,1 or 2)
    B is the A* variant being used (1,2,3 or 4)
    C is the weight being used (2,3,4 or 5)
    D is the number of paths extracted from the Frontier (or expanded) during the search
    E is the number of paths generated by the successor function during the search
    F is the overall solution cost    

    Note that you will submit your CSV file (comparison.csv) with your code
    """
    # Define my field names (A, B, C, D, E, F)
    field_names = ['A', 'B', 'C', 'D', 'E', 'F']

    # Define File name 
    file_name = "comparison.csv"

    # Start writing to the csv file
    with open(file_name, 'w') as csvfile:
      writer_csv = csv.writer(csvfile)
      writer_csv.writerow(field_names)

      for i in range(0,3):
          problem = PROBLEMS[i] 
          # Using search engine to get the Standard A*
          search_eng = SearchEngine(strategy="astar")
          search_eng.init_search(initState=problem, goal_fn=sokoban_goal_state, heur_fn=heur_manhattan_distance, fval_function= lambda sN: fval_function(sN, 1))
          solution, stats = search_eng.search(timebound=5)
          # [A, B, C, D, E, F]
          writer_csv.writerow([i, 1, 1, stats.states_expanded, stats.states_generated, solution.gval])

          for weight in [2,3,4,5]:
            #you can write code in here if you like
            # Using search engine to get the Weighted A*
            search_eng = SearchEngine(strategy="custom")
            search_eng.init_search(initState=problem, goal_fn=sokoban_goal_state, heur_fn=heur_manhattan_distance, fval_function= lambda sN: fval_function(sN, weight))
            solution, stats = search_eng.search(timebound=5)
            # [A, B, C, D, E, F]
            row_astar = [i, 2, weight, stats.states_expanded, stats.states_generated, solution.gval]
            writer_csv.writerow(row_astar)

            # Using search engine to get the Weighted A* XUP
            search_eng = SearchEngine(strategy="custom")
            search_eng.init_search(initState=problem, goal_fn=sokoban_goal_state, heur_fn=heur_manhattan_distance, fval_function= lambda sN: fval_function_XUP(sN, weight))
            solution, stats = search_eng.search(timebound=5)
            # [A, B, C, D, E, F]
            row_astar_xup = [i, 3, weight, stats.states_expanded, stats.states_generated, solution.gval]
            writer_csv.writerow(row_astar_xup)

            # Using search engine to get the Weighted A* XDP
            search_eng = SearchEngine(strategy="custom")
            search_eng.init_search(initState=problem, goal_fn=sokoban_goal_state, heur_fn=heur_manhattan_distance, fval_function= lambda sN: fval_function_XDP(sN, weight))
            solution, stats = search_eng.search(timebound=5)
            # [A, B, C, D, E, F]
            row_astar_xdp = [i, 4, weight, stats.states_expanded, stats.states_generated, solution.gval]
            writer_csv.writerow(row_astar_xdp)
            pass

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''

    # Define constant INF
  INF = float("inf")
  # Initalize costbound to be at INFINITY and best solution
  costbound = (INF, INF, INF)
  best_solution = False 
  # 15 with weight 6 and fval funct
  weight = 6
  # Wrapper function
  wrapper_func = lambda sN: fval_function(sN, weight)

  # Call on the SearchEngine Class 
  search_eng = SearchEngine('custom', 'full')
  # Run the search 
  search_eng.init_search(initState=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=wrapper_func)

  # Get the start time and completion time
  start_time = os.times()[0]
  completion_time = start_time + timebound

  # Keep searching before the timebound 
  while (os.times()[0] < completion_time):
    # Get the new timebound to update it
    # start_time = os.times()[0]
    new_solution, _ = search_eng.search(completion_time - os.times()[0], costbound)
    # time_taken = os.times()[0] - start_time
    # timebound -= time_taken
    if(new_solution):
      costbound = (new_solution.gval, INF, INF)
      best_solution = new_solution
    else:
      break 
  return best_solution

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime greedy best-first search'''
  # TO PRUNE STATES BASED ON costbound[0] FOR GREEDY BEST FIRST SEARCH 

  # Define constant INF
  INF = float("inf")

  # Initalize costbound to be at INFINITY and best solution
  costbound = (INF, INF, INF)
  best_solution = False 

  # Call on the SearchEngine Class 
  search_eng = SearchEngine('best_first', 'full')
  # Run the search 
  search_eng.init_search(initState=initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=None)

  # Get the start time and completion time
  start_time = os.times()[0]
  completion_time = start_time + timebound

  # Get the goal state of the first solution 
  #solution, _ = search_eng.search(timebound)

  # Keep searching before the timebound 
  while (start_time <= completion_time):
  #while(timebound > 0):
    #if(solution):
    # Get the new timebound to update it
    start_time = os.times()[0]
    #completion_time = start_time + timebound
    new_solution, _ = search_eng.search(timebound, costbound)
    time_taken = os.times()[0] - start_time
    timebound -= time_taken
    if(new_solution):
      costbound = (new_solution.gval, INF, INF)
      best_solution = new_solution
    else:
      break 
  return best_solution

