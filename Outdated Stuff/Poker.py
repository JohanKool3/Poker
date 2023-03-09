## Poker   // Completed : 
import csv , random
from random import shuffle

class Card(object):## Card Object Classification

    """ A Simple Card Object """

    def __init__(self,colour,value,suit,points,faceup,shorthand,sortCode):

        self.colour = str(colour)
        self.value = str(value)
        self.suit = str(suit)
        self.faceup = bool(faceup)
        self.points = int(points)
        self.shorthand = str(shorthand)
        self.sortCode = int(sortCode)
        self.fullName = "The " + str(value) + " Of " + str(suit)

    def __str__(self):

        if self.faceup == False:
            return "This Card Is Face Down"

        else:
            return str(self.value) + " Of " + str(self.suit)

    def getColour(self):
        return self.colour

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def isFaceup(self):
        self.faceup = True

    def changeState(self,newState):
        
        try:
            bool(newState)
            self.faceup = newState

        except:
            print("No Valid Boolean Input Detected")

    def getPoints(self):
        return self.points ## End Of Card Classification

class PlayerHand(object): ## Hand Object Classification

    def __init__(self,player,visible,contents=[]):

        self.contents = list(contents)
        self.player = str(player)
        self.visible = bool(visible)
        self.ranking = None
        self.playedCards = []
        self.bust = False

    def __str__(self):
        
        if self.visible == True:
            output = "Player: "+ str(self.player) + ", Contains: "+ str(self.contents)

        else:
            output = "Player: "+ str(self.player)+ "'s Hand"

        return output
    
    def getLength(self):
        return len(self.contents)

    def getContents(self):
        return self.contents

    def drawCard(self,deck):
        newCard = deck.contents[0]
        self.contents.append(newCard)
        self.latestCard = newCard

    def playCard(self,card):
        self.playedCards.append(card)
        self.contents.remove(card)

    def getStartingHand(self,deck,startingHandAmount):
        outputList = []
        n = 0
        
        for i in range(0,startingHandAmount):
            newCard = deck.contents[n]
            outputList.append(newCard)
            n += 1
            
        self.contents = list(outputList)

    def setRanking(self,ranking):
        self.ranking = ranking

    def getPoints(self):
        return self.points

    def resetPoints(self):
        self.points = int(0)

    def setBust(self):
        self.bust = True

    def sortHand(self):

        localContents = self.contents
        tupleList = []

        for card in localContents:
            tupleList.append((card.sortCode,card))

        def sort(aList):
            
            listLength = len(aList)

            for index in range(listLength):

                currentvalue = aList[index]
                position = index

                while position > 0 and aList[position -1] > currentvalue:
                    firstNumber = aList[position]
                    secondNumber = aList[position -1]

                    aList[position] = secondNumber
                    aList[position -1] = firstNumber

            return aList

        tupleList = sort(tupleList)
        returnList = []

        for item in tupleList:
            returnList.append(item[1])

        self.contents = returnList

    ## End Of Hand Classification
    

class Deck(object):

    def __init__(self,contents,dev):

        self.contents = list(contents)
        self.dev = True
        self.deckBackup = list(contents)

##        if dev == True:  //For Debugging Only! (It is rather annoying to see "Deck Ready" for each round instantiated!)
##            print("Deck Ready")
##            print("\n")

    def shuffle(self):
        self.contents = random.sample(self.contents,len(self.contents))
    def getContents(self):
        return self.contents

    def displayCardNames(self):

        for card in self.contents:

            print(card)

    def checkDoubles(self,hand):

        for cardH in hand.contents:
            for cardD in self.contents:
                if cardH == cardD:
                    self.contents.remove(cardD)
    ## End Of Deck Classification

    def resetPlay(self,players):

        for player in players:
            player.contents = []

        self.contents = self.deckBackup

    def createValidationDeck(self):## Also Functions As A Reset

        returnList = []

        for card in self.deckBackup[1:13]:

            returnList.append((0,card))

        returnList.insert(len(returnList),(0,self.deckBackup[0]))

        self.validDeck = returnList

    def displayValidationDeck(self):

        for card in self.validDeck:

            print(card[0],card[1].value+"s")

    def scoring(self,player):

        for card in player.contents:
            
            for index,item in enumerate(self.validDeck):

                if item[1].points == card.points:
                    newItem = (item[0] + 1,item[1])

                    self.validDeck.remove(item)
                    self.validDeck.insert(index,newItem)
                    

