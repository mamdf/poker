import pytest
from poker.card import Card
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
    board = Board.from_cards([Card("Qh"), Card("Kd"), Card("Ac"), Card("Ad")])
    assert isinstance(board, Board)
    assert board.cards == [Card("Ac"), Card("Kd"), Card("Qh"), Card("Ad")]


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
    # add_cards
    board = Board("AsKcQh")
    board.add_cards("2c")
    board.add_cards("3h")
    assert board.river == Card("3h")

    board = Board("AsKcQh")
    board.add_cards("AcAd")
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


def test_has_pair():
    board = Board("AcKcKdQd")
    assert board.has_pair is True
    board = Board("AcKcQd")
    assert board.has_pair is False


def test_has_double():
    board = Board("AcKcQdQhKh")
    assert board.has_double is True
    board = Board("AcKcQdQh")
    assert board.has_double is False


def test_has_trip():
    board = Board("2c2d2h")
    assert board.has_trip is True
    board = Board("2c2dKcKd")
    assert board.has_trip is False


def test_has_quad():
    board = Board("2c2d2h2s")
    assert board.has_quad is True
    board = Board("2c2d2hKcKd")
    assert board.has_quad is False


def test_has_straightdraw():
    board = Board("5c8cKd")
    assert board.has_straightdraw is True
    board = Board("5c9cKd")
    assert board.has_straightdraw is False


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


def test_compare_boards():
    board1 = Board("AcKcQhJs")
    board2 = Board("QhKcAcJs")
    assert board1 == board2
    board1.add_cards("2c")
    assert board1 != board2
    board2.add_cards("2c")
    assert board1 == board2




