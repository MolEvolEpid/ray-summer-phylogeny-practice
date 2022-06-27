#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import random
import math
import sys

def count_faces(string):
    """
    Given a string of space-separated letters, count 
    the number of times "H" and "T" occur
    """
    heads = tails = 0
    for face in string.split():
        if face.lower() == "h":
            heads += 1
        elif face.lower() == "t":
            tails += 1
    return heads, tails

def likelihood(p, heads, tails):
    """
    Calculate the likelihood of a certain p (0 to 1, exclusive) 
    based on observed numbers of heads and tails. 
    """
    bc = math.factorial(heads + tails) / (math.factorial(heads) * math.factorial(tails)) 
    return bc * pow(p, heads) * pow(1-p, tails)

def high_low_ci(heads, tails):
    """
    Use fisher information to find the high and low confidence intervals
    for the log likelihood, then convert these values back into likelihood.
    Statistical reference from Slavković (n.d.)
        http://personal.psu.edu/abs12/
    """
    p_sample = heads / (heads + tails)
    fisher_info = (heads + tails) * p_sample * (1 - p_sample)

    phi_hat = np.log(p_sample / (1 - p_sample))
    confidence_interval = 1.96 * math.sqrt(1 / fisher_info)
    phi_low = phi_hat - confidence_interval
    phi_high = phi_hat + confidence_interval

    low_ci = math.pow(math.e, phi_low) / (1 + math.pow(math.e, phi_low))
    high_ci = math.pow(math.e, phi_high) / (1 + math.pow(math.e, phi_high))
    return low_ci, high_ci

def likelihood_curve(heads, tails):
    """
    Given a number of heads and tails, construct a curve showing
    the log likelihood of p between 0 and 1.
    """
    x = np.linspace(0, 1, 1000, endpoint=False)[1:] 
    y = []
    for p in x:
        y.append(likelihood(p, heads, tails)) 
    return x, y

def plot_likelihood(heads, tails):
    """
    Plot the likelihood curve of p based on the number of heads
    and tails and highlight the 95% confidence interval of the 
    curve.
    """
    p_sample = heads / (heads + tails)
    x, y = likelihood_curve(heads, tails)
    low_ci, high_ci = high_low_ci(heads, tails)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(x, y, c="black")
    ax.set_xlabel("p value")
    ax.set_ylabel("likelihood")
    ax.set_title("95% Confidence Interval of p")
    ax.fill_between(x, 0, y, where=(np.array(x) > low_ci) & (np.array(x) < high_ci), facecolor="lightgreen")
    ax.axvline(x=p_sample, color="blue", linestyle="--")

    plt.xticks(np.arange(0, 1.01, 0.10))
    plt.ylim(0, max(y) + 0.01) 
    plt.show()

def generate_sequence(p, n):
    """
    Generate a sequence of n length, where p is the probability
    to get a head when flipping the coin.
    """
    heads = tails = 0
    tails = 0
    for i in range(n):
        if random.random() <= p:
            heads += 1
        else:
            tails += 1
    if heads == 0: # A lot of these stats break if either value is zero
        heads += 1
        tails -= 1
    elif tails == 0:
        tails += 1
        heads -= 1
    return heads, tails


if __name__ == "__main__":
    try:
        p = float(sys.argv[1])
        n = int(sys.argv[2])
        heads, tails = generate_sequence(p, n)
    except ValueError:
        heads, tails = count_faces(sys.argv[1])
        if heads + tails == 0:
            raise Exception("Make sure your input string is made of H and T, separated by spaces")
    except IndexError:
        raise Exception("Make sure to run the script with arguments!\nYou can either provide a string of H's and T's or two numbers representing p and n.")

    plot_likelihood(heads, tails)

