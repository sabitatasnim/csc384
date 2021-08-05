#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the addproblem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

import queue
from typing import final
from cspbase import Constraint


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    contraints = None
    pruned = []

    # Check if the new variable exists, if it does, get all constraints with the newVar
    if newVar is not None:
        contraints = csp.get_cons_with_var(var = newVar)
    else:
        contraints = csp.get_all_cons()

    # Go through the constraints but we need to get the constraints with only one unassigned values for FC
    for constraint in contraints:
        if constraint.get_n_unasgn() == 1:
            # using the first index because we have only one unassigned variable for FC
            unassigned_var = constraint.get_unasgn_vars()[0] 

            # Must create a list of values, one for each variable in the constraints scope for the constraint.check() method 
            scope_vals = []
            unassigned_index = 0
            # Need to enumerate in order to keep track of the indexes of the contraint.scope() list of variables to test ONLY THE PLACE OF the unassigned variable 
            # in the current domain
            for i, variable in enumerate(constraint.get_scope()):
                # Checking if the value is already assigned to the 
                if variable.get_assigned_value() is not None:
                    scope_vals.append(variable.get_assigned_value())
                if variable == unassigned_var:
                    unassigned_index = i
                    # Placeholder for now until we assign a domain value from the current domain of the unassigned value later on
                    scope_vals.append(None)

            # check FC for each constraint in the current domain
            for domain_value in unassigned_var.cur_domain():
                # Test all domain value with the constraint scope values to check if it satifies the constraint
                scope_vals[unassigned_index] = domain_value
                if not constraint.check(vals=scope_vals):
                    # Now we know we have to prune this value and add it to the list of (var, val) tuples
                    unassigned_var.prune_value(domain_value)
                    # Add to the pruned list
                    pruned.append((unassigned_var, domain_value))

            # Check for a domain wipeout now (DWO)
            if unassigned_var.cur_domain_size() == 0:
                return False, pruned
        else:
            continue
    
    return True, pruned

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT

    contraints = None
    pruned = []
    queue_gac = queue.Queue() #Using a list as a queue not familiar with the queue library

    # Check if the new variable exists, if it does, get all constraints with the newVar (same as FC)
    # Put these contraints into the queue directly 
    if newVar is not None:
        for constraint in csp.get_cons_with_var(var = newVar):
            queue_gac.put(constraint)
    else:
        for constraint in csp.get_all_cons():
            queue_gac.put(constraint) 

    ############# GAC ENFORCE (implemented from lecture slides) ###################
    # Ensuring the queue is actually not empty
    while queue_gac.empty() is not True:
        # take out and return the first element in the list
        constraint = queue_gac.get(0) 
        # Going through the scope of the constraint 
        for variable in constraint.get_scope():
            for domain_value in variable.cur_domain():
                if constraint.has_support(var=variable, val=domain_value) is not True:
                    # Prune variable, values that does not work for constraint
                    pruned.append((variable, domain_value))
                    variable.prune_value(domain_value)

                    # Domain Wipeout (DWO)
                    if variable.cur_domain_size() == 0:
                        return False, pruned
                    else:
                        # Pushing all constraints C' so that variables within the scope of C' 
                        for c_prime in csp.get_cons_with_var(var=variable):
                            # Checking if C' is not in the queue already to add to the queue
                            if c_prime not in queue_gac.queue:
                                queue_gac.put(c_prime)

    return True, pruned

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    final_mrv = None
    mrv = float("inf")
    unassigned_vars = csp.get_all_unasgn_vars()

    for v in unassigned_vars:
        if v.cur_domain_size() < mrv:
            mrv = v.cur_domain_size()
            final_mrv = v

    return final_mrv

	