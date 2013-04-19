from .moderator import Game

from .bots import SimpleBuyStrategy

game = Game((SimpleBuyStrategy, SimpleBuyStrategy))

if __name__ == '__main__':
    game.initialize_game()
    game.process_game()
