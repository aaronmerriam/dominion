from collections import defaultdict

from dominion.core import Game

from dominion.bots.buy_money import SimpleBuyStrategy
from dominion.bots.random_bot import RandomActionStrategy
from dominion.bots.logic import MoneyLogicBot, SmithyLogicBot, SmithyLabLogicBot


#game = Game((SimpleBuyStrategy, RandomActionStrategy))
#game = Game((RandomActionStrategy, RandomActionStrategy))
#game = Game((SimpleBuyStrategy, RandomActionStrategy, MoneyLogicBot, SmithyLogicBot))

if __name__ == '__main__':
    wins = defaultdict(int)
    for i in xrange(10000):
        #game = Game((MoneyLogicBot, SmithyLogicBot))
        game = Game((SimpleBuyStrategy, SmithyLabLogicBot, MoneyLogicBot, SmithyLogicBot))
        game.initialize_game()
        game.process_game()
        wins[type(game.winner)] += 1
    for k, v in wins.iteritems():
        print "{0} - {1}".format(k, v)
