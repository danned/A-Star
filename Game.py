import random
#import Agent as Agent
from Agent import Agent
import Judge

class Deck:
    # strength of each type
    HAND_RANK = {'2': 1,
                '3': 2,
                '4': 3,
                '5': 4,
                '6': 5,
                '7': 6,
                '8': 7,
                '9': 8,
                'T': 9,
                'J': 10,
                'Q': 11,
                'K': 12,
                'A': 13}

    HAND_SUIT = {'s', 'h', 'd', 'c'}

    def __init__(self):
        self.deck = []
        self.poppedCards = []
        self.createDeck()
        self.shuffle()


    #creates a sorted deck
    def createDeck(self):
        self.deck = []
        self.poppedCards = []
        for e in self.HAND_RANK.keys():  # create deck
            for c in self.HAND_SUIT:
                self.deck.append(e + c)

    # shuffle
    def shuffle(self):
        random.shuffle(self.deck)

    #take and remove card from deck
    def pop(self):
        c = self.deck.pop()
        self.poppedCards.append(c)
        return c

    # maybe just use the cards of players hands as arguments and remove poppedCards array
    def returnCards(self):
        self.deck.extend(self.poppedCards)
        self.poppedCards = []

    def extend(self,list):
        self.deck.extend(list)






class Game:
    def __init__(self, maxRounds):
        self.agents = [Agent(100),Agent(100)]
        self.deck = Deck()
        self.roundNumber = 0
        self.maxRounds = maxRounds
        self.state = "deal"
        self.pot = 0
        self.folded = 0

    def deal(self):
        # pop 5 cards 2 times
        self.deck.extend( ['3h', 'Js', 'Qh', 'Kd', 'Ah','3s', '4d', 'Qd', 'Kc', 'Ad' ])
        for i in  range(2):
            for _ in range(5):
                self.agents[i].giveCard(self.deck.pop())

        self.defineHand()
        self.state = "bid"

    def bid(self):
        #both agents should bid in turn
        agent1Action = "none"
        agent1ActionValue = 0
        agent2Action = "none"
        agent2ActionValue = 0

        while True:#(playerAction, playerActionValue, playerStack, agentHand, agentHandRank, agentStack)
            # agentAction, agentValue
            #agent2ActionValue = 1
            agent1Response = self.agents[0].getAction(agent2Action, agent2ActionValue, self.agents[1].getStack(),\
                                                      self.agents[0].getType(), self.agents[0].getRank(), self.agents[0].getStack())
            agent1Action, agent1ActionValue = agent1Response
            self.agents[0].decreaseStack(agent1ActionValue)
            if agent1Action == 'Fold':
                print "Agent1 folding"
                self.folded = -1
                #self.state = "showdown"
                break
            if agent1Action == 'Call':
                print "Agent1 Calling"
                self.pot = self.pot + agent1ActionValue
                #self.state = "showdown"
                break

            agent2Response = self.agents[1].getAction(agent1Action, agent1ActionValue, self.agents[0].getStack(),\
                                                      self.agents[1].getType(), self.agents[1].getRank(), self.agents[1].getStack())
            agent2Action, agent2ActionValue = agent2Response
            self.agents[1].decreaseStack(agent2ActionValue)

            if agent2Action == 'Fold':
                print "Agent2 folding"
                self.folded = 1
                #self.state = "showdown"
                break
            if agent2Action == 'Call':
                print "Agent2 Calling"
                self.pot = self.pot + agent2ActionValue
                #self.state = "showdown"
                break

            self.pot = self.pot + agent1ActionValue + agent2ActionValue
            print "Both agents betting"

        self.state = "showdown"





    # let the judge define hand strenghts
    def defineHand(self):
        for i in range(2):
            sortedHand = Judge.groupHand(self.agents[i].getHand())
            self.agents[i].setRankedHand(Judge.identifyHand(sortedHand)) # returns [type,rank,theHand]

    def isFolded(self):
        return self.folded != 0

    def showdown(self):
        if self.isFolded():
            winner = self.folded
        else:
            # 1 if player 1 win, 0  draw, -1 if player 2.
            winner = Judge.judgeHands(self.agents[0].getRankedHand(),self.agents[1].getRankedHand())


        print "Agent1hand: ", self.agents[0].getRankedHand()
        print "Agent2hand: ", self.agents[1].getRankedHand()
        if winner == 1:
            print "Agent 1 wins ", self.pot, " $"
            self.agents[0].addWinnings(self.pot)
        elif winner == 0:
            print "Draw"
            self.agents[0].addWinnings(self.pot/2)
            self.agents[1].addWinnings(self.pot/2)
        elif winner == -1:
            print "Agent 2 wins ", self.pot, " $"
            self.agents[1].addWinnings(self.pot)

        self.pot = 0
        self.agents[0].removeHand()
        self.agents[1].removeHand()
        self.folded = 0
        self.roundNumber = self.roundNumber +1
        self.deck.returnCards()
        self.deck.shuffle()
        print "Current standings:\n Agent 1: ", self.agents[0].getStack(), " agent2: ", self.agents[1].getStack()
        if self.isContinue():
            self.state = "deal"
        else:
            self.state = "end"


    def isContinue(self):
        return  not (self.roundNumber >= self.maxRounds or self.agents[0].isBroke() or self.agents[1].isBroke())

    def mainFlow(self):
        while self.state != "end":

            if self.state == "deal":
                print "Dealing"
                self.deal()

            if self.state == "bid":
                print "biddingphase"
                self.bid()

            if self.state == "showdown":
                print "showdown"
                self.showdown()

game = Game(5000)
game.mainFlow()
