Fork Additions
==============

This fork adds a small set of features that are not described in the upstream documentation.
The goal of this page is to explain what changed, what each addition is for, and the most
useful ways to use them from application code.


Board Helper
------------

The new :class:`poker.board.Board` class represents the community cards as a reusable object.
It is useful when you want to inspect board texture outside of hand-history parsing, or when
you want richer helpers than the tuple returned by ``HandHistory.board``.

Create a board from a concatenated card string:

.. code-block:: python

   >>> from poker import Board
   >>> board = Board("AcKcQh")
   >>> board.cards
   (Card('A♣'), Card('K♣'), Card('Q♥'))
   >>> board.value
   'AcKcQh'

Build it incrementally from flop to river:

.. code-block:: python

   >>> board = Board("AcKcQh")
   >>> board.turn is None
   True
   >>> board.add_cards("JsTd")
   >>> board.turn, board.river
   (Card('J♠'), Card('T♦'))
   >>> board.best_ranking_name()
   'straight'

Or create it from existing :class:`poker.card.Card` objects:

.. code-block:: python

   >>> from poker import Board, Card
   >>> Board.from_cards((Card("Qh"), Card("Kd"), Card("Ac")))
   Board('A♣K♦Q♥')

The class normalizes the board to a canonical order. This means two boards with the same cards
compare equal even if the flop cards were passed in a different order:

.. code-block:: python

   >>> Board("AcKcQhJs") == Board("QhKcAcJs")
   True

Board helpers are grouped into a few categories:

- Structure: ``cards``, ``flop``, ``turn``, ``river``, ``value``, ``__len__``
- Texture: ``is_rainbow``, ``is_monotone``, ``has_pair``, ``has_double``, ``has_trip``,
  ``has_straightdraw``, ``has_gutshot``, ``has_flushdraw``
- Made hands: ``has_straight``, ``has_flush``, ``has_full_house``, ``has_quad``,
  ``has_straight_flush``, ``best_ranking``, ``best_ranking_name()``
- Suit and rank inspection: ``get_higher_ranks``, ``get_possible_straights()``,
  ``suit_count``, ``suit_counts()``, ``ranks_for_suit()``

Examples:

.. code-block:: python

   >>> from poker import Board, Suit
   >>> board = Board("AcKcQh")
   >>> board.get_possible_straights(num_cards=2)
   [[Rank('T'), Rank('J')]]
   >>> board.suit_counts()[Suit.CLUBS]
   2
   >>> board.ranks_for_suit(Suit.CLUBS)
   [Rank('A'), Rank('K')]

``HandHistory.board`` still returns a tuple of cards. If you want the richer board API, wrap it:

.. code-block:: python

   >>> from poker import Board
   >>> board = Board.from_cards(hh.board)


Card, Rank and Combo Additions
------------------------------

This fork adds a few small helpers that make it easier to serialize cards and work with straights.

``Rank`` now accepts numeric aliases for face cards, and Ace works as both high and low:

.. code-block:: python

   >>> from poker import Rank
   >>> Rank(11), Rank(12), Rank(13)
   (Rank('J'), Rank('Q'), Rank('K'))
   >>> Rank(14), Rank(1)
   (Rank('A'), Rank('A'))

``Card.value`` returns the ASCII-friendly version of a card, using ``c``, ``d``, ``h`` and ``s``
instead of the unicode suit symbols:

.. code-block:: python

   >>> from poker import Card
   >>> Card("A♠").value
   'As'

``Combo.value`` does the same for exact two-card combinations, and ``Combo.suits`` returns the
set of suits contained in the combo:

.. code-block:: python

   >>> from poker.hand import Combo
   >>> combo = Combo("KhAs")
   >>> combo.value
   'AsKh'
   >>> combo.suits
   {Suit('♥'), Suit('♠')}

For the full reference of the new board object, see :doc:`api/board`.
