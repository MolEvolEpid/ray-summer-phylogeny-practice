import random
from ete3 import TreeNode

class TreeGenerator:
	def __init__(self, n):
		self.nodes = []
		for i in range(n):
			host = random.choice(["A", "B"])
			node = TreeNode(name=host)
			node.host = host
			node.time = 1
			self.nodes.append(node)

	def find_weighted_partner(self, node):
		"""
		Given a node, find the other possible nodes it is most likely
		to pair with. 
		A node is most likely to pair with one from its own host, then one of an 
		unknown host, then one of a different host.
		"""
		partners = [item for item in self.nodes if item != node]
		
		weights = []
		for partner in partners:
			if partner.host == "?": # undetermined host is a base case so it gets weight 1
				weights.append(1)
			elif partner.host == node.host: # same host is more likely
				weights.append(2)
			else: # different host is less likely
				weights.append(0.5)

		return random.choices(partners, weights=weights)[0]

	def intuitive_inheritance(self, child1, child2):
		"""
		Based on two child nodes, decide what host their parent is most
		likely to have.
		"""
		h1 = child1.host
		h2 = child2.host
		if h1 == h2:
			return h1
		elif h1 == "?":
			return h2
		elif h2 == "?":
			return h1
		else:
			return "?"

	def step(self):
		"""
		Take a timestep, randomly deciding whether to take any actions.
		At the moment this is redundant, but when time is a bigger factor
		it will be important that something does not necessarily happen
		at every timestep.
		"""
		if random.random() < 0.15:
			self.make_pair()

	def make_pair(self):
		"""
		Choose two nodes and combine their lineages at a common parent.
		That parent is then able to pair with other nodes.
		"""
		first = random.choice(self.nodes)
		second = self.find_weighted_partner(first)

		parent = TreeNode()
		parent.host = self.intuitive_inheritance(first, second)
		for child in [first, second]:
			parent.add_child(child)
			self.nodes.remove(child)

		self.nodes.append(parent)

	def run(self):
		"""
		Run the model until only one node is left and return that node.
		"""
		while len(self.nodes) > 1:
			self.step()
		return self.nodes[0]

if __name__ == '__main__':
	"""
	Run from the command line, prints an example tree with 15 nodes.
	"""
	g = TreeGenerator(15)
	end = g.run()
	print(end)
	#end.write(format=1, outfile="tests/output.nwk")

