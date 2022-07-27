import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from new_optimization import *
from basic_optimization import error_hdi
from time_tree import TimeTree
from arviz import hdi

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

def plot_from_summary_csv():
    # Read the summary csv file into two dicts to be plotted
    changing_k = {}
    changing_a = {}
    with open("erik-sim/summary.csv", "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Typecast the relevant columns to be easier to work with
            for col in ['line', 'real_a', 'real_k', 'real_b', 'mle_b']:
                row[col] = float(row[col])
            row["success"] = bool(row["success"])

            # Convenience variables for the most important cols
            a = row["real_a"]
            k = row["real_k"]
            b = row["real_b"]
            mle_b = row["mle_b"]

            # Read the data into dictionaries. 
            # These won't work with more complex data, I'll need something more SQL-like
            for key, d in zip([a, k], [changing_a, changing_k]):
                if key in d:
                    if b in d[key]:
                        d[key][b].append(mle_b)
                    else:
                        d[key][b] = [mle_b]
                else:
                    d[key] = {b: [mle_b]}

    # Plot the data in those dicts
    k_fig, (k_ax1, k_ax2) = plt.subplots(1, 2)
    a_fig, (a_ax1, a_ax2) = plt.subplots(1, 2)

    for val, ax, d in zip([1, 5, 20, 100],
                          [a_ax1, a_ax2, k_ax1, k_ax2],
                          [changing_a, changing_a, changing_k, changing_k]):
        x = list(d[val].keys())
        all_mle = [d[val][n] for n in x]
        mean_mle = []
        error = []
        for points in all_mle:
            mean_mle.append(sum(points) / len(points))
            error.append(error_hdi(points))
        error = np.transpose(error)
        ax.errorbar(x, mean_mle, yerr=error, fmt='o')
        ax.plot(x, x)

        ax.set_yticks(x)
        ax.set_xticks(x)
        ax.set_xlabel("Simulated value of β")
        ax.set_ylabel("Mean MLE of β")


    k_ax1.set_title("α = 1, k = 20")
    k_ax2.set_title("α = 5, k = 20")
    a_ax1.set_title("α = 5, k = 20")
    a_ax2.set_title("α = 5, k = 100")

    k_fig.suptitle("β Prediction accuracy with different k")
    a_fig.suptitle("β Prediction accuracy with different α")

    plt.show()



def main():
    #calculate_all_sim_trees() # To write data to the file. Only do this once, it won't change
    plot_from_summary_csv()

if __name__ == '__main__':
    main()
