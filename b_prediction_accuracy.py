import numpy as np
import os
import matplotlib.pyplot as plt
from population_models import *
from tree_likelihood import *
from basic_optimization import *
from time_tree import TimeTree

def read_erik_sim_dir(): # TODO I broke this whole thing didn't I lol love it
    """
    Read the 'trees.tre' file in every subdirectory of erik-sim.

    Very hardcoded. Be careful that you run from the same directory
    as this file.
    """
    all_data = {}
    for dirname in os.listdir("erik-sim"):
        print(f"Now reading {dirname}")
        treefile = ("erik-sim/" + dirname + "/trees.tre") # bootleg but it'll do
        with open(treefile) as f:
            trees = [TimeTree(l) for l in f.readlines()]
            all_data[dirname] = [t for t in trees if t.time <= 2*(365/1.5)] # Also hard coded. Filter out "invalid" trees.
    return all_data

def organize_data(data):
    organized_a = {}
    organized_k = {}
    for key in data:
        a = int(key[1:2])
        k = int(key[4:6])
        b = int(key[8:])
        
        if a in organized_a:
            if b in organized_a[a]:
                organized_a[a][b] += data[key]
            else:
                organized_a[a][b] = data[key]
        else:
            organized_a[a] = {}
            organized_a[a][b] = data[key]
        
        if k in organized_k:
            if b in organized_k[k]:
                organized_k[k][b] += data[key]
            else:
                organized_k[k][b] = data[key]
        else:
            organized_k[k] = {}
            organized_k[k][b] = data[key]

    return organized_a, organized_k

def b_prediction_accuracy(org_a, org_k):
    """
    First, plot the b predictions if we fix k and vary alpha.

    Then, plot the b predictions if we fix alpha and vary k.
    """
    # Initialize figures
    a_fig, ((a_ax1, a_ax2), (a_ax3, a_ax4)) = plt.subplots(2, 2)
    k_fig, ((k_ax1, k_ax2), (k_ax3, k_ax4)) = plt.subplots(2, 2)

    for a in org_a:
        for b in a:
            pass # THIS ISN'T DONE YET, SORRY FOR ANY CONFUSION


def main():
    all_data = read_erik_sim_dir()
    org_a, org_k = organize_data(all_data)
    b_prediction_accuracy(org_a, org_k)

if __name__ == '__main__':
    main()
