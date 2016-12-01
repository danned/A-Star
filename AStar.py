from Node import Node
from Agent import pokerStrategyExampleAggro
from Agent import pokerStrategyExample
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
        self.openList.insert(0,Node(0,0,playerStack, False, None, None,0))
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
        invested = node.getInvested()
        possibleEarnings = node.getG()
        print "invested money: ", invested, "closed list length: ", len(self.closedList)
        if node.getStack() >  1:
            earning = self.getEarnings(1, node.getStack(), self.agentStack-node.getG())
            if earning[0] == "Call" and not self.willWin:
                #node.setEndNode = True
                x = 0
                #sucessors.append(Node(node, -node.getG() - (self.playerStack-node.getStack()) -1, node.getStack() - 1, earning[0] != "Bet", ["Bet", 1], earning))
            else:
                sucessors.append(Node(node,earning[1],node.getStack()-1,earning[0] != "Bet", ["Bet",1],earning, invested +1))
        if node.getStack() > 5:
            earning = self.getEarnings(5, node.getStack(), self.agentStack-node.getG())
            if earning[0] == "Call" and not self.willWin:
                x = 0
                #sucessors.append(Node(node, -node.getG()- (self.playerStack-node.getStack())-5, node.getStack() - 5, earning[0] != "Bet", ["Bet", 5],earning))
            else:
                sucessors.append(Node(node,earning[1],node.getStack()-5,earning[0] != "Bet",["Bet",5],earning, invested +5))

        if node.getStack() > 10:
            earning = self.getEarnings(10, node.getStack(), self.agentStack-node.getG())
            if earning[0] == "Call" and not self.willWin:
                #sucessors.append(Node(node, -node.getG()- (self.playerStack-node.getStack())-10, node.getStack() - 10, earning[0] != "Bet", ["Bet", 10],earning))
                x = 0
            else:
                sucessors.append(Node(node,earning[1],node.getStack()-10,earning[0] != "Bet",["Bet",10],earning, invested +10))

        # call
        if self.willWin:
            sucessors.append(Node(node, 0, node.getStack(),True,["Call",0],None, invested))
        else:
            # fold
            sucessors.append(Node(node, -node.getG() - (invested), node.getStack(),True,["Fold",0],None, invested))

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

    def getEarnings(self, playerActionValue, playerStack, agentStack):
        return self.getAction(None, playerActionValue, playerStack, self.agentHand, self.agentHandRank, agentStack)

    def gOpenList(self,node):
        i = self.openList.index(node)
        return self.openList[i].getG()

    def getAction(self, playerAction, playerActionValue, playerStack, agentHand, agentHandRank, agentStack):  #
        #pokerStrategyExample()
        action = pokerStrategyExampleAggro(playerAction, playerActionValue, playerStack, agentHand, agentHandRank, agentStack)

        # You can extend this strategy as much as you want as long as you keep it fully deterministic (no random)
        return action

