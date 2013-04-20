from dominion.core import Game

from dominion.bots import SimpleBuyStrategy, RandomActionStrategy

#game = Game((SimpleBuyStrategy, RandomActionStrategy))
game = Game((RandomActionStrategy, RandomActionStrategy))

if __name__ == '__main__':
    game.initialize_game()
    game.process_game()
