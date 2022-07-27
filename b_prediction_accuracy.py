import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from population_models import *
from tree_likelihood import *
from new_optimization import *
from time_tree import TimeTree

def calculate_all_sim_trees():
    """
    For every tree in erik-sim, calculate the MLE and compare it to the actual value.
    
    Write these results to a csv file.
    """
    with open("erik-sim/summary.csv", "w") as outfile:
        # Initialize CSV file overwriting any previous data
        fieldnames = ['file', 'line', 'real_a', 'real_k', 'real_b', 'mle_b', 'success']
        writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()

        # Read trees within each directory
        to_read = sorted([s for s in os.listdir("erik-sim") if s[-4:] != ".csv"]) # Do not read csv files. Very bootleg.
        for dirname in to_read: 
            real_a, real_k, real_b = [float(term[1:]) for term in dirname.split("_")] # "a5_k100_b4" -> [5.0, 100.0, 4.0]
            treefile = ("erik-sim/" + dirname + "/trees.tre")
            with open(treefile) as f:
                print(f"Calculating trees from {treefile}...")
                # Filter trees by those that do not have invalid root times.
                # Will introduce bias in the data, especially for higher b.
                all_data = [TimeTree(l) for l in f.readlines()]
                valid_lines, valid_data = [], []
                for i, t in enumerate(all_data):
                    if t.time <= 2*(365/1.5): # Hardcoded time of I
                        valid_lines.append(i)
                        valid_data.append(t)
                valid_lines = valid_lines[:100]
                valid_data = valid_data[:100]

                # For each valid tree, record it into the data file.
                for line, tree in zip(valid_lines, valid_data):
                    res = optimize_b(tree, real_a, 2*(365/1.5))
                    writer.writerow({'file': treefile,
                                     'line': line+1,
                                     'real_a': real_a, 
                                     'real_k': real_k, 
                                     'real_b': real_b, 
                                     'mle_b': res.x,
                                     'success': res.success})

def b_prediction_accuracy(org_a, org_k):
    """
    First, plot the b predictions if we fix k and vary alpha.

    Then, plot the b predictions if we fix alpha and vary k.
    """
    # Initialize figures
    a_fig, ((a_ax1, a_ax2), (a_ax3, a_ax4)) = plt.subplots(2, 2)
    k_fig, ((k_ax1, k_ax2), (k_ax3, k_ax4)) = plt.subplots(2, 2)

    for a in org_a:
        for b in org_a[a]:
            pass # THIS ISN'T DONE YET, SORRY FOR ANY CONFUSION


def main():
    calculate_all_sim_trees()

if __name__ == '__main__':
    main()
