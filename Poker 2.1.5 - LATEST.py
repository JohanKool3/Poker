## Poker l v2.1.5 - NOTE: this is in early version and there are still bugs in the latest additions
## Naming Convention: Major version.Minor version.Patch Number
## Author: Johan Kool

import csv,random,math ; from random import shuffle


class Card(object):## Card Object Classification

    """ A Simple Card Object """

    def __init__(self,colour,value,suit,points,faceup,shorthand):

        self.__colour = str(colour)## All class based variables are now private to prevent tampering during runtime (to stop people from cheating!!!!!!)
        self.__value = str(value)
        self.__suit = str(suit)
        self.__faceup = bool(faceup)
        self.__points = int(points)
        self.__shorthand = str(shorthand)
        self.__fullName = "The " + str(value) + " Of " + str(suit)

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
        self.__validationAI = []
        self.__rank = None
        self.__handType = None
        self.__newCard = None
        self.__bet = 0
        self.__balance = 1000 ## £10 starting Balance
        self.__highestCard = None
        self.__deck = deck

        for card in deck.getDeckBackup()[1:13]:
            self.__validation.append((0,card.getValue()))

        for i in range(5):
            self.playerDraw(deck)

        self.__validationAI = self.__validation
    ## End of __init__

    def __str__(self):
        
        output = "Player: "+str(self.__name)+"'s Hand"
        return output

    def getName(self):
        return self.__name

    def getBetAmount(self):
        return self.__bet
    
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

            try:
                if self.__balance == 0 or currentBet > self.__balance:
                    quit("Player:",self.__name,"Has run out of balance")
                else:        
                    while 1:
                        amount = int(input("Please Enter The Amount You Are Going To Bet (in pence), You Currently Have: "+ str(self.__balance)))
                        try:
                            if amount == 0 or amount < int(currentBet) or amount > self.__balance:
                                print("Please enter a valid amount (greater than the current highest bet yet available to your current balance)")
                                
                            else:                    
                                self.__bet = int(amount)
                                self.__balance -= int(amount)
                                return self.__bet
                                break                
                        except:
                            print("Invalid Input , Please try again")
            except:
                print("Invalid Input")

    def aiSetBet(self,inputAmount):        
        self.__bet = int(inputAmount)
        self.__balance -= int(inputAmount)

    def winBet(self,prize):
        self.__balance += prize + self.__bet
        print("New balance of:",self.__balance)
        return prize
        

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
            print("You Draw:",self.__newCard,"Replacing: ",axisCard.getFullname())
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

    def determineHighestCard(self):

            for card in self.__contents:
                returnCard = card

            self.__highestCard = returnCard


    def determineRank(self):
        self.sortHand()

        def getCardQuantities():

            for cardC in self.__contents:
            
                for index,cardV in enumerate(self.__validation):

                    if cardC.getValue() == cardV[1]:
                        localValue = cardV[0]
                        self.__validation.remove(cardV)
                        self.__validation.insert(index,(localValue + 1,cardV[1]))

        
                
        getCardQuantities()## Gets a list of quantities
        rank = None
        self.determineHighestCard()## Finds highest card for the rule "Highest Card"

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


    def aiPlay(self,scoreToBeat,opponent):

        def playByProbability():
            
            def createGhostDeck():## Instatiates a blank deck replica which doesn't contain cards that are in play

                ghostDeck = self.__deck.getDeckBackup()            
                inPlayCards = self.getContentsFull() + opponent.getContentsFull()

                for card in ghostDeck:
                    for item in inPlayCards:
                        if card == item:
                            ghostDeck.remove(item)
                            
                return ghostDeck

            def nextMove(inputList):

                def countSuits(inputList):
                    hearts = []
                    diamonds = []
                    spades = []
                    clubs = []
                    for card in inputList:
                        if card.getSuit() == "Hearts":
                            hearts.append(card)
                        if card.getSuit() == "Diamonds":
                            diamonds.append(card)
                        if card.getSuit() == "Spades":
                            spades.append(card)
                        else:
                            clubs.append(card)

                    return [hearts,diamonds,spades,clubs]

                def countValues(inputList):

                    for suit in inputList:
                        
                        for cardC in suit:
            
                            for index,cardV in enumerate(self.__validationAI):

                                if cardC.getValue() == cardV[1]:
                                    localValue = cardV[0]
                                    self.__validationAI.remove(cardV)
                                    self.__validationAI.insert(index,(localValue + 1,cardV[1]))
                                
                countedSuits = [("Hearts",countedSuits(inputList)[0]),("Diamonds",countedSuits(inputList)[1]),("Spades",countedSuits(inputList)[2]),("Clubs",countedSuits(inputList)[3])]                                           
                countValues(countSuits(inputList))


            ## Main Logic     LAST UPDATED 03/01/21                   
            print("Changes Need To Be Made")            
            possibleCards = createGhostDeck()        
            nextMove(possibleCards)
            
        self.determineRank()## Sets the ai's rank, from which the next step can be determined

        if self.__rank < scoreToBeat:## If the ai has a better hand and will win by doing nothing
            print("No Changes Need To Be Made")

        elif self.__rank == 10 and scoreToBeat == 10:## If the ai needs a higher card

            if self.__highestCard.getPoints() <= opponent.getHighestCard().getPoints():                
                replacement = random.choice(self.getContentsFull()[:-1])
                self.replaceCard(replacement.getShorthand().lower(),self.__deck)

            if self.__highestCard.getPoints() > opponent.getHighestCard().getPoints():
                print("No changes Made")
                
            else:
                replacement = self.getContentsFull()[0]
                self.replaceCard(replacement.getShorthand().lower(),self.__deck)

        elif self.__rank == 1 and scoreToBeat == 1:
            print("No changes can be made")## No higher hand than the royal flush!
                                            
        else:
            playByProbability()
            
            
 

