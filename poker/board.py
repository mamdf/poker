import collections
import itertools
from ._common import _ReprMixin
from .card import Rank, Card

__all__ = [
    "Board"
]


class Board(_ReprMixin):
    """
    A board is a set of cards.
    """

    def __new__(cls, board):
        if isinstance(board, Board):
            return board

        if len(board) != 6 and len(board) != 8 and len(board) != 10:
            raise ValueError("%r, should have a length of 6-8-10" % board)

        self = super().__new__(cls)

        turn_card = Card(board[6:8]) if len(board) >= 8 else None
        river_card = Card(board[8:]) if len(board) == 10 else None
        self._set_cards(board[:2], board[2:4], board[4:6], turn_card, river_card)
        self._create_all_combinations()

        return self

    @classmethod
    def from_cards(cls, cards):
        """
        Create a board from a list of cards.
        """
        board = ""
        for card in cards:
            board += card.rank.val + card.suit.val
        return Board(board)

    def __str__(self):
        result = ''
        for card in self.cards:
            result += str(card)

        return result

    def __hash__(self):
        result = 0
        for card in self.cards:
            result += hash(card)

        return result

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.cards == other.cards
        return NotImplemented

    def __len__(self):
        return len(self.cards)

    def _set_cards(self, first, second, third, turn, river):
        self._cards = sorted([Card(first), Card(second), Card(third)], reverse=True)
        if turn:
            self._cards.append(Card(turn))
        if river:
            self._cards.append(Card(river))

    def add_cards(self, cards):
        if len(cards) == 2:
            cards = [Card(cards)]
        elif len(cards) == 4:
            cards = [Card(cards[:2]), Card(cards[2:])]
        else:
            raise ValueError("%r, should have a length of 2 or 4" % cards)

        if len(cards) == 2:
            if cards[0] == cards[1]:
                raise ValueError(f"{cards}, Pair can't have the same suit: {cards[0].suit!r}")

        if len(self.cards) + len(cards) > 5:
            raise ValueError("Board is already full")
        for card in cards:
            if card in self.cards:
                raise ValueError(f"{card!r}, already in board {self.cards}")

        self._cards.extend(cards)
        self._create_all_combinations()  # create new combinations

    def _create_all_combinations(self):
        """
        Create all combinations of cards and counter all ranks to check for straights, flushdraws, etc.
        """
        self._all_combinations = tuple(itertools.combinations(self.cards, 2))
        for comb in self._all_combinations:
            if comb[0] == comb[1]:
                raise ValueError(f"{comb}, Pair can't have the same suit: {comb[0].suit!r}")

        self._all_ranks_counter = collections.Counter(card.rank for card in self.cards)

    @property
    def is_rainbow(self):
        return all(
            first.suit != second.suit for first, second in self._all_combinations
        )

    @property
    def is_monotone(self):
        return all(
            first.suit == second.suit for first, second in self._all_combinations
        )

    @property
    def has_pair(self):
        return any(
            first.rank == second.rank for first, second in self._all_combinations
        )

    @property
    def has_double(self):
        result = self._all_ranks_counter.most_common(2)
        return result[0][1] >= 2 and result[1][1] >= 2

    @property
    def has_trip(self):
        return self._all_ranks_counter.most_common(1)[0][1] >= 3

    @property
    def has_full_house(self):
        result = self._all_ranks_counter.most_common(2)
        return result[0][1] == 3 and result[1][1] == 2

    @property
    def has_quad(self):
        return self._all_ranks_counter.most_common(1)[0][1] == 4

    @property
    def has_straightdraw(self):
        return any(1 <= diff <= 3 for diff in self._get_differences())

    @property
    def has_gutshot(self):
        return any(1 <= diff <= 4 for diff in self._get_differences())

    @property
    def has_flushdraw(self):
        return any(
            first.suit == second.suit for first, second in self._all_combinations
        )

    @property
    def flop(self):
        return tuple(self.cards[:3])

    @property
    def turn(self):
        if len(self.cards) >= 4:
            return self.cards[3]

    @property
    def river(self):
        if len(self.cards) == 5:
            return self.cards[4]

    @property
    def cards(self):
        return tuple(self._cards)

    def _get_differences(self):
        return (
            Rank.difference(first.rank, second.rank)
            for first, second in self._all_combinations
        )

    @property
    def value(self):
        result = ''
        for card in self.cards:
            result += card.value

        return result

