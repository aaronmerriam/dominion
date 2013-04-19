import sys
import logging
import datetime

from .cards import Copper, Silver, Gold, Estate, Duchy, Province, CardCollection
from .exceptions import WinCondition, ProvincesDepleted, ActionsDepleted


def get_initial_hand():
    cards = [Copper() for i in xrange(7)] + [Estate() for i in xrange(3)]
    return CardCollection(*cards)


def get_logger(name='dominion', filename=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(filename or datetime.datetime.now().strftime('%Y-%m-%d-%f.log'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(level)
    return logger

DEFAULT_LOG_LEVEL = logging.DEBUG


class Game(object):
    round = None
    turn = None
    winner = None
    log_level = DEFAULT_LOG_LEVEL
    MAX_ROUNDS = 40

    def __init__(self, player_classes):
        assert len(player_classes) > 1, 'Cannot initiate a game with less than 2 players'
        self.player_classes = player_classes
        self.logger = get_logger(level=self.log_level)

    def log(self, level=DEFAULT_LOG_LEVEL, message=''):
        self.logger.log(level, message)

    def get_round(self):
        return self.round

    def get_turn(self):
        return self.turn

    def get_player_count(self):
        return len(self.players)

    def buy_card(self, card):
        assert self.current_player, 'No current player set'
        assert card in self.supply.cards, 'This card is not available from the supply.'
        assert self.supply.cards[card], 'The supply is out of this card.'
        card = self.supply.cards[card].draw_card()
        self.log(logging.INFO, 'Player {0}: BUY "{1}"'.format(self.get_turn(), card))
        return card

    def trash_card(self, card):
        assert self.current_player, 'No current player set'
        self.log(logging.INFO, 'Player {0}: TRASH "{1}"'.format(self.get_turn(), card))
        self.trash.add_cards(card)

    def initialize_game(self):
        self.log(logging.DEBUG, 'Begin Game Initialization')
        self.trash = CardCollection()
        self.supply = Supply()
        self.players = []
        self.round = 0
        for PlayerClass in self.player_classes:
            self.players.append(PlayerClass(
                game=self,
                deck=get_initial_hand()),
            )
        self.log(logging.DEBUG, 'Finished Game Initialization')

    def process_game(self):
        try:
            self.process_rounds_forever()
        except WinCondition:
            self.log(logging.INFO, 'Win Conditions Satisfied')
            self.process_win()
        self.process_no_win()

    def process_win(self):
        scores = dict([(i, p.victory_point_count()) for i, p in enumerate(self.players)])
        winner = max(scores, scores.get)
        self.log(logging.INFO, 'Player {0} Won'.format(winner))

    def process_no_win(self):
        pass

    def process_rounds_forever(self):
        while self.round < self.MAX_ROUNDS:
            self.process_round()
        self.log(logging.INFO, 'Round Limit Reached')

    def process_round(self):
        self.log(logging.INFO, 'Beginning Round {0}'.format(self.get_round()))
        self.turn = 0
        for i in xrange(len(self.players)):
            self.turn = i
            self.process_turn(self.players[i])
        self.round += 1
        self.log(logging.INFO, 'Finished Round {0}'.format(self.get_round()))
        self.turn = None

    def process_turn(self, player):
        self.log(logging.INFO, 'Beginning Player {0} Turn'.format(self.get_turn()))
        self.current_player = player
        player.do_turn()
        self.current_player = None
        self.supply.check_win_conditions()
        self.log(logging.INFO, 'Finished Player {0} Turn'.format(self.get_turn()))


class Supply(object):
    BASE_CARDS = dict((
        (Copper, 60),
        (Silver, 45),
        (Gold, 25),
        (Estate, 50),
        (Duchy, 25),
        (Province, 12),
    ))

    def __init__(self, action_card_classes=[]):
        self.cards = {}
        for Card, pile_size in self.BASE_CARDS.iteritems():
            self.cards[Card] = CardCollection(*(Card() for i in xrange(pile_size)))

    @property
    def provinces(self):
        return self.cards[Province]

    @property
    def actions(self):
        return [self.cards[key] for key in filter(lambda k: not k in self.BASE_CARDS, self.cards)]

    def check_win_conditions(self):
        if sum(len(pile) < 3 for pile in self.actions) > 2:
            raise ActionsDepleted
        elif not len(self.provinces):
            raise ProvincesDepleted
