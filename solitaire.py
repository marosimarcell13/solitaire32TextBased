import random
BREAK_STRING = "----------------------------------------------------------------------"

class Card():
    card_to_name = {7:"7", 8:"8", 9:"9", 10:"10", 11:"A", 12:"F", 13:"K", 14:"ZS"}

    def __init__(self, value, suit):
        self.name = self.card_to_name[value]
        self.suit = suit
        self.value = value
    
    def isBelow(self, card):
        return self.value == (card.value - 1)

    def isGreater(self, card):
        return self.value == (card.value + 1)

    def isDiffSuit(self, card):
        return self.suit != card.suit

    def isSameSuit(self, card):
        return self.suit == card.suit

    def canAttach(self,card):
        if card.isBelow(self) and card.isDiffSuit:
            return True
        else:
            return False
    
    def __str__(self):
        return f"{self.name} {self.suit}"

    def __repr__(self):
        return self.__str__()

class Deck():
    unshuffled_deck = [Card(value, suit) for value in range(7,15) for suit in ["tok", "makk", "sziv", "zold"]]

    def __init__(self):
        self.deck = self.unshuffled_deck
        random.shuffle(self.deck)

    def deal(self, cardNums):
        return [self.deck.pop() for x in range(0, cardNums)]

    def dealOne(self):
        return self.deck.pop()

    def __str__(self):
        return str(self.deck)

    def __repr__(self):
        return self.__str__()

class DeckWasteLock():

    def __init__(self, cards):
        self.cards = cards
        self.waste = []
        self.locked = self.cards.deal(4)

    def deal(self):
        if len(self.cards.deck) > 0:
            self.waste.append(self.cards.dealOne())
        else:
            print("No more cards to deal from deck")

    def getWaste(self):
        if len(self.waste) > 0:
            return self.waste[-1]
        else:
            return "empty    "
    
    def getDeck(self):
        if len(self.cards.deck) > 0:
            return str(len(self.cards.deck)) + " card(s)"
        else:
            return "empty    "

    def autoDraw(self):
        if len(self.waste) == 0:
            self.deal()

    def moveLockedToWaste(self):
        """Move one locked card to waste if conditions match."""
        if not self.waste and self.locked and not self.cards.deck:
            self.waste.append(self.locked.pop())
        else:
            print("Waste is not empty or there is no more locked card")
            
    def __str__(self):
        return str(self.waste)

    def __repr__(self):
        return self.__str__()

class Table():
    
    def __init__(self):
        self.stack_1 = [] 
        self.stack_2 = [] 
        self.stack_3 = [] 
        self.stack_4 = []
    
    def stackAttr(self, attrNum):
        if int(attrNum) > 4 or int(attrNum) < 1:
            print("**THERE IS ONLY 4 STACKS IN THE TABLE**")
            return False
        return getattr(self, f"stack_{attrNum}")

    def moveInTableUniversal(self, stackNumberFrom, stackNumberTo, topCard=None):
        stackFrom = self.stackAttr(stackNumberFrom)
        stackTo = self.stackAttr(stackNumberTo)
    
        if not stackFrom:
            print(f"No card in stack_{stackNumberFrom}")
            return
    
        # Determine the starting index of cards to move
        if topCard is None:
            # Move only the last card
            start_index = len(stackFrom) - 1
        else:
            # Find the card in the stack
            start_index = None
            for i, card in enumerate(stackFrom):
                if card.name.lower() == topCard.lower():
                    start_index = i
                    break
            if start_index is None:
                print(f"No {topCard} in stack_{stackNumberFrom}")
                return
    
        # Cards to move
        moving_cards = stackFrom[start_index:]
    
        # Moving logic
        if stackTo:
            if stackTo[-1].isDiffSuit(moving_cards[0]) and stackTo[-1].isGreater(moving_cards[0]):
                stackTo.extend(moving_cards)
            else:
                print("Card is invalid to move")
                return
        else:
            stackTo.extend(moving_cards)
    
        # Remove moved cards from source
        del stackFrom[start_index:]

    def maxLength(self):
        return max(len(self.stack_1), len(self.stack_2), len(self.stack_3), len(self.stack_4))

    def getElement(self, stackNum, elementNum):
        stack = getattr(self, f"stack_{stackNum}")
        if len(stack) > elementNum:
            return stack[elementNum]
        else:
            return "    "

    def addFromWaste(self, w, stackNumber):
        if int(stackNumber) < 1 or int(stackNumber) > 4:
            print("There is only 4 pile of cards in the table")
            return
        if len(w) > 0:
            cardToAdd = w[-1]
            stack = self.stackAttr(stackNumber)
            if len(stack) == 0:
                stack.append(w.pop())
            elif len(stack) > 0:
                if cardToAdd.isDiffSuit(stack[-1]) and cardToAdd.isBelow(stack[-1]):
                    stack.append(w.pop())
                else:
                    print("Card to add is invalid")
            else:
                print("Invalid stack")
        


