import random
BREAK_STRING = "---------------------------------------------------------------------------------------------------------"

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
        return f"{self.name} of {self.suit}"

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

class DeckWaste():

    def __init__(self, cards):
        self.cards = cards
        self.waste = []

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
            return
        return getattr(self, f"stack_{attrNum}")

    def moveInTableMore(self, stackNumberFrom, stackNumberTo, topCard):
        stackFrom = self.stackAttr(stackNumberFrom)
        stackTo = self.stackAttr(stackNumberTo)
        cnt = None
        if stackFrom:
            for i in range(0,len(stackFrom)):
                if stackFrom[i].name.lower() == topCard:
                    cnt = i
                    break
            if cnt is None:
                print(f"No {topCard} is in the stack")
                return
            print(cnt)
            if stackTo:
                if stackTo[-1].isDiffSuit(stackFrom[cnt]) and stackTo[-1].isGreater(stackFrom[cnt]):
                    stackTo.extend(stackFrom[cnt:])
                else:
                    print("Card is invalid to move")
                    return
            elif stackTo is not None:
                stackTo.extend(stackFrom[cnt:])
                return
            else:
                print("No stack was created")
                return
            del stackFrom[cnt:]
        else:
            print("Stack is empty")

    def maxLength(self):
        return max(len(self.stack_1), len(self.stack_2), len(self.stack_3), len(self.stack_4))

    def getElement(self, stackNum, elementNum):
        stack = getattr(self, f"stack_{stackNum}")
        if len(stack) > elementNum:
            return stack[elementNum]
        else:
            return "         "

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

    def moveInTable(self, stackNumberFrom, stackNumberTo):
        stackFrom = self.stackAttr(stackNumberFrom)
        stackTo = self.stackAttr(stackNumberTo)
        if stackFrom:
            if stackTo:
                if stackFrom[-1].isBelow(stackTo[-1]) and stackFrom[-1].isDiffSuit(stackTo[-1]):
                    stackTo.append(stackFrom.pop())
                else:
                    print("Card is invalid to move")
            else:
                stackTo.append(stackFrom.pop())
        else:
            print(f"No card in stack_{stackNumberFrom}")
        


class Foundation():

    def __init__(self):
        self.foundation_tok = []
        self.foundation_sziv = []
        self.foundation_zold = []
        self.foundation_makk = []

    def foundationAttr(self, attrKind):
        if attrKind == "tok" or attrKind == "sziv" or attrKind == "zold" or attrKind == "makk":
            return  getattr(self, f"foundation_{attrKind}")
        print("**FOUNDATION CAN BE ONLY A,F,K,ZS**")
    
    def isWon(self):
        if len(self.foundation_tok) > 0 and len(self.foundation_sziv) > 0 and len(self.foundation_zold) > 0 and len(self.foundation_makk) > 0:
            return self.foundation_tok[-1].value == 14 and self.foundation_sziv[-1].value == 14 and self.foundation_zold[-1].value == 14 and self.foundation_makk[-1].value == 14
        return False

    def getTopCard(self, suit):
        foundationGet = self.foundationAttr(suit)
        if len(foundationGet) == 0:
            return suit[0].upper()
        else:
            return foundationGet[-1]

    def addFromWaste(self, w):
        if len(w.waste) > 0: 
            cardToAdd = w.waste[-1]
            foundationToAdd = self.foundationAttr(cardToAdd.suit)
            if len(foundationToAdd) == 0 and cardToAdd.value == 7:
                foundationToAdd.append(w.waste.pop())
            elif len(foundationToAdd) > 0:
                if cardToAdd.isGreater(foundationToAdd[-1]):
                    foundationToAdd.append(w.waste.pop())
                else:
                    print("Invalid card to add to the foundation")
            else:
                print("Foundation can only start with 7")
        else:
            print("No card in waste")

    def addFromTableStack(self, stack):
        if len(stack) > 0:
            cardToAdd = stack[-1]
            foundationToAdd = self.foundationAttr(cardToAdd.suit)
            if len(foundationToAdd) == 0 and cardToAdd.value == 7:
                foundationToAdd.append(stack.pop())
            elif len(foundationToAdd) > 0:
                if cardToAdd.isGreater(foundationToAdd[-1]):
                    foundationToAdd.append(stack.pop())
                else:
                    print("Invalid card to add to the foundation")
            else:
                print("Foundation can only start with 7")
        else:
            print("No card in stack")
    
def printCommands():
    print("Valid commands:")
    print("\tdw - move card from deck to waste")
    print("\twf - move card from waste to foundation")
    print("\twt #T- move card from waste to table")
    print("\ttf #T- move card from table to foundation")
    print("\ttt #T1 #T2 - move card between stacks")
    print("\ttm #T1 #T2 #CN - move carcs from one stock to an other")
    print("\tlw - move card from locked to waste")
    print("\th - help")
    print("\tq - quit")

def printTable(table, foundation, waste, locked):
    print(BREAK_STRING)
    print("Locked \t  Waste \t Deck \t\t\t Foundation")
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
        len(locked),
        waste.getWaste(),
        waste.getDeck(),
        foundation.getTopCard("tok"),
        foundation.getTopCard("sziv"),
        foundation.getTopCard("zold"),
        foundation.getTopCard("makk")
    ))
    print("\nTable\n\t1\t\t2\t\t3\t\t4")
    for x in range(0,table.maxLength()):
        print("\t{}\t{}\t{}\t{}".format(
            table.getElement(1,x),
            table.getElement(2,x),
            table.getElement(3,x),
            table.getElement(4,x)
        ))
    print("\n"+BREAK_STRING)


if __name__ == "__main__":
    d = Deck()
    f = Foundation()
    locked = d.deal(4)
    w = DeckWaste(d)
    t = Table()
    printCommands()
    #Fill the board
    for n in range(1,5):
        w.deal()
        t.addFromWaste(w.waste,n)
    printTable(t, f, w, locked)
    q = True
    while not f.isWon():
        command = input("Enter a command (type 'h' for help): ")
        command = command.lower().replace(" ", "")

        if command == "h":
            printCommands()
        elif command == "q":
            print("Game exited.")
            break
        elif command == "dw":
            w.deal()
            printTable(t, f, w, locked)
        elif command == "wf":
            f.addFromWaste(w)
            printTable(t, f, w, locked)
        elif "wt" in command and len(command) == 3:
            t.addFromWaste(w.waste,command[-1])
            printTable(t, f, w, locked)
        elif "tf" in command and len(command) == 3:
            f.addFromTableStack(t.stackAttr(command[-1]))
            printTable(t, f, w, locked)
        elif "tt" in command and len(command) == 4:
            t.moveInTable(command[-2], command[-1])
            printTable(t, f, w, locked)
        elif "tm" in command and len(command) == 5:
            t.moveInTableMore(command[-3], command[-2], command[-1])
            printTable(t, f, w, locked)
        elif "tm" in command and len(command) == 6:
            t.moveInTableMore(command[-4], command[-3], command[-2] + command[-1])
            printTable(t, f, w, locked)
        elif command == "lw":
            if len(w.waste) == 0 and len(locked) > 0 and len(w.cards.deck) == 0:
                w.waste.append(locked.pop())
                printTable(t, f, w, locked)
            else:
                print("Waste is not empty or there is no more locked card")
        else:
            print("Command unknown")
    
    if f.isWon():
        print("Congratulations! You've won!")