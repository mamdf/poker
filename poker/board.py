import collections
import itertools
from ._common import _ReprMixin
from .card import Rank, Card

__all__ = [
    "Board"
]

RANKING_NAMES = ("high_card", "pair", "two_pair", "three_of_a_kind", "straight", "flush", "full_house",
                 "four_of_a_kind", "straight_flush")


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

        self._suits = collections.Counter(card.suit for card in self.cards)
        self._all_ranks_counter = collections.Counter(card.rank for card in self.cards)
        self._straight_ranks = self._get_straight_ranks()

    def _get_straight_ranks(self) -> list:
        """return all unique rank cards as integers (Ace is 14 and 1)"""
        result = set(card.rank.value[1] for card in self.cards)
        # if As (14) in result append rank 1
        if 14 in result:
            result.add(1)
        return sorted(result)

    def get_possible_straights(self, num_cards=2) -> list:
        """
        num_cards: number of cards to complete a straight
        return: list of possible straights
        """
        result = []
        for i in range(len(self._straight_ranks)):
            # select number i + (5 - num_cards) items if exists
            n = (5 - num_cards)
            if i + n <= len(self._straight_ranks):
                # select n items from numbers
                ranks_split = self._straight_ranks[i:i + n]
                # create a range of numbers from the first to the last of the consecutive numbers
                range_of_numbers = range(max(1, ranks_split[0] - num_cards), min(ranks_split[-1] + num_cards + 1, 15))
                for j in range(len(range_of_numbers)):
                    if j + 5 <= len(range_of_numbers):
                        # select 5 items from range_of_numbers
                        range_of_numbers_5 = range_of_numbers[j:j + 5]
                        # check if the consecutive numbers are in the range of numbers
                        if all([x in range_of_numbers_5 for x in ranks_split]):
                            # append the ranks needed to complete the straight
                            str_ranks = [Rank(x) for x in range_of_numbers_5 if x not in ranks_split]
                            if str_ranks not in result:
                                result.append(str_ranks)

        return result

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
        return self._all_ranks_counter.most_common(1)[0][1] >= 2

    @property
    def has_double(self):
        if len(self._all_ranks_counter) < 2:
            return False
        result = self._all_ranks_counter.most_common(2)
        return result[0][1] >= 2 and result[1][1] >= 2

    @property
    def has_trip(self):
        return self._all_ranks_counter.most_common(1)[0][1] >= 3

    @property
    def has_straight(self):
        ranks_diff = self._get_differences()
        return ranks_diff.count(1) == 4

    @property
    def has_flush(self):
        return self.suit_count == 5

    @property
    def has_full_house(self):
        if len(self._all_ranks_counter) < 2:
            return False
        result = self._all_ranks_counter.most_common(2)
        return result[0][1] == 3 and result[1][1] == 2

    @property
    def has_quad(self):
        return self._all_ranks_counter.most_common(1)[0][1] == 4

    @property
    def has_straight_flush(self):
        return self.has_straight and self.has_flush

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
    def suit_count(self) -> int:
        return self._suits.most_common(1)[0][1]

    @property
    def best_ranking(self) -> int:
        """
        return the best ranking of the board (8 to 0)
        """
        if self.has_straight_flush:
            return 8
        if self.has_quad:
            return 7
        if self.has_full_house:
            return 6
        if self.has_flush:
            return 5
        if self.has_straight:
            return 4
        if self.has_trip:
            return 3
        if self.has_double:
            return 2
        if self.has_pair:
            return 1
        return 0

    def best_ranking_name(self) -> str:
        """
        return the best ranking name of the board
        """
        return RANKING_NAMES[self.best_ranking]

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
        """get differences between a sorted list numbers in self._straight_ranks"""
        return [y - x for x, y in zip(self._straight_ranks, self._straight_ranks[1:])]

    @property
    def value(self):
        result = ''
        for card in self.cards:
            result += card.value

        return result
