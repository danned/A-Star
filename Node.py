class Node(object):
    #predecessor = 0
    #x = 0
    #y = 0
    #f = 0
    #g = 0
    map = 0

    def __init__(self, pre, earning, stack,endNode, action, predictedAction, invested):
        global endPoint
        self.predecessor = pre
        #print type(pre)
        self.action = action
        self.stack = stack
        self.invested = invested
        self.endNode = endNode
        self.predictedAction = predictedAction
        if type(pre) is Node:
            #print "setting g"
            #print "addding :", Node.map[y,x], " to g"
            self.g = pre.g+earning
        else:
            self.g = 0

        self.f = self.g - self.heuristic( )

    def __eq__(self, other):
        #print "Node() __eq__ called"
        return self.f == other.f and type(other.predecessor) == type(self.predecessor) #False#self.x == other.x and self.y == other.y # same position means same node

    def __cmp__(self,other):
        return other.f - self.f

    def __str__(self):
        return " f: " + str(self.f)

    def getStack(self):
        return self.stack

    def getF(self):
        return self.f

    def getG(self):
        return self.g
    def isEndNode(self):
        return self.endNode

    def getAction(self):
        return self.action

    def getPre(self):
        return self.predecessor

    def getInvested(self):
        return self.invested

    def heuristic(self):
        return self.invested/200 # normalised with max stack
