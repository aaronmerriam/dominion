import sys
import logging
import datetime

from .cards import Market, Copper, Silver, Gold, Estate, Duchy, Province, CardCollection
from .exceptions import WinCondition


def build_initial_hand():
    cards = [Copper() for i in xrange(7)] + [Estate() for i in xrange(3)]
    return CardCollection(cards)


def get_logger(name='dominion', filename=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(filename or datetime.datetime.now().strftime('logs/%Y-%m-%d-%f.log'))
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
    MAX_ROUNDS = 200

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

    def get_current_player(self):
        return self.players[self.get_turn()]

    def get_other_players(self):
        return filter(lambda p: not p == self.get_current_player(), self.players)

    def trash_card(self, card):
        assert self.get_current_player(), 'No current player set'
        self.log(logging.INFO, 'Player {0}: TRASH "{1}"'.format(self.get_turn(), card))
        self.trash.add_cards(card)

    def initialize_game(self):
        self.log(logging.DEBUG, 'Begin Game Initialization')
        self.trash = CardCollection()
        self.supply = Supply()
        self.players = []
        self.round = 0
        for i, PlayerClass in enumerate(self.player_classes):
            player = PlayerClass(game=self, deck=build_initial_hand())
            player.set_turn(self.build_turn(player, 0, i))
            self.players.append(player)
        self.log(logging.DEBUG, 'Finished Game Initialization')

    def build_turn(self, player, round=None, turn=None):
        """
        Helper for constructing a Turn object for a player.
        """
        if turn is None:
            turn = self.turn
        if round is None:
            round = self.round
        return Turn(
            game=self,
            hand_cards=[player.draw_card() for j in xrange(5)],
            turn=turn,
            round=round,
        )

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
        player.do_turn()
        player.cleanup_turn()
        player.set_turn(self.build_turn(player, self.round + 1, self.turn + 1))
        self.supply.check_win_conditions()
        self.log(logging.INFO, 'Finished Player {0} Turn'.format(self.get_turn()))


class Turn(object):
    available_actions = 1
    available_buys = 1
    available_treasure = 0

    def __init__(self, game, hand_cards, turn, round):
        self.game = game
        self.hand = CardCollection(hand_cards)
        self.turn = turn
        self.round = round
        self.discard = CardCollection()

    def log(self, level, message):
        self.game.log(level, message)

    def discard_cards(self, *cards):
        self.discard.add_cards(*cards)

    def get_event_kwargs(self, **kwargs):
        defaults = {
            'turn': self,
            'player': self.game.get_current_player(),
            'other_players': self.game.get_other_players(),
            'game': self.game,
        }
        defaults.update(kwargs)
        return defaults

    def play_action(self, card):
        assert self.available_actions, 'No more actions left'
        assert card.is_action, 'Non-action card played as action'
        self.available_actions -= 1
        self.log(logging.INFO, 'Player {0}: ACTION "{1}"'.format(self.turn, card))
        card.execute_events(**self.get_event_kwargs(card=card))
        self.discard_cards(card)

    def spend_treasures(self, *treasures):
        assert all(treasure.is_treasure for treasure in treasures), 'Attempting to spend non treasure cards'
        treasures = CardCollection(treasures)
        for treasure in treasures:
            self.game.log(logging.INFO, 'Player {0}: SPEND "{1}"'.format(self.game.get_turn(), treasure))
        self.available_treasure += treasures.total_treasure_value()
        self.discard_cards(*treasures)

    def buy_card(self, card):
        assert self.available_buys, 'No more buys left'
        assert card in self.game.supply.cards, 'This card is not available from the supply.'
        assert self.game.supply.cards[card], 'The supply is out of this card.'
        assert card.cost <= self.available_treasure, 'You cannot afford that card'
        card = self.game.supply.cards[card].draw_card()
        self.available_treasure -= card.cost
        self.available_buys -= 1
        self.game.log(logging.INFO, 'Player {0}: BUY "{1}"'.format(self.game.get_turn(), card))
        self.discard_cards(card)


class Supply(object):
    BASE_CARDS = dict((
        (Copper, 60),
        (Silver, 45),
        (Gold, 25),
        (Estate, 50),
        (Duchy, 25),
        (Province, 12),
    ))
    ACTION_CARDS = dict((
        (Market, 12),
    ))

    def __init__(self):
        self.cards = {}
        for Card, pile_size in self.BASE_CARDS.iteritems():
            self.cards[Card] = CardCollection((Card() for i in xrange(pile_size)))
        for Card, pile_size in self.ACTION_CARDS.iteritems():
            self.cards[Card] = CardCollection((Card() for i in xrange(pile_size)))

    def province_cards(self):
        return self.cards[Province]

    def action_cards(self):
        return [self.cards[key] for key in filter(lambda k: not k in self.BASE_CARDS, self.cards)]

    def affordable_cards(self, value):
        return filter(lambda c: c.cost <= value and self.cards[c], self.cards)

    def check_win_conditions(self):
        if sum(len(pile) < 3 for pile in self.action_cards()) > 2:
            raise WinCondition('Actions depleted')
        elif not len(self.province_cards()):
            raise WinCondition('Provinces depleted')
