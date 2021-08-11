#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools
'''
* Need to extract variables in order to use for other functions creating a list of lists in order to map coordinates to the futo grid
* Dealing with the row/col constraints are much easier to iterate though as an array (without the binary inequality constraints)
* Return type for the models are also arrays
'''
def extract_variables(futo_grid):
    # we know that the futo grid is n x n 
    n = len(futo_grid)
    # the number of coloumns in a row 
    col = n + n - 1
    # The indices of the variables only so we can save those indices for later in the string
    var_indices = range(0, col, 2)

    # create the domain for the variables 1 to n inclusive 
    domain = range(1,n+1)
    domain = list(domain)
    
    # board_1 = [[1,'<',0,'.',0],[0,'.',0,'.',2],[2,'.',0,'>',0]]

    variable_array = []
    variable_list = []
    # create the list of lists with only the variables but not the lists 
    for i in range(n):
        #variable_row = []
        for j in var_indices:
            variable = None
            value = futo_grid[i][j]
            var_name = "var " + str(i) + " " + str(j)

            # Need to check if our futo grid value is actually 0 or not because need to assign the domain based on that
            if value == 0:
                # Save the indices of the variable with each name so it's easier to find the location of each variable in the futo grid 
                variable = Variable(name=var_name, domain=domain)
            else:
                variable = Variable(name=var_name, domain=[value])
            variable_list.append(variable)

    # Turn the list into an array 
    variable_array = [variable_list[i : i+n] for i in range(0, len(variable_list), n)]

    # Returns both variable array (return type for model + for easier tracking for adding row/col constraints + mapping to the futo_grid) and variable list for the csp
    return variable_array, variable_list

'''
####################### Binary not equal constraints for the row and column constraints ########################

'''
def add_binary_row_and_col_constraints_to_csp(futo_grid, variables_array, csp, is_row):
    # Find size of futo grid 
    n = len(futo_grid)

    for i in range(n):
        # THIS IS NEEDED TO ENSURE THAT WE ARE TAKING INTO ACCOUNT THE ROW/COL CONSTRAINTS (EVERY POSSIBLE COMBINATION) but in pairs 
        for j, k in itertools.combinations(range(n), 2):
            constraint = None
            satisfying_tuples_list = []
            # Check if it's a row constraint
            if is_row:
                var_left = variables_array[i][j]
                var_right = variables_array[i][k]
                c_name = "row constraint: " + str(i) + " " + str(j) + " and " + str(i) + " " + str(k) 
            else:
                var_left = variables_array[j][i]
                var_right = variables_array[k][i]
                c_name = "col constraint: " + str(j) + " " + str(i) + " and " + str(k) + " " + str(i) 

            # Define the scope after finding the variables on the left and right 
            scope = [var_left, var_right]
            # Compile all the satisfying tuples for the constraints
            for val_left in var_left.cur_domain():
                for val_right in var_right.cur_domain():
                    if val_left != val_right:
                        pair = (val_left,val_right)
                        satisfying_tuples_list.append(pair)
            
            constraint = Constraint(name=c_name, scope=scope)

            # Finally add all the satifying tuples to the constraint
            constraint.add_satisfying_tuples(tuples=satisfying_tuples_list)

            # Then add the constraints to the csp
            csp.add_constraint(c=constraint)

'''
########################### n-ary all-different constraints for the row and column constraints ###########################

'''
def add_nary_row_col_contraints_to_csp(futo_grid, variables_array, csp, is_row):
    # Find size of futo grid 
    n = len(futo_grid)

    for i in range(n):
        constraint = None
        satisfying_tuples_list = []
        constraint_domain = []


        # Check if we have a row constraint
        if is_row:
            # Get all the row domains in a list of list to pass into itertools
            for d in variables_array[i]:
                constraint_domain.append(d.cur_domain())
            c_name = "all-diff row constraint at row: " + str(i)
            scope = variables_array[i]

        # Check if have a column constraint
        else:
            # Getting col domains require us to parse a different row but same column 
            col_variables = list(map(lambda x : x[i], variables_array))
            for d in col_variables:
                constraint_domain.append(d.cur_domain())
            c_name = "all-diff col constraint at col: " + str(i)
            scope = col_variables

        for product in itertools.product(*constraint_domain):
            if len(product) == len(set(product)) and len(product) == n: 
                satisfying_tuples_list.append(product)

        constraint = Constraint(name=c_name, scope=scope)

        # Finally add all the satifying tuples to the constraint
        constraint.add_satisfying_tuples(tuples=satisfying_tuples_list)

        # Then add the constraints to the csp
        csp.add_constraint(c=constraint)

