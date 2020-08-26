import ipywidgets


class CardGrouper(object):
	def __init__(self, card_tree):
		self.tree = card_tree
		self.states = dict()

	def __create_tree(self):
		for 