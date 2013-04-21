from dominion.core import Game

from dominion.bots.buy_money import SimpleBuyStrategy
from dominion.bots.random_bot import RandomActionStrategy

#game = Game((SimpleBuyStrategy, RandomActionStrategy))
game = Game((RandomActionStrategy, RandomActionStrategy))

if __name__ == '__main__':
    game.initialize_game()
    game.process_game()
