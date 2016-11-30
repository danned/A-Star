
class Node(object):


    def __init__(self,action,parent):
        self.successors = None
        self.parent = parent
        self.action = action

    def setSuccessors(self,Successors):
        self.successors = Successors

    def setParent(self,Parent):
        self.parent = Parent

    def getAction(self):
        return self.action

    def getParent(self):
        return self.parent

    def getSuccessors(self):
        return self.successors
