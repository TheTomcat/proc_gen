# CustomQueue.py
from queue import PriorityQueue

class CustomQueue(PriorityQueue):
    def __init__(self, key):
        super().__init__()
        self.key = key
    def put(self, item):
        super().put((self.key(item), item))
    def get(self, *args, **kwargs):
        _,item = super().get(*args, **kwargs)
        return item