class Round(object):## This Is Where You Program The Game!

    def __init__(self,roundNo,fileDirectory):
        
        def initDeck(targetFile):

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
##        self.__playerList.append(PlayerHand("AI",self.__deck))## An AI opponent will be implemented at a later stage to replace this player
        
                                        
    def __str__(self):
        reply = "Round: "+str(self.__roundNo)
        return reply

    def getDeck(self):
        return self.__deck

    def playRound(self):

        def determineWinner():## Compares two players
            player1 = self.__playerList[0]
            player2 = self.__playerList[1]
            if self.__playerList[0].getRank() < self.__playerList[1].getRank():                
                print("Player", player1.getName(),"Wins - Higher Hand Value")
                print("Player",player1.getName(),"Wins: ",player1.winBet(player2.loseBet()),"p")
                

            elif self.__playerList[1].getRank() < self.__playerList[0].getRank():
                print("Player",player2.getName(),"Wins - Higher Hand Value")
                print("Player",player2.getName(),"Wins: ",player2.winBet(player1.loseBet()),"p")
                

            elif self.__playerList[0].getRank() != 10 and self.__playerList[1].getRank() != 10:
                print("Stalemate - Both hands yield the same value")
                for player in self.__playerList:
                    player.resetBet()

            else:
                
                if self.__playerList[0].getHighestCard().getPoints() > self.__playerList[1].getHighestCard().getPoints():
                    print("Player" ,player1.getName(),"Wins , Higher Highest Card"+" (" + str(self.__playerList[0].getHighestCard().getFullname())+")")
                    print("Player",player1.getName(),"Wins: ",player1.winBet(player2.loseBet()),"p")
                    

                elif self.__playerList[1].getHighestCard().getPoints() > self.__playerList[0].getHighestCard().getPoints():
                    print("Player",player2.getName(),"Wins , Higher Highest Card"+" (" + str(self.__playerList[1].getHighestCard().getFullname())+")")
                    print("Player",player2.getName(),"Wins: ",player2.winBet(player1.loseBet()),"p")
                    

                else:
                    print("Stalemate - Both Highest Cards Have The Same Value")
                    for player in self.__playerList:
                        player.resetBet()

        def outputs(player):
            
            print("Rank: ",player.getRank(), ",Derived From Hand Type: ", player.getHandType())
            print("\n")
            print("###### Next Player ######")
            print("\n")

        currentHighestBet = 0

        for index,player in enumerate(self.__playerList):            
            print("Player:",player.getName())
            
            if player.getName() != "AI":
                currentHighestBet == player.placeBet(currentHighestBet)
                player.displayContents()
                
                
                while 1:
                    
                    userRes = input("Would You Like To Replace A Card?")

                    if userRes.lower() == "yes":                    
                        userRes2 = input("Which Card?"+ str(self.__playerList[0].getContentsShort())).lower()                     
                        self.__deck.replaceCard(self.__playerList[0].replaceCard(userRes2,self.__deck))
                        self.__playerList[0].displayContents()                        
                        break
                    if userRes.lower() == "no":
                        break
                        
                player.determineRank()
                outputs(player)
                
            else:
                player.aiSetBet(self.__playerList[index-1].getBetAmount())
                player.displayContents()
                player.aiPlay(self.__playerList[index-1].getRank(),self.__playerList[index-1])
                outputs(player)

##        determineWinner() 

fileLocation = "Datasets/Poker_Ruleset"
round1 = Round(1,fileLocation)

round1.playRound()
