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

    def __iter__(self):
        return self