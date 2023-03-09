## Completed 28/11/2020 - Poker 0.0.1
import csv , random

from random import shuffle

class Card(object):## Card Object Classification

    """ A Simple Card Object """

    def __init__(self,colour,value,suit,points,faceup,shorthand):

        self.colour = str(colour)
        self.value = str(value)
        self.suit = str(suit)
        self.faceup = bool(faceup)
        self.points = int(points)
        self.shorthand = str(shorthand)
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

    def __init__(self,player,deck,contents=[]):

        self.contents = list(contents)
        self.name = str(player)
        self.validation = []
        self.rank = None
        self.handType = None
        self.newCard = None
        self.bet = 0
        self.balance = 1000 ## £10 starting Balance (In intiger form because floating point numbers scare me)

        for card in deck.deckBackup[1:13]:
            self.validation.append((0,card.value))
        self.validation.append((0,deck.deckBackup[0].value))
            

    def __str__(self):

        output = "Player: "+str(self.name)+"'s Hand"
        return output
    
    def getLength(self):
        return len(self.contents)

    def getContents(self):
        returnList = []
        for card in self.contents:
            returnList.append(card.shorthand)
            
        return returnList

    def drawCard(self,deck):
        newCard = deck.drawCard()
        self.contents.append(newCard)
        self.newCard = newCard

    def playCard(self,card):
        self.contents.remove(card)
        return card

    def placeBet(self):

        while 1:
            amount = input("Please Enter The Amount You Are Going To Bet (in pence), You Currently Have: "+ str(self.balance))

            try:

                if amount == 0:
                    print("Bruh")

                else:                    
                    self.bet = int(amount)
                    self.balance -= int(amount)
                break

            except:
                print("Invalid Input")

    def loseBet(self):
        prize = self.bet
        self.bet = 0
        return prize

    def resetbet(self):
        self.balance += self.bet
        self.bet = 0
            
    
    def replaceCard(self,userInput,deck):
        axisCard = None

        for card in self.contents:
            
            if card.shorthand.lower() == str(userInput):
                axisCard = card
                self.contents.remove(card)

        if axisCard != None:
            self.drawCard(deck)
            print("You Draw:",self.newCard)
            print("\n")
            return axisCard
        else:
            print("Invalid Input")                                

    def sortHand(self):
        
        localContents = []
        returnList = []
        valueList = []
        
        for card in self.contents:
            localContents.append((card.points,card))## 14;59 - Makes Local Contents equal A Tuple Value Where (x,y) x = value of card, y = The Card Object
            valueList.append(card.points)
            
        valueList.sort()

        for value in valueList:
            for card in localContents:

                if value == card[0]:
                    localContents.remove(card)
                    returnList.append(card[1])
                    
        self.contents = returnList

    def displayContents(self):
        
        def display(aList):## Simple Display Function

            for card in aList:
                print(card.shorthand,": ",card.fullName)
        self.sortHand()
        display(self.contents)


    def getRank(self):
        self.sortHand()
        ## Got To Get Card Amounts!!!!

        def getCardQuantities():

            for cardC in self.contents:
            
                for index,cardV in enumerate(self.validation):

                    if cardC.value == cardV[1]:
                        localValue = cardV[0]
                        self.validation.remove(cardV)
                        self.validation.insert(index,(localValue + 1,cardV[1]))

        def getHighestCard():

            for card in self.contents:
                returnCard = card

            self.highestCard = returnCard
                

        getCardQuantities()

        rank = None

        getHighestCard()

        if self.contents[0].suit == self.contents[1].suit and self.contents[0].suit == self.contents[2].suit and self.contents[0].suit == self.contents[3].suit and self.contents[0].suit == self.contents[4].suit:

            if self.contents[0].points == 9 and self.contents[1].points == 10 and self.contents[2].points == 11 and self.contents[3].points == 12 and self.contents[4].points == 13:## Royal Flush
                rank = 1
                self.handType = "Royal Flush"

            elif (self.contents[0].points) + 1 == self.contents[1].points and (self.contents[0].points) + 2 == self.contents[2].points and (self.contents[0].points) + 3 == self.contents[3].points and (self.contents[0].points + 4) == self.contents[4].points:## Straight Flush
                rank = 2
                self.handType = "Straight Flush"


            else:
                rank = 5
                self.handType = "Flush"

        else:

            if (self.contents[0].points) + 1 == self.contents[1].points and (self.contents[0].points) + 2 == self.contents[2].points and (self.contents[0].points) + 3 == self.contents[3].points and (self.contents[0].points + 4) == self.contents[4].points:## Straight 
                rank = 6
                self.handType = "Straight"
                
                        
            for tValue in self.validation:## For Grouping Rules

                if tValue[0] == 4:## Four Of A Kind
                    rank = 3
                    self.handType = "Four Of A Kind"

                elif tValue[0] == 3:## Three Of A Kind
                    rank = 7
                    self.handType = "Three Of A Kind"
                    
                if tValue[0] == 2 and rank == None:## Two Of A Kind
                    rank = 9
                    self.handType = "Two Of A Kind"

                elif tValue[0] == 2 and rank != 7:## Double Two Of A Kind
                    rank = 8
                    self.handType = "Double Two Of A Kind"

                elif tValue[0] == 2 and rank == 7:
                    rank = 4
                    self.handType = "Full House"

            if rank == None:
                rank = 10
                self.handType = "Highest Card(" + self.highestCard.fullName+ ")"
            

        self.rank = rank
          
                      
    ## End Of Hand Classification