class Round(object):## This Is Where You Program The Game!

    def __init__(self,roundNo,fileDirectory,maxStartingHand,players):## Sets Up The PlayerHands , Deck and GameRules

        ## Basic Rules
        maxPlayers = 12


        def initDeck(targetFile):## Instantiates The Deck Of Cards // Takes File Directory In Form (A/B.FileExtension)

            def displayCards(tList):

                for item in tList:
                    print(item)
            
            def openFile(target):

                with open(target + ".csv","rt") as text_file:
                           step1 = csv.reader(text_file)
                           vlist = list(step1)
                           return vlist
                
            ## Imports The Data From target.csv
            deckimport = openFile(targetFile)
            del deckimport[0]## Removes Topper text E.g. Price or Name

            objectDeck = []

            for card in deckimport:
                objectDeck.append(Card(str(card[0]),str(card[1]),str(card[2]),int(card[3]),bool(card[4]),str(card[5]),int(card[6])))
##            displayCards(objectDeck) ## Not Necessary, but good for debugging
                
            return objectDeck## End of Function

        
        self.roundNo = int(roundNo)
        self.playerList = []
        self.startingHand = int(maxStartingHand)

        self.deck = Deck(initDeck(fileDirectory),True)
        self.deck.shuffle()## Because Having A Sorted Deck Is No Fun!

        self.deck.createValidationDeck()
        playerAmount = players

        try:
            if int(playerAmount) > maxPlayers:## Max Players Can Be Changed
                print("Too Many Players!, There Aren't Enough Cards To Go Around!")
                    
            else:

                for i in range(int(playerAmount)):

                    self.playerList.append(PlayerHand(str(int(i + 1)),True))

        except:
            print("Invalid Player Amount Input!")
                                
    def __str__(self):
        reply = "Round: "+str(self.roundNo)
        return reply

    def playRound(self):## Program Poker Here!

        self.ranking = 0

        def createPlayerHands():
            for player in self.playerList:
                player.getStartingHand(self.deck,self.startingHand)

            return self.playerList

        def displayPlayerHand(player):

            for card in player.contents:
                print(card.shorthand,":" , card)

        def getHandValue(deck):

            def determineStrength(deck):
                ranking = 0
                setStrength = False

                for card_1 in deck.validDeck:
                                    
                    if card_1[0] == 4:
                        ranking = 2
                        setStrength = True
                                            
                    elif card_1[0] == 2:
                        ranking = 9

                        if setStrength == True:## For Two Pairs
                            ranking = 8
                        setStrength = True

                if setStrength != True:
                    highestCard = None

                    for card in deck.validDeck:
                        
                        if card[0] > 0:
                            highestCard = card[1]

                    ranking = 10

                return ranking

            ranking = determineStrength(self.deck)

            return ranking

        self.playerList = createPlayerHands()## Instatiates The Player's Hands

        for player in self.playerList:
            
            displayPlayerHand(player)## Shows Cards [Shorthand] - Full Name
            
            self.deck.scoring(player)## Makes Tuple List Containing The Amount Of Each Value.
            self.deck.displayValidationDeck()## Shows This // For Debugging
            self.ranking = getHandValue(self.deck)
            
            self.deck.createValidationDeck()

            
            

        

        ## End Of Hand Setup
## End Of Round Classification
    
dataSetLocation = "Datasets/Poker_Ruleset"

round1 = Round(1,dataSetLocation,5,1)##1 Player For Debugging And Developing

round1.playRound()



            





        





    


    


        
