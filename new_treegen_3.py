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
		branch = self.tree.add_child(dist=1)
		for child in pair:
			new_dist = child.dist - 1 # TODO: What should 1 actually be? What if child.dist is too low?
			branch.add_child(child=child, dist=new_dist)
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


