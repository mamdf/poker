Board API
=========

The :mod:`poker.board` module provides a reusable helper for working with community cards outside
of the room-specific hand-history classes.

.. currentmodule:: poker.board


Board
-----

.. autoclass:: poker.board.Board(board)

   :param str board:
      concatenated card string with 3, 4 or 5 cards, for example ``"AcKcQh"``,
      ``"AcKcQhJs"`` or ``"AcKcQhJsTd"``

   The constructor accepts a board string, another :class:`Board` instance, or use
   :meth:`Board.from_cards` to build from a sequence of :class:`poker.card.Card` objects.

   .. automethod:: from_cards

   .. automethod:: add_cards

   .. automethod:: get_possible_straights

   .. automethod:: best_ranking_name

   .. automethod:: suit_counts

   .. automethod:: ranks_for_suit

   .. autoattribute:: cards

      :type: tuple of :class:`poker.card.Card`

   .. autoattribute:: flop

      :type: tuple of :class:`poker.card.Card`

   .. autoattribute:: turn

      :type: :class:`poker.card.Card` or ``None``

   .. autoattribute:: river

      :type: :class:`poker.card.Card` or ``None``

   .. autoattribute:: value

      :type: str

   .. autoattribute:: is_rainbow

      :type: bool

   .. autoattribute:: is_monotone

      :type: bool

   .. autoattribute:: get_higher_ranks

      :type: list of :class:`poker.card.Rank`

   .. autoattribute:: has_pair

      :type: bool

   .. autoattribute:: has_double

      :type: bool

   .. autoattribute:: has_trip

      :type: bool

   .. autoattribute:: has_straight

      :type: bool

   .. autoattribute:: has_flush

      :type: bool

   .. autoattribute:: has_full_house

      :type: bool

   .. autoattribute:: has_quad

      :type: bool

   .. autoattribute:: has_straight_flush

      :type: bool

   .. autoattribute:: has_straightdraw

      :type: bool

   .. autoattribute:: has_gutshot

      :type: bool

   .. autoattribute:: has_flushdraw

      :type: bool

   .. autoattribute:: suit_count

      :type: int

   .. autoattribute:: best_ranking

      :type: int

      Ranking codes follow this order:
      ``0`` high card, ``1`` pair, ``2`` two pair, ``3`` trips, ``4`` straight,
      ``5`` flush, ``6`` full house, ``7`` quads, ``8`` straight flush
