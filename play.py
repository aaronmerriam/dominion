from dominion.core import Game, get_logger

from dominion.bots.buy_money import SimpleBuyStrategy
from dominion.bots.random_bot import RandomActionStrategy
from dominion.bots.logic import MoneyLogicBot, SmithyLogicBot

#game = Game((SimpleBuyStrategy, RandomActionStrategy))
#game = Game((RandomActionStrategy, RandomActionStrategy))
#game = Game((SimpleBuyStrategy, RandomActionStrategy, MoneyLogicBot, SmithyLogicBot))
game = Game((MoneyLogicBot, SmithyLogicBot), get_logger())

if __name__ == '__main__':
    game.initialize_game()
    game.process_game()