def add_binary_inequality_constraints_to_csp(futo_grid, variables_array, csp):
    # need to find the size of the futo grid again
    n = len(futo_grid)

    for i in range(n):
        for j in range(n - 1): # n - 1 to prevent unacessed variables in right variable
            var_left = variables_array[i][j]
            var_right = variables_array[i][j+1]
            # This is where the mapping from the n x n variable array is being used hence needing an array for variables
            ineq_constraint = futo_grid[i][2*j+1]
            constraint = None
            # Define the scope of the constraint to put into the constraint
            scope = [var_left, var_right]
            satisfying_tuples_list = []
            
            # Check if we have a greater than constraint 
            if ineq_constraint == ">":
                # Compile all the satisfying tuples for the constraints
                for val_left in var_left.cur_domain():
                    for val_right in var_right.cur_domain():
                        if val_left > val_right:
                            pair = (val_left,val_right)
                            satisfying_tuples_list.append(pair)
                
                # Now create the constraint
                c_name = "constraint: > " + str(i) + " " + str(j)
                constraint = Constraint(name=c_name, scope=scope)

            # Check if we have a less than constraint   
            elif ineq_constraint == "<":
                # Compile all the satisfying tuples for the constraints
                for val_left in var_left.cur_domain():
                    for val_right in var_right.cur_domain():
                        if val_left < val_right:
                            pair = (val_left,val_right)
                            satisfying_tuples_list.append(pair)
                
                # Now create the constraint
                c_name = "constraint: < " + str(i) + " " + str(j)
                constraint = Constraint(name=c_name, scope=scope)

            # Check if we have no constraint 
            else:
                continue

            # Finally add all the satifying tuples to the constraint
            constraint.add_satisfying_tuples(tuples=satisfying_tuples_list)

            # Then add the constraints to the csp
            csp.add_constraint(c=constraint)

# board_1 = [[1,'<',0,'.',0],[0,'.',0,'.',2],[2,'.',0,'>',0]]
# a, b= extract_variables(board_1)


def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    variables_array = []
    variables_list = []
    csp_model1 = None
    # Get the variables first as an array and as a list
    variables_array, variables_list = extract_variables(futo_grid=futo_grid)

    # Create the CSP for this model
    csp_model1 = CSP(name="CSP: Model 1 - Binary Constraints only", vars=variables_list)

    # Add the row and column constraints
    # ROW CONSTRAINTS (is_row=True)
    add_binary_row_and_col_constraints_to_csp(futo_grid, variables_array, csp_model1, True)

    # COL CONSTRAINTS (is_row=False)
    add_binary_row_and_col_constraints_to_csp(futo_grid, variables_array, csp_model1, False)

    # Add the inequality constraints as well
    add_binary_inequality_constraints_to_csp(futo_grid, variables_array, csp_model1)

    return csp_model1, variables_array

def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT 
    variables_array = []
    variables_list = []
    csp_model2 = None
    # Get the variables first as an array and as a list
    variables_array, variables_list = extract_variables(futo_grid=futo_grid)

    # Create the CSP for this model
    csp_model2 = CSP(name="CSP: Model 2 - N-ary Constraints", vars=variables_list)

    # Add the row and column constraints
    # ROW CONSTRAINTS (is_row=True)
    add_nary_row_col_contraints_to_csp(futo_grid, variables_array, csp_model2, True)

    # COL CONSTRAINTS (is_row=False)
    add_nary_row_col_contraints_to_csp(futo_grid, variables_array, csp_model2, False)

    # Add the inequality constraints as well
    add_binary_inequality_constraints_to_csp(futo_grid, variables_array, csp_model2)


    return csp_model2, variables_array
   
# board_1 = [[1,'<',0,'.',0],[0,'.',0,'.',2],[2,'.',0,'>',0]]
# print(futoshiki_csp_model_1(board_1))