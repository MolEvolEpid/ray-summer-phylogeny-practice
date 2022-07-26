from b_prediction_accuracy import *

all_data = read_erik_sim_dir()
org_a, org_k = organize_data(all_data)

for a in sorted(org_a):
    print(f"a = {a}")
    for b in sorted(org_a[a]):
        trees = len(org_a[a][b])
        print(f"  b = {b} -> {trees} valid trees")

for k in sorted(org_k):
    print(f"k = {k}")
    for b in sorted(org_k[k]):
        trees = len(org_k[k][b])
        print(f"  b = {b} -> {trees} valid trees")
