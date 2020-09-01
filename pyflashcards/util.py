import numpy as np

class bidirectional_iterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = -1

    def next(self):
        self.index += 1
        if self.index == (len(self.collection)):
            self.index = 0

        return self.collection[self.index]

    def prev(self):
        self.index -= 1
        if self.index < 0:
            self.index = (len(self.collection)-1)
        return self.collection[self.index]

    def shuffle(self):
        old_item = self.collection[self.index]
        collection = list(self.collection)
        np.random.shuffle(collection)
        self.index = collection.index(old_item)
        self.collection = collection

    def __iter__(self):
        return self