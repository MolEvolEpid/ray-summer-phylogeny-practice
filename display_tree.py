from ete3 import Tree, NodeStyle, TreeStyle

def display_tree(tree):
    """
    Gets rid of those stupid little circles so I can see
    if the branches actually line up or not. Why is this such
    a pain?
    """
    ns = NodeStyle()
    ns["size"] = 0
    for n in tree.traverse():
        n.set_style(ns)
    tree.show()

