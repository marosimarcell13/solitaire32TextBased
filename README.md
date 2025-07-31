# Console Solitaire (Hungarian-style)

A text-based implementation of a simple Solitaire variant written in Python. This version uses Hungarian-style card suits and supports basic solitaire moves via command-line interaction.

## Game Overview

This solitaire game uses a custom deck where cards range from **7** to **ZS** (presumably Jack, Ace, Queen, King, Joker equivalents), and suits are:
- `tok`
- `makk`
- `sziv`
- `zold`

The game includes:
- A **Deck**
- A **Waste pile**
- A **Foundation** (for sorted final stacks by suit)
- A **Table** (4 tableau piles for working with cards)
- A **Locked pile** (reserve stack for later use)

You win by moving all cards into the foundation piles in ascending order per suit, starting from 7 and ending at ZS (14).

---

## How to Play

When you run the script, the game:
1. Shuffles and deals 4 cards to the **Locked pile**.
2. Initializes the **Deck** and **Waste** pile.
3. Deals one card to each of the 4 **Table** stacks from the **Waste** pile.

You then interact with the game using typed commands in the terminal.

---

## Commands

You can enter the following commands:

| Command | Description |
|--------|-------------|
| `dw` | Deal one card from the deck to the waste pile |
| `wf` | Move the top card from the waste pile to the foundation |
| `wt #` | Move the top card from the waste pile to table stack `#` (1–4) |
| `tf #` | Move the top card from table stack `#` to the foundation |
| `tt #1 #2` | Move the top card from table stack `#1` to table stack `#2` |
| `tm #1 #2 CN` | Move multiple cards starting from card name `CN` in table stack `#1` to `#2` |
| `lw` | Move a card from the locked pile to the waste (if waste and deck are empty) |
| `h` | Display help (list of commands) |
| `q` | Quit the game |

**Examples**:
- `wt 2`: Move from waste to table stack 2.
- `tm 3 4 A`: Move cards starting from "A" in stack 3 to stack 4.

---

## Winning the Game

You win when each foundation pile (one per suit) is filled from 7 to ZS (value 14). The game automatically checks and congratulates you when this condition is met.

---

## Technical Notes

- All cards are instances of the `Card` class, which includes logic for ordering and matching by suit.
- The `Deck` handles shuffling and dealing.
- `DeckWaste` manages the waste pile.
- `Table` has 4 stacks and handles all in-table and from-waste interactions.
- `Foundation` manages sorted piles by suit.
- The game loop continuously prompts the user until they win or quit.

---

## Requirements

- Python 3.x

No external libraries are required.

---

## To Run

```bash
python3 solitaire.py
