# Dominion Game Simulator

# Game Moderator

- Centralized logging

# Supply

- Manages the card supply.
- Knows when the game is over.

# Turns

- Keeps track of actions and cards.
- Processes card events


# Cards

Cards should be able to be accurately represented as a set of linear events,
some of which may require intervention by the bot.

## Automated Events
- extra action
- extra buy
- draw cards
- free buy

## Choice Based Events
- trash a card, pick new card
- use action multiple times
- select cards from own cards to discard
- select cards from others cards to discard
- select cards from others cards to steal
- discard, draw, and then repeat?


# Areas to improve

- Turn might should hold the `hand` of cards.
- `CardCollection` is hard to work with.
  - give me all the treasure/action cards
  - pop out all of the treasure/action cards
  - pop out the first X card.
  - 
