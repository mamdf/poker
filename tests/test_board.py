import pytest
from poker.card import Card, Rank
from poker.board import Board


def test_cards_are_Card_instances():
    board = Board("AsKcQh2c3h")
    for card in board.cards:
        assert isinstance(card, Card)

    for card in board.flop:
        assert isinstance(card, Card)

    assert isinstance(board.turn, Card)
    assert isinstance(board.river, Card)


def test_from_cards():
    board = Board.from_cards((Card("Qh"), Card("Kd"), Card("Ac"), Card("Ad")))
    assert isinstance(board, Board)
    assert board.cards == (Card("Ac"), Card("Kd"), Card("Qh"), Card("Ad"))


def test_flop_is_three_cards():
    board = Board("AsKcQh2c3h")
    assert len(board.flop) == 3
    assert tuple(board.cards[:3]) == board.flop


def test_turn_and_river_are_none_if_not_present():
    board = Board("AsKcQh")
    assert len(board.cards) == 3
    assert board.turn is None
    assert board.river is None
    board.add_cards('2c')
    assert len(board.cards) == 4
    assert board.river is None


def test_turn_and_river_are_present():
    board = Board("AsKcQh2c3h")
    assert board.turn == Card("2c")
    assert board.river == Card("3h")
    assert len(board) == 5
    # add_cards
    board = Board("AsKcQh")
    assert len(board) == 3
    board.add_cards("2c")
    assert len(board) == 4
    board.add_cards("3h")
    assert len(board) == 5
    assert board.river == Card("3h")

    board = Board("AsKcQh")
    assert len(board) == 3
    board.add_cards("AcAd")
    assert len(board) == 5
    assert board.turn == Card("Ac")
    assert board.river == Card("Ad")


def test_board_order():
    board = Board("3c3d3sAhAs")
    assert board.cards[0] == Card("3s") == board.flop[0]
    assert board.cards[1] == Card("3d") == board.flop[1]
    assert board.cards[2] == Card("3c") == board.flop[2]
    assert board.cards[3] == Card("Ah") == board.turn
    assert board.cards[4] == Card("As") == board.river

    board = Board("QcAcJcAsKc")
    assert board.cards[0] == Card("Ac") == board.flop[0]
    assert board.cards[1] == Card("Qc") == board.flop[1]
    assert board.cards[2] == Card("Jc") == board.flop[2]
    assert board.cards[3] == Card("As") == board.turn
    assert board.cards[4] == Card("Kc") == board.river


def test_invalid_board():
    # incorrect number of cards
    with pytest.raises(ValueError):
        Board("AsKcQh2c3h2c")
    with pytest.raises(ValueError):
        Board("AsKc")
    # repeated cards
    with pytest.raises(ValueError):
        Board("AcQdQd")
    with pytest.raises(ValueError):
        Board("3c3d3sAhAh")
    # invalid cards
    with pytest.raises(ValueError):
        Board("2c2d2k")


def test_invalid_add_cards():
    board = Board("AsKcQh")
    with pytest.raises(ValueError):
        board.add_cards("As")
    board = Board("AsKcQh")
    with pytest.raises(ValueError):
        board.add_cards("2c2c")
    board = Board("AsKcQh")
    with pytest.raises(ValueError):
        board.add_cards("2c2c")
    board = Board("AsKcQh")
    board.add_cards("2c")
    with pytest.raises(ValueError):
        board.add_cards("5d6h")
    board = Board("AsKcQh")
    board.add_cards("2c2d")
    with pytest.raises(ValueError):
        board.add_cards("5d")


def test_compare_boards():
    board1 = Board("AcKcQhJs")
    board2 = Board("QhKcAcJs")
    assert board1 == board2
    board1.add_cards("2c")
    assert board1 != board2
    board2.add_cards("2c")
    assert board1 == board2


def test_value():
    board = Board("AcKcQhJs")
    assert board.value == "AcKcQhJs"
    board.add_cards("Ad")
    assert board.value == "AcKcQhJsAd"


def test_is_rainbow():
    board = Board("AcKdQhJs")
    assert board.is_rainbow is True
    board = Board("AcKdQhJsTc")
    assert board.is_rainbow is False


def test_is_monotone():
    board = Board("AcKcQcJc")
    assert board.is_monotone is True
    board = Board("AcKcQcJcTc")
    assert board.is_monotone is True
    board = Board("AcKcQcJcTd")
    assert board.is_monotone is False


