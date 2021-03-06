from ete3 import Tree
import warnings

class TimeTree(Tree):
    def __init__(self, *args, **kwargs):
        # We need to take hosts out of kwargs before doing super.
        if "hosts" in kwargs:
            hosts = kwargs["hosts"]
            kwargs.pop("hosts")
        else:
            hosts = {}

        super(TimeTree, self).__init__(*args, **kwargs)

        self.populate_times()
        if hosts:
            self.populate_hosts(hosts)

    def populate_times(self):
        """
        Add a time attribute to each node based on its distance from the tips
        of the tree (lower is more recent)
        """
        tree_max = self.get_farthest_node()[1]
        for node in self.traverse():
            node_dist = self.get_distance(node)
            node.add_feature("time", tree_max - node_dist)

    def populate_hosts(self, hostnames):
        """
        Add a host attribute to each leaf in the tree. If no host could be determined,
        a warning will be raised and the host will be set to -1.

        Parameters:
          hostnames (dict): A dict associating the first part of a
          leaf's name and the number of its host.
            ex. {"D": 0, "R": 1} gives the node with name="R_5" host=1

        Returns:
          nothing. Modifies the nodes of the TimeTree object.
        """
        for leaf in self.iter_leaves():
            name_prefix = leaf.name.split('_')[0]
            try:
                leaf.host = hostnames[name_prefix]
            except KeyError:
                warnings.warn(f"Could not find a host for name_prefix {name_prefix} in {hostnames}")
                leaf.host = -1

    def get_leaf_hosts(self):
        """
        For each leaf in the tree, get the host value.
        """
        leaf_hosts = []
        for node in self.traverse():
            if node.is_leaf():
                leaf_hosts.append(node.host)
        return leaf_hosts

    def all_hosts_infected_node(self):
        """
        Return the earliest node where all hosts have been infected.
        """
        hosts_overall = set(self.get_leaf_hosts())
        hosts_so_far = set()
        # check from the closest (oldest) leaf to the newest one
        for leaf in sorted(self.get_leaves(), key=lambda x: x.time, reverse=True):
            hosts_so_far.add(leaf.host)
            if hosts_overall == hosts_so_far:
                return leaf
        raise Exception("Could not find any point where all hosts were infected.")

    def get_mixed_nodes(self):
        """
        Return a list of all nodes in the tree with children that have multiple hosts.
        """
        mixed = []
        for node in self.traverse():
            if len(set(node.get_leaf_hosts())) > 1: # TODO: instead of leaf names must be leaf hosts
                mixed.append(node)
        return mixed

    def most_recent_mixed_node(self):
        """
        Find the most recent node with children that have multiple hosts.
        """
        latest_possible = self.all_hosts_infected_node()
        recent = self
        mixed_nodes = self.get_mixed_nodes()
        if mixed_nodes:
            for node in self.get_mixed_nodes():
                if node.time < recent.time and node.time > latest_possible.time:
                    recent = node
            return recent
        else:
            raise Exception("There are no mixed nodes on the tree.")

    def split_at_time(self, T):
        """
        Return two parts of the tree: Those before T and those after.

        Parameters:
          T (float): Time to split around

        Returns:
          before (TimeTree): All branches before T
          after (list): All branches after T. There can be multiple branches separated.
        """
        before = self.copy()

        after = []
        for node in before.iter_descendants():
            start = node.time
            end = node.up.time

            if start < T <= end: # We're on the boundary.
                # Detach the node from the base tree
                parent = node.up # Detach the node from the base tree
                after_T = node.detach()

                # Add that node to the new list of nodes after T
                after_T.dist = T-start
                after.append(after_T)

                # Clean up the parent so the distances still match
                parent.add_child(dist=end-T)

        return before, after

    def get_k(self, host, time):
        """
        Determine the value of k for a certain host at a specific point in time.

        If the first coalescence event has not yet happened (e.g. at the tips), k
        is equal to the number of tips with the appropriate host.
        At any other point, k is equal to the number of branches that pass through
        that time.

        Parameters:
          tree (TimeTree): Representation of tree
          host (int): Integer representation of host, usually 0 or 1.
          time (float): Time to count k.

        Returns:
          k (int): k at that time
        """
        # Earliest coalescence in the tree. Host shouldn't matter, as we just want
        # a small time value that's appropriate to the tree.
        # TODO this will *REALLY* break if we have tips at different times. Be careful about that.
        node_times = [node.time for node in self.traverse() if node.children]
        cutoff_time = min(node_times)

        if time < cutoff_time:
            # k is the number of leaves if we're before the first coalescence event
            k = len([leaf for leaf in self.get_leaves() if leaf.host == host])
        else:
            # k is the number of branches that cross the time at any other point
            k = 0
            for node in self.iter_descendants():
                start = node.time
                end = node.up.time
                if end <= time <= start:
                    k += 1
        return k

