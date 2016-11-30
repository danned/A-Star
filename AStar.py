from Node import Node
from Judge import handRank
from Judge import typeRank

class aStar(object):
    #openList = []
    #closedList = []
    #map = []
    #solvedMap = np.zeros(shape=(60,60))
    def __init__( self, playerStack, agentHand, agentHandRank, agentStack, willWin,heuristic = None):
        self.openList = []
        self.closedList = []
        self.willWin = willWin
        self.openList.insert(0,Node(0,0,playerStack, False, None, None))
        self.heuristic = heuristic
        self.playerStack = playerStack
        self.agentHand = agentHand
        self.agentHandRank = agentHandRank
        self.agentStack = agentStack
        self.currentBest = None

    #iterates the map to find the endpoint
    def start(self):
        while len(self.openList) > 0:
            node = self.openList.pop(0)
            print "Looking at node: ", str(node)
            if self.agentStack - node.getF() <= 0:
                return node

            self.closedList.append(node)
            if not node.isEndNode():
                self.expandNode(node)
            else:
                if not type(self.currentBest) is Node:
                    self.currentBest = node
                elif self.currentBest > node:
                    self.currentBest = node



        return self.currentBest



    def expandNode(self, node):
        sucessors = []
        currentAgentStack = self.agentStack-node.getG()
        currentPlayerStack = node.getStack()
        invested = self.playerStack-node.getStack()
        possibleEarnings = node.getG()
        if node.getStack() >  1:
            earning = self.getEarnings(1, node.getStack(), self.agentStack-node.getG())
            if earning[0] == "Call" and not self.willWin:
                sucessors.append(Node(node, -node.getG() - (self.playerStack-node.getStack()) -1, node.getStack() - 1, earning[0] != "Bet", ["Bet", 1], earning))
            else:
                sucessors.append(Node(node,earning[1],node.getStack()-1,earning[0] != "Bet", ["Bet",1],earning))
        if node.getStack() > 5:
            earning = self.getEarnings(5, node.getStack(), self.agentStack-node.getG())
            if earning[0] == "Call" and not self.willWin:
                sucessors.append(Node(node, -node.getG()- (self.playerStack-node.getStack())-5, node.getStack() - 5, earning[0] != "Bet", ["Bet", 5],earning))
            else:
                sucessors.append(Node(node,earning[1],node.getStack()-5,earning[0] != "Bet",["Bet",5],earning))

        if node.getStack() > 10:
            earning = self.getEarnings(10, node.getStack(), self.agentStack-node.getG())
            if earning[0] == "Call" and not self.willWin:
                sucessors.append(Node(node, -node.getG()- (self.playerStack-node.getStack())-10, node.getStack() - 10, earning[0] != "Bet", ["Bet", 10],earning))
            else:
                sucessors.append(Node(node,earning[1],node.getStack()-10,earning[0] != "Bet",["Bet",10],earning))

        # call
        if self.willWin:
            sucessors.append(Node(node, 0, node.getStack(),True,["Call",0],None))
        else:
            # fold
            sucessors.append(Node(node, -node.getG() - (self.playerStack-node.getStack()), node.getStack(),True,["Fold",0],None))

        for s in sucessors:
            # this should never happen in poker tree
            if s in self.closedList:
                continue
            #newG = node.g + 1
            # This should never happen in poker tree
            if s in self.openList:
                continue
            #    if newG >= self.gOpenList(s):
            #        continue
                # found shorter path to node, replace
            #    i = self.openList.index(s)
            #    self.openList[i] = s
                # print self.openList, " now sorting \n"
            #    self.openList.sort()
                # print self.openList
            self.openList.append(s)
            # print self.openList., " now sorting \n"
            self.openList.sort()
            # s.predecessor = node

        #Maybe wrong
       # print self.map.shape[0]
        #print y
        #print x

        """
        if y+1 < self.map.shape[0]:
            if self.map[y + 1, x] != -1:
                sucessors.append(Node(node,y+1,x, self.heuristic))
            else:
                self.solvedMap[y + 1, x] = -1

        if y-1 >= 0:
            if self.map[y - 1, x] != -1:
                sucessors.append(Node(node,y-1,x, self.heuristic))
            else:
                self.solvedMap[y - 1, x] = -1


        if x+1  < self.map.shape[1]:
            if self.map[y, x + 1] != -1:
                sucessors.append(Node(node,y,x+1, self.heuristic))
            else:
                self.solvedMap[y, x + 1] = -1

        if x-1  >= 0:
            if self.map[y, x - 1] != -1:
                sucessors.append(Node(node,y,x-1, self.heuristic))
            else:
                self.solvedMap[y, x - 1] = -1

        for s in sucessors:
            if s in self.closedList:
                continue
            newG = node.g + 1
            if s in self.openList:
                if newG >= self.gOpenList(s):
                    continue
                # found shorter path to node, replace
                i = self.openList.index(s)
                self.openList[i] = s
                #print self.openList, " now sorting \n"
                self.openList.sort()
                #print self.openList
            self.openList.append(s)
            #print self.openList., " now sorting \n"
            self.openList.sort()
            #s.predecessor = node
            """

    def getEarnings(self, playerActionValue, playerStack, agentStack):
        return self.getAction(None, playerActionValue, playerStack, self.agentHand, self.agentHandRank, agentStack)

    def gOpenList(self,node):
        i = self.openList.index(node)
        return self.openList[i].getG()

    def getAction(self, playerAction, playerActionValue, playerStack, agentHand, agentHandRank, agentStack):  #

        agentAction = None
        agentValue = None

        if typeRank[agentHand] == 1 and handRank[agentHandRank] < handRank['Q']:  # Hand rank is lower than queen
            if playerActionValue < 0.02 * playerStack:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack
            else:
                if playerActionValue < 0.05 * agentStack:
                    if agentStack > playerStack:
                        if agentStack < playerActionValue:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Call'
                            agentValue = 5 if agentStack >= 5 else agentStack
                    else:
                        agentAction = 'Fold'
                        agentValue = 0
                else:
                    agentAction = 'Fold'
                    agentValue = 0


        if (typeRank[agentHand] == 1 and handRank[agentHandRank] >= handRank['Q']) \
                or (typeRank[agentHand] == 2 and handRank[agentHandRank] <= handRank['T']):
            # print(playerActionValue, type(agentStack))
            if playerActionValue < 0.02 * agentStack:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack
            else:
                if playerActionValue < 0.05 * agentStack:
                    if agentStack < 2 * playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = playerActionValue * 2
                else:
                    agentAction = 'Fold'
                    agentValue = 0

        if typeRank[agentHand] == 2 and handRank[agentHandRank] > handRank['T'] and handRank[agentHandRank] <= handRank['A']:
            if playerActionValue < 0.04 * playerStack:
                if agentStack < playerStack:
                    if playerActionValue < 0.06 * agentStack:
                        if agentStack < 2 * playerActionValue:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Bet'
                            agentAction = 'Fold'
                        agentValue = 0
                        agentValue = playerActionValue * 2
                else:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack
            if handRank[agentHandRank] == handRank['A']:
                if agentStack < 2 * playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Bet'
                    agentValue = playerActionValue * 2
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack

        if typeRank[agentHand] == typeRank['TwoPairs']:
            if playerActionValue < 0.05 * playerStack:
                if handRank[agentHandRank] > handRank['9']:
                    if agentStack < 2 * playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = playerActionValue * 2
                else:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
            else:
                if playerActionValue < 0.1 * agentStack:
                    if handRank[agentHandRank] > handRank['9'] and agentStack > playerStack:
                        if agentStack < 2 * playerActionValue:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Bet'
                            agentValue = playerActionValue * 2
                    else:
                        if agentStack < playerActionValue:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Call'
                            agentValue = 5 if agentStack >= 5 else agentStack
                    if handRank[agentHandRank] > handRank['J']:
                        if agentStack < playerActionValue:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Call'
                            agentValue = 5 if agentStack >= 5 else agentStack
                    else:
                        agentAction = 'Fold'
                        agentValue = 0

        if typeRank[agentHand] == typeRank['3ofakind']:
            if agentStack > 1.5 * playerStack:
                if playerActionValue < 0.05 * agentStack:
                    if playerActionValue > 0:
                        if agentStack < 2 * playerActionValue:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Bet'
                            agentValue = playerActionValue * 2
                    else:
                        if agentStack < 10:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Bet'
                            agentValue = 10
                else:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack

        # additional strategy added > than 3ofakind
        if typeRank[agentHand] > typeRank['3ofakind']:
            if agentStack > 1.5 * playerStack:
                if playerActionValue < 0.05 * agentStack:
                    if playerActionValue > 0:
                        if agentStack < 2 * playerActionValue:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Bet'
                            agentValue = playerActionValue * 2
                    else:
                        if agentStack < 10:
                            agentAction = 'Bet'
                            agentValue = agentStack
                        else:
                            agentAction = 'Bet'
                            agentValue = 15
                else:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack

        if agentAction is None or agentValue is None:
            agentAction = 'Fold'
            agentValue = 0

        # You can extend this strategy as much as you want as long as you keep it fully deterministic (no random)
        return agentAction, agentValue

