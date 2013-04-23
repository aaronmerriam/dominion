import logging
import datetime
from collections import defaultdict
from pprint import pprint

from dominion.core import Game
from dominion.cards import *

from dominion.bots.logic import MoneyLogicBot, SmithyLogicBot, SmithyLabLogicBot, RandomLogicBot

COMPARE_CARDS = (
    Market, Village, Moat, Woodcutter, Workshop,
    Bureaucrat, Gardens, Smithy, Festival, Laboratory,
)

def get_logger(name='dominion', filename=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(filename or datetime.datetime.now().strftime('logs/%Y-%m-%d-%f.log'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    #logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(level)
    return logger

if __name__ == '__main__':
    best = 0
    signature = None
    while True:
        wins = defaultdict(int)
        game = Game((RandomLogicBot, SmithyLabLogicBot, MoneyLogicBot, SmithyLogicBot), action_cards=COMPARE_CARDS)
        game.initialize_game()
        for i in xrange(1000):
            game.process_game()
            wins[type(game.winner).__name__] += 1
            game.reset_game()
        #print '############# test completed ###############'
        #for k, v in wins.iteritems():
        #    print "{0} - {1}".format(k, v)
        #print '############# test completed ###############'
        if max(wins, key=wins.get) == RandomLogicBot.__name__ and wins['RandomLogicBot'] > best:
            best = wins['RandomLogicBot']
            signature = game.players[0].signature
            print '############# test completed ###############'
            for k, v in wins.iteritems():
                print "{0} - {1}".format(k, v)
            print '############# test completed ###############'
            print '############### WIN ###############'
            pprint(game.players[0].signature)
            print '############### WIN ###############'
