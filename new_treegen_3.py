import random
from time_tree import TimeTree

class Generator:
	def __init__(self, tree, n):
		self.tree = tree
		# self.leaves = []
		for i in range(n):
			child = self.tree.add_child(name=random.choice(["A", "B"]), dist=10)
			# self.leaves.append(child) # TODO: Do I need this or not?

	def step(self):
		if random.random() < 0.15:
			self.make_pair()

	def make_pair(self):
		pair = random.sample(self.tree.get_children(), k=2)
		new_dist = pair[0].dist - 1
		branch = self.tree.add_child(dist=new_dist)
		for child in pair:
			branch.add_child(child=child, dist=1)
			self.tree.remove_child(child)

	def run(self):
		while len(self.tree.children) > 2:
			self.step()
		return self.tree
		# self.tree.write() is throwing an error. why?!?!?!
		# print(self.tree.write())


if __name__ == '__main__':
	g = Generator(TimeTree(), 10)
	end = g.run()
	print(end)


