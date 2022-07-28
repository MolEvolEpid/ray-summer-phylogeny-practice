from tree_likelihood import tree_segments, tree_segments_multihost
from time_tree import TimeTree

t = TimeTree("((D_1:1, D_2:1):3, (R_3:2, R_4:2):2);")
# Hmm, I wonder if T=0.0 will result in the same coal_D as the original list
# May be worth testing

coal_D, coal_R, none_D, none_R = tree_segments_multihost(t, 3.)

for name, l in zip(['coal_D', 'coal_R', 'none_D', 'none_R'],
                   [ coal_D,   coal_R,   none_D,   none_R]):
    print(f"{name}: {l}")
