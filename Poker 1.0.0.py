## Poker v1.0.0
## Naming Convention: Major version.Minor version.Patch Number
## Author: Johan Kool  No. 16761

import csv,random ; from random import shuffle


class Card(object):## Card Object Classification

    """ A Simple Card Object """

    def __init__(self,colour,value,suit,points,faceup,shorthand):

        self.__colour = str(colour)## All class based variables are now private to prevent tampering during runtime (to stop people from cheating!!!!!!)
        self.__value = str(value)
        self.__suit = str(suit)
        self.__faceup = bool(faceup)
        self.__points = int(points)
        self.__shorthand = str(shorthand)
        self.__fullName = "The " + str(value) + " Of " + str(suit)## Not necessary but nice to have for debugging

    def __str__(self):
        
        if self.__faceup == False:
            return "This Card Is Face Down"
        else:
            return str(self.__value) + " Of " + str(self.__suit)

    def getColour(self):
        return self.__colour

    def getValue(self):
        return self.__value

    def getSuit(self):
        return self.__suit

    def isFaceup(self):
        self.__faceup = True

    def getShorthand(self):
        return self.__shorthand

    def getFullname(self):
        return self.__fullName

    def changeState(self,newState):        
        try:
            bool(newState)
            self.__faceup = newState
        except:
            print("No Valid Boolean Input Detected")

    def getPoints(self):
        return self.__points

## End Of Card Classification

class Deck(object):

    def __init__(self,contents):
        self.__contents = list(contents)
        self.__deckBackup = list(contents)## Created as a safe backup incase of emergency

    def shuffle(self):
        self.__contents = random.sample(self.__contents,len(self.__contents))

    def getDeckBackup(self):
        return self.__deckBackup
        
    def getContents(self):
        return self.__contents

    def displayCardNames(self):
        for card in self.__contents:
            print(card)

    def drawCard(self):
        newCard = self.__contents[0]
        self.__contents.remove(newCard)        
        return newCard

    def replaceCard(self,card):
        self.__contents.append(card)
    
    def resetPlay(self,players):        
        for player in players:
            player.resetContents()            
        self.__contents = self.__deckBackup
## End Of Deck Classification

class PlayerHand(object): ## Hand Object Classification

    def __init__(self,player,deck,contents=[]):

        self.__contents = list(contents)
        self.__name = str(player)
        self.__validation = []
        self.__rank = None
        self.__handType = None
        self.__newCard = None
        self.__bet = 0
        self.__balance = 1000 ## £10 starting Balance
        self.__highestCard = None

        for card in deck.getDeckBackup()[1:13]:
            self.__validation.append((0,card.getValue()))

        for i in range(5):
            self.playerDraw(deck)
    ## End of __init__

    def __str__(self):
        
        output = "Player: "+str(self.__name)+"'s Hand"
        return output
    
    def getLength(self):
        return len(self.__contents)
    def resetContents(self):
        self.__contents = []
        
    def getContentsShort(self):## Fetch card shorthands
        returnList = []
        for card in self.__contents:
            returnList.append(card.getShorthand())            
        return returnList

    def getContentsFull(self):
        returnList = []
        for card in self.__contents:
            returnList.append(card)            
        return returnList

    def playerDraw(self,deck):
        newCard = deck.drawCard()
        self.__contents.append(newCard)
        self.__newCard = newCard ## Updates the most recent card action

    def playCard(self,card):
        self.__contents.remove(card)
        return card

    def placeBet(self,currentBet):

        while 1:
            amount = input("Please Enter The Amount You Are Going To Bet (in pence), You Currently Have: "+ str(self.__balance))
            try:
                if amount == 0 or amount < int(currentBet):
                    print("Please enter a valid amount (greater than the current highest bet)")
                    
                else:                    
                    self.__bet = int(amount)
                    self.__balance -= int(amount)
                    break
            except:
                print("Invalid Input , Please try again")

    def winBet(self,prize):
        self.__balance += prize

    def getHandType(self):
        return self.__handType
        
    def loseBet(self):
        prize = self.__bet
        self.__bet = 0
        return prize

    def resetBet(self):
        self.__balance += self.__bet
        self.__bet = 0
            
    
    def replaceCard(self,userInput,deck):
        axisCard = None

        for card in self.__contents:
            
            if card.getShorthand().lower() == str(userInput):
                axisCard = card
                self.__contents.remove(card)

        if axisCard != None:## If the card has a definition
            self.playerDraw(deck)
            print("You Draw:",self.__newCard)
            print("\n")
            return axisCard
        else:
            print("Invalid Input")                                

    def sortHand(self):
        
        localContents = []
        returnList = []
        valueList = []
        
        for card in self.__contents:
            localContents.append((card.getPoints(),card))## Creates a tuple object (x,y) where x is the points and y is the card  object
            valueList.append(card.getPoints())
            
        valueList.sort()

        for value in valueList:
            for card in localContents:

                if value == card[0]:## x of the tuple value
                    localContents.remove(card)
                    returnList.append(card[1])
                    
        self.__contents = returnList

    def displayContents(self):
        
        def display(aList):## Simple Display Function

            for card in aList:
                print(card.getShorthand(),": ",card.getFullname())
                
        self.sortHand()
        display(self.__contents)

    def getRank(self):
        return self.__rank

    def getHighestCard(self):
        return self.__highestCard


    def determineRank(self):
        self.sortHand()

        def getCardQuantities():

            for cardC in self.__contents:
            
                for index,cardV in enumerate(self.__validation):

                    if cardC.getValue() == cardV[1]:
                        localValue = cardV[0]
                        self.__validation.remove(cardV)
                        self.__validation.insert(index,(localValue + 1,cardV[1]))

        def getHighestCard():

            for card in self.__contents:
                returnCard = card

            self.__highestCard = returnCard
                
        getCardQuantities()## Gets a list of quantities
        rank = None
        getHighestCard()## Finds highest card for the rule "Highest Card"

        ## For any rule that requires the same suit
        if self.__contents[0].getSuit() == self.__contents[1].getSuit() and self.__contents[0].getSuit() == self.__contents[2].getSuit() and self.__contents[0].getSuit() == self.__contents[3].getSuit() and self.__contents[0].getSuit() == self.__contents[4].getSuit():

            if self.__contents[0].getPoints() == 9 and self.__contents[1].getPoints() == 10 and self.__contents[2].getPoints() == 11 and self.__contents[3].getPoints() == 12 and self.__contents[4].getPoints() == 13:## Royal Flush
                rank = 1
                self.__handType = "Royal Flush"

            elif (self.__contents[0].getPoints()) + 1 == self.__contents[1].getPoints() and (self.__contents[0].getPoints()) + 2 == self.__contents[2].getPoints() and (self.__contents[0].getPoints()) + 3 == self.__contents[3].getPoints() and (self.__contents[0].getPoints() + 4) == self.__contents[4].getPoints():## Straight Flush
                rank = 2
                self.__handType = "Straight Flush"


            else:
                rank = 5
                self.__handType = "Flush"

        else:

            if (self.__contents[0].getPoints()) + 1 == self.__contents[1].getPoints() and (self.__contents[0].getPoints()) + 2 == self.__contents[2].getPoints() and (self.__contents[0].getPoints()) + 3 == self.__contents[3].getPoints() and (self.__contents[0].getPoints() + 4) == self.__contents[4].getPoints():## Straight 
                rank = 6
                self.__handType = "Straight"

            else:
                                                        
                for tValue in self.__validation:## For Grouping Rules

                    if tValue[0] == 4:## Four Of A Kind
                        rank = 3
                        self.__handType = "Four Of A Kind"

                    elif tValue[0] == 3:## Three Of A Kind
                        rank = 7
                        self.__handType = "Three Of A Kind"
                        
                    if tValue[0] == 2 and rank == None:## Two Of A Kind
                        rank = 9
                        self.__handType = "Two Of A Kind"

                    elif tValue[0] == 2 and rank != 7:## Double Two Of A Kind
                        rank = 8
                        self.__handType = "Double Two Of A Kind"

                    elif tValue[0] == 2 and rank == 7:
                        rank = 4
                        self.__handType = "Full House"

                if rank == None:
                    rank = 10
                    self.__handType = "Highest Card(" + self.__highestCard.getFullname()+ ")"            

        self.__rank = rank


