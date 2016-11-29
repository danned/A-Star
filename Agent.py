#import Judge.handRank as handRank
#import Judge.typeRank as typeRank
import Judge

handRank = Judge.handRank
typeRank = Judge.typeRank

#Judge.handRank
class Agent:
    def __init__(self,startingStack):
        self.hand = []
        self.stack = startingStack
        self.rankedHand = []

    def giveCard(self,c):
        self.hand.append(c)

    def getHand(self):
        return self.hand

    def setRankedHand(self, rc):
        self.rankedHand = rc

    def getRankedHand(self):
        return self.rankedHand

    def removeHand(self):
        self.hand = []
        self.rankedHand = []

    def getType(self):
        return self.rankedHand[0]

    def getRank(self):
        i = len(self.rankedHand[1])-1
        return self.rankedHand[1][i][0]

    def getStack(self):
        return self.stack

    def addWinnings(self,pot):
        self.stack += pot

    def isBroke(self):
        return self.stack <= 0

    def decreaseStack(self,value):
        self.stack -= value


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

