import random
from ete3 import TreeNode

class Generator:
	def __init__(self, n):
		self.nodes = []
		for i in range(n):
			self.nodes.append(TreeNode(name=random.choice(["A", "B"])))

	def step(self):
		if random.random() < 0.15:
			self.make_pair()

	def make_pair(self):
		pair = random.sample(self.nodes, k=2)
		parent = TreeNode()
		for child in pair:
			parent.add_child(child)
			self.nodes.remove(child)
		self.nodes.append(parent)

	def run(self):
		while len(self.nodes) > 1:
			self.step()
		return self.nodes[0]

if __name__ == '__main__':
	g = Generator(15)
	end = g.run()
	print(end)
	print(end.write(format=1))