class Deck(object):

    def __init__(self,contents):

        self.contents = list(contents)
        self.deckBackup = list(contents)

    def shuffle(self):
        self.contents = random.sample(self.contents,len(self.contents))
        
    def getContents(self):
        return self.contents

    def displayCardNames(self):

        for card in self.contents:
            print(card)

    def drawCard(self):

        newCard = self.contents[0]

        self.contents.remove(newCard)
        
        return newCard
    
    def resetPlay(self,players):
        
        for player in players:
            player.contents = []
            
        self.contents = self.deckBackup
    ## End Of Deck Classification


class Round(object):## This Is Where You Program The Game!

    def __init__(self,roundNo,fileDirectory,players):## Sets Up The PlayerHands , Deck and GameRules

        ## Basic Rules
        maxPlayers = 1
        startingHand = 5
        
        def initDeck(targetFile):## Instantiates The Deck Of Cards // Takes File Directory In Form (A/B.FileExtension)

            def displayCards(tList):
                for item in tList:
                    print(item)
            
            def openFile(target):
                with open(target + ".csv","rt") as text_file:
                           step1 = csv.reader(text_file)
                           vlist = list(step1)
                           return vlist
                
            deckimport = openFile(targetFile)
            del deckimport[0]

            objectDeck = []
            for card in deckimport:### Modified So Only One Suit Is Created
                objectDeck.append(Card(str(card[0]),str(card[1]),str(card[2]),int(card[3]),bool(card[4]),str(card[5])))
##            displayCards(objectDeck) ## Not Necessary, but good for debugging
                
            return objectDeck## End of Function

        
        self.roundNo = int(roundNo)        

        self.deck = Deck(initDeck(fileDirectory))
        self.deck.shuffle()## Because Having A Sorted Deck Is No Fun!

        self.playerList = []

        for i in range(players):
            self.playerList.append(PlayerHand(str(i),self.deck))

        for player in self.playerList:

            for i in range(startingHand):
                player.drawCard(self.deck)
        
## Setup Instance Rules
                                
    def __str__(self):
        reply = "Round: "+str(self.roundNo)
        return reply

    def playRound(self):

        def determineWinner():
            player1 = self.playerList[0]
            player2 = self.playerList[1]
            if self.playerList[0].rank < self.playerList[1].rank:                
                print("Player 1 Wins - Higher Hand Value")
                player1.balance += player2.loseBet()
                

            elif self.playerList[1].rank < self.playerList[0].rank:
                print("Player 2 Wins - Higher Hand Value")
                player2.balance += player1.loseBet()
                

            elif self.playerList[0].rank != 10 and self.playerList[1].rank != 10:
                print("Stalemate - Both hands yield the same value")
                for player in self.playerList:
                    player.resetBet()

            else:
                
                if self.playerList[0].highestCard.points > self.playerList[1].highestCard.points:
                    print("Player 1 Wins , Higher Highest Card"+" (" + str(self.playerList[0].highestCard.fullName)+")")
                    player1.balance += player2.loseBet()
                    

                elif self.playerList[1].highestCard.points > self.playerList[0].highestCard.points:
                    print("Player 2 Wins , Higher Highest Card"+" (" + str(self.playerList[1].highestCard.fullName)+")")
                    player2.balance += player1.loseBet()
                    

                else:
                    print("Stalemate - Both Highest Cards Have The Same Value")
                    for player in self.playerList:
                        player.resetBet()
                
        for player in self.playerList:
##            player.placeBet() Didn't get working in time :(
            player.displayContents()

            userRes = input("Would You Like To Replace A Card?")

            if userRes.lower() == "yes":
                userRes2 = input("Which Card?"+ str(player.getContents()))
                self.deck.contents.append(player.replaceCard(userRes2,self.deck))
                player.displayContents()
                
            player.getRank()
            print("Rank: ",player.rank, ",Derived From Hand Type: ", player.handType)
            print("\n")
            print("###### Next Player ######")
            print("\n")

        determineWinner()
                    
## __Main__
fileLocation = "Datasets/Poker_Ruleset"
round1 = Round(1,fileLocation,2)
round1.playRound()