class Foundation():

    def __init__(self):
        self.foundation_tok = []
        self.foundation_sziv = []
        self.foundation_zold = []
        self.foundation_makk = []

    def foundationAttr(self, attrKind):
        if attrKind == "tok" or attrKind == "sziv" or attrKind == "zold" or attrKind == "makk":
            return  getattr(self, f"foundation_{attrKind}")
        print("**FOUNDATION CAN BE ONLY T,SZ,Z,M**")
    
    def isWon(self):
        if len(self.foundation_tok) > 0 and len(self.foundation_sziv) > 0 and len(self.foundation_zold) > 0 and len(self.foundation_makk) > 0:
            return self.foundation_tok[-1].value == 14 and self.foundation_sziv[-1].value == 14 and self.foundation_zold[-1].value == 14 and self.foundation_makk[-1].value == 14
        return False

    def getTopCard(self, suit):
        foundationGet = self.foundationAttr(suit)
        if len(foundationGet) == 0:
            return f"{suit[0].upper()}    "
        else:
            return foundationGet[-1]

    def addFromWaste(self, w):
        self._addCardToFoundation(w.waste)

    def addFromTableStack(self, stack, stackNum):
        stackFrom = stack.stackAttr(stackNum)
        self._addCardToFoundation(stackFrom)

    def _addCardToFoundation(self, source_pile):
        """Internal reusable logic to move top card from source pile to foundation."""
        if len(source_pile) == 0:
            print("No card to move")
            return

        cardToAdd = source_pile[-1]
        foundationToAdd = self.foundationAttr(cardToAdd.suit)

        if len(foundationToAdd) == 0 and cardToAdd.value == 7:
            foundationToAdd.append(source_pile.pop())
        elif len(foundationToAdd) > 0:
            if cardToAdd.isGreater(foundationToAdd[-1]):
                foundationToAdd.append(source_pile.pop())
            else:
                print("Invalid card to add to the foundation")
        else:
            print("Foundation can only start with 7")
    
def printCommands():
    print("Valid commands:")
    print("\th              - help")
    print("\tq              - quit")
    print("\tpt             - prints the gaming area")
    print("\tta             - toggle auto draw (default: OFF)")
    print("\tdw             - move card from deck to waste")
    print("\twf             - move card from waste to foundation")
    print("\twt #T          - move card from waste to table")
    print("\ttf #T          - move card from table to foundation")
    print("\ttt #T1 #T2     - move cards between stacks")
    print("\ttt #T1 #T2 #CV - move cards between stacks (CV = Card Value)")
    print("\tlw             - move card from locked to waste")

def printTable(table, foundation, waste):
    print(BREAK_STRING)
    print("Lock    Waste      Deck                   Foundation")
    print(
        "{:<7} {:10} {:<9}    {:<8} {:<8} {:<8} {:<8}".format(
            len(waste.locked),
            str(waste.getWaste()),
            waste.getDeck(),
            str(foundation.getTopCard("tok")),
            str(foundation.getTopCard("sziv")),
            str(foundation.getTopCard("zold")),
            str(foundation.getTopCard("makk"))
        )
    )

    print("\nTable")
    print("        {:<10} {:<10} {:<10} {:<10}".format("1", "2", "3", "4"))
    for x in range(table.maxLength()):
        print(
            "      {:<10} {:<10} {:<10} {:<10}".format(
                str(table.getElement(1, x)),
                str(table.getElement(2, x)),
                str(table.getElement(3, x)),
                str(table.getElement(4, x))
            )
        )
    print("\n" + BREAK_STRING)


if __name__ == "__main__":
    d = Deck()
    f = Foundation()
    w = DeckWasteLock(d)
    t = Table()
    printCommands()
    autoDraw = False
    #Fill the board
    for n in range(1,5):
        w.deal()
        t.addFromWaste(w.waste,n)
    while not f.isWon():
        if autoDraw:
            w.autoDraw()
        printTable(t, f, w)

        command = input("Enter a command (type 'h' for help): ")
        command = command.lower().replace(" ", "")

        if command == "h":
            printCommands()
        elif command == "q":
            print("Game exited.")
            break
        elif command == "dw":
            w.deal()
        elif command == "pt":
            continue
        elif command == "ta":
            print("Auto draw toggeled")
            autoDraw = not autoDraw
        elif command == "wf":
            f.addFromWaste(w)
        elif command == "lw":
            w.moveLockedToWaste()
        elif command == "lp":
            print(w.locked)
        elif "wt" in command and len(command) == 3:
            t.addFromWaste(w.waste,command[-1])
        elif "tf" in command and len(command) == 3:
            f.addFromTableStack(t, command[-1])
        elif "tt" in command and len(command) == 4:
            t.moveInTableUniversal(command[-2], command[-1])
        elif "tt" in command and len(command) == 5:
            t.moveInTableUniversal(command[-3], command[-2], command[-1])
        elif "tt" in command and len(command) == 6:
            t.moveInTableUniversal(command[-4], command[-3], command[-2] + command[-1])
        else:
            print("Command unknown")
    
    if f.isWon():
        print("****************************************************")
        print("************Congratulations! You've won!************")
        print("****************************************************")
