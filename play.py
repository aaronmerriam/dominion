from dominion.core import Game

from dominion.bots.buy_money import SimpleBuyStrategy
from dominion.bots.random_bot import RandomActionStrategy
from dominion.bots.logic import MoneyLogicBot, SmithyLogicBot

#game = Game((SimpleBuyStrategy, RandomActionStrategy))
#game = Game((RandomActionStrategy, RandomActionStrategy))
game = Game((MoneyLogicBot, SmithyLogicBot))

if __name__ == '__main__':
    game.initialize_game()
    game.process_game()