def test_has_straightdraw():
    board = Board("5c8cKd")
    assert board.has_straightdraw is True
    board = Board("5c9cKd")
    assert board.has_straightdraw is False
    board = Board("Ac3c9d")
    assert board.has_straightdraw is True


def test_has_gutshot():
    board = Board("5c9cKd")
    assert board.has_gutshot is True
    board = Board("2c7cKd")
    assert board.has_gutshot is False


def test_has_flushdraw():
    board = Board("5c9cKd")
    assert board.has_flushdraw is True
    board = Board("2c7hKd")
    assert board.has_flushdraw is False


class TestBoardRanking:
    board_high_card = Board("AcKdQhJs")
    board_pair = Board("AcKcKdQd")
    board_double = Board("AcKcQdQhKh")
    board_trips = Board("2c2d2h")
    board_straight = Board("AcKcQdJhTh")
    board_flush = Board("8s7s6s5sTs")
    board_full_house = Board("2c2d2hKcKh")
    board_quads = Board("2c2d2h2s")
    board_straight_flush = Board("AcKcQcJcTc")

    def test_has_pair(self):
        assert self.board_pair.has_pair is True
        assert self.board_high_card.has_pair is False

    def test_has_double(self):
        assert self.board_double.has_double is True
        assert self.board_pair.has_double is False
        assert self.board_trips.has_double is False

    def test_has_trip(self):
        assert self.board_trips.has_trip is True
        assert self.board_double.has_trip is False

    def test_has_straight(self):
        board = Board("AcKcQhJs")
        assert board.has_straight is False
        board.add_cards("Ts")
        assert board.has_straight is True

        board = Board("Ac2c4c5c")
        assert board.has_straight is False
        assert self.board_straight.has_straight is True
        assert self.board_trips.has_straight is False

    def test_has_flush(self):
        board = Board("Ac4c5c6c")
        assert board.has_flush is False
        board.add_cards("Tc")
        assert board.has_flush is True

        board = Board("8d7s6s5sTs")
        assert board.has_flush is False
        assert self.board_flush.has_flush is True
        assert self.board_trips.has_flush is False

    def test_has_full_house(self):
        assert self.board_full_house.has_full_house is True
        assert self.board_trips.has_full_house is False

    def test_has_quad(self):
        assert self.board_quads.has_quad is True
        assert self.board_full_house.has_quad is False

    def test_straight_flush(self):
        assert self.board_straight_flush.has_straight_flush is True
        assert self.board_flush.has_straight_flush is False
        assert self.board_straight.has_straight_flush is False

    def test_best_ranking(self):
        assert self.board_high_card.best_ranking == 0
        assert self.board_pair.best_ranking == 1
        assert self.board_double.best_ranking == 2
        assert self.board_trips.best_ranking == 3
        assert self.board_straight.best_ranking == 4
        assert self.board_flush.best_ranking == 5
        assert self.board_full_house.best_ranking == 6
        assert self.board_quads.best_ranking == 7
        assert self.board_straight_flush.best_ranking == 8


def test_straight_ranks():
    board = Board("AcKcQhJs")
    assert board._get_straight_ranks() == [1, 11, 12, 13, 14]
    board.add_cards("4d")
    assert board._get_straight_ranks() == [1, 4, 11, 12, 13, 14]

    board = Board("3d3c3h")
    assert board._get_straight_ranks() == [3]
    board.add_cards("As")
    assert board._get_straight_ranks() == [1, 3, 14]
    board.add_cards("Tc")
    assert board._get_straight_ranks() == [1, 3, 10, 14]


def test_possible_straights():
    board = Board("Ac9cJs")
    assert board.get_possible_straights(num_cards=1) == []
    assert board.get_possible_straights(num_cards=2) == []
    board.add_cards("Kd")
    assert board.get_possible_straights(num_cards=1) == []
    assert board.get_possible_straights(num_cards=2) == [[Rank("T"), Rank("Q")]]
    board.add_cards("Qh")
    assert board.get_possible_straights(num_cards=1) == [[Rank("T")]]

    board = Board("Ad3dQc5sTs")
    assert board.get_possible_straights(num_cards=1) == []
    assert board.get_possible_straights(num_cards=2) == [[Rank("2"), Rank("4")], [Rank("J"), Rank("K")]]

    board = Board("6s4s7s")
    assert board.get_possible_straights(num_cards=2) == [[Rank("3"), Rank("5")], [Rank("5"), Rank("8")]]
