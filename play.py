from pprint import pprint
from collections import defaultdict

from dominion.core import Game, get_logger

from dominion.bots.buy_money import SimpleBuyStrategy
from dominion.bots.random_bot import RandomActionStrategy
from dominion.bots.logic import MoneyLogicBot, SmithyLogicBot, SmithyLabLogicBot, RandomLogicBot

from dominion.cards import (
    Market, Village, Moat, Woodcutter, Workshop,
    Bureaucrat, Gardens, Smithy, Festival, Laboratory,
)

COMPARE_CARDS = (
    Market, Village, Moat, Woodcutter, Workshop,
    Bureaucrat, Gardens, Smithy, Festival, Laboratory,
)

#game = Game((SimpleBuyStrategy, RandomActionStrategy))
#game = Game((RandomActionStrategy, RandomActionStrategy))
#game = Game((SimpleBuyStrategy, RandomActionStrategy, MoneyLogicBot, SmithyLogicBot))
game = Game((MoneyLogicBot, SmithyLogicBot, SmithyLabLogicBot), action_cards=COMPARE_CARDS)

if __name__ == '__main__':
    wins = defaultdict(int)
    game.initialize_game()
    assert Smithy in game.supply
    assert Laboratory in game.supply
    #game.process_game()
    for i in xrange(1000000):
        game.process_game()
        wins[type(game.winner).__name__] += 1
        game.reset_game()
        if not i % 10000:
            pprint(wins)
    pprint(wins)
