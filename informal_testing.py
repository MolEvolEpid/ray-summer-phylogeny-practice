from tree_likelihood import * 
from time_tree import TimeTree

t = TimeTree("((D_2:1, D_3:1):2, (D_1:1.5, R_4:1.5):1.5);")
# Hmm, I wonder if T=0.0 will result in the same coal_D as the original list
# May be worth testing

t.populate_hosts({"D": 0, "R": 1})
before, after = divide_tree_at_time(t, 1.4)

for a in after:
    print(a)
    for l in a.get_leaves():
        print(l.host)

coal_D, coal_R, none_D, none_R = tree_segments_multihost(t, 1.4)

for name, l in zip(['coal_D', 'coal_R', 'none_D', 'none_R'],
                   [ coal_D,   coal_R,   none_D,   none_R]):
    print(f"{name}: {l}")