class Round(object):## This Is Where You Program The Game!

    def __init__(self,roundNo,fileDirectory):## Sets Up The PlayerHands , Deck and GameRules
        
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
            for card in deckimport:
                objectDeck.append(Card(str(card[0]),str(card[1]),str(card[2]),int(card[3]),bool(card[4]),str(card[5])))                
            return objectDeck
        
        self.__roundNo = int(roundNo)        

        self.__deck = Deck(initDeck(fileDirectory))
        self.__deck.shuffle()
        self.__playerList = []
        self.__playerList.append(PlayerHand("1",self.__deck))
        self.__playerList.append(PlayerHand("AI",self.__deck))## An AI opponent will be implemented at a later stage to replace this player
        
                                        
    def __str__(self):
        reply = "Round: "+str(self.__roundNo)
        return reply

    def playRound(self):

        def determineWinner():
            player1 = self.__playerList[0]
            player2 = self.__playerList[1]
            if self.__playerList[0].getRank() < self.__playerList[1].getRank():                
                print("Player 1 Wins - Higher Hand Value")
                player1.winBet(player2.loseBet())
                

            elif self.__playerList[1].getRank() < self.__playerList[0].getRank():
                print("Player 2 Wins - Higher Hand Value")
                player2.winBet(player1.loseBet())
                

            elif self.__playerList[0].getRank() != 10 and self.__playerList[1].getRank() != 10:
                print("Stalemate - Both hands yield the same value")
                for player in self.__playerList:
                    player.resetBet()

            else:
                
                if self.__playerList[0].getHighestCard().getPoints() > self.__playerList[1].getHighestCard().getPoints():
                    print("Player 1 Wins , Higher Highest Card"+" (" + str(self.__playerList[0].getHighestCard().getFullname())+")")
                    player1.winBet(player2.loseBet())
                    

                elif self.__playerList[1].getHighestCard().getPoints() > self.__playerList[0].getHighestCard().getPoints():
                    print("Player 2 Wins , Higher Highest Card"+" (" + str(self.__playerList[1].getHighestCard().getFullname())+")")
                    player2.winBet(player1.loseBet())
                    

                else:
                    print("Stalemate - Both Highest Cards Have The Same Value")
                    for player in self.__playerList:
                        player.resetBet()
                
        for player in self.__playerList:

            player.displayContents()
            while 1:
                
                userRes = input("Would You Like To Replace A Card?")

                if userRes.lower() == "yes":                    
                    userRes2 = input("Which Card?"+ str(player.getContentsShort())).lower()                     
                    self.__deck.replaceCard(player.replaceCard(userRes2,self.__deck))
                    player.displayContents()                        
                    break
                if userRes.lower() == "no":
                    break
                    
            player.determineRank()
                    
            print("Rank: ",player.getRank(), ",Derived From Hand Type: ", player.getHandType())
            print("\n")
            print("###### Next Player ######")
            print("\n")

        determineWinner()

fileLocation = "Datasets/Poker_Ruleset"
round1 = Round(1,fileLocation)

round1.playRound()
