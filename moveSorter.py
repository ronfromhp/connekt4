import bisect 
from collections import namedtuple

Entry = namedtuple('Entry', 'move score')
class entries:
        def __init__(self, move=0, score=0) :
            self.move = move
            self.score = score
            
class MoveSorter:
    
    
    def __init__(self):
        self.entries = []
        
    def add(self, move, score ):
        entry = Entry(move, score)
        bisect.insort(self.entries, entry, key= lambda x : x.score)
        
    def getNext(self):
        if len(self.entries) ==0 :
            return 0
        return self.entries.pop().move
    
    def reset(self):
        self.entries =[]
        
