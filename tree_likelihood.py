#!/usr/bin/env python3

from population_models import con_probability, lin_probability, exp_probability
from time_tree import TimeTree 

t = TimeTree("((A:1, B:1):2, C:3);")

def closest_parent_node(time, tree):
    """
    Return the next closest node backwards from the specified time.
    (for instance, the next node inwards from the leaves at time 0)
    """
    closest_node = tree # the root has the highest time so will always be replaced if possible
    for node in tree.traverse():
        # Any candidates need to be:
        #     Sooner than the current best time
        #     Later than the target time
        #     Have children (not be a leaf)
        if node.time < closest_node.time and node.time > time and node.children:
            closest_node = node
    return closest_node

# okay, what needs to happen?
# find the k and n and t of a certain bit of the tree (and assume for now it's constant pop)
