import random
import numpy as np

from typing import List, Union, Optional


class Deck:
    """
    A bass class that defines and interface for a Iowa Gambling Task card deck.
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Abstract class to represent a deck of Iowa Gambling Task cards

        Args:
            seed: The random number generators seed, default is None, which causes seed
                based on time.
        """
        self.num_pulls = 0
        self.seed = seed

        # Instantiate and seed the random number generator. Use this to shuffle things.
        self._random = random.Random()
        self._random.seed(self.seed)

    def pull(self):
        """
        Pull a card from the deck.

        Note: Do not override this method in derived classes, instead, override Deck._pull

        Returns:
            A 2-tuple, (win_amount, loss_amount).
        """
        self.num_pulls = self.num_pulls + 1
        return self._pull()

    def _pull(self):
        raise NotImplementedError("_pull method not implemented for base class. Derive a class and implement the"
                                  " pull method.")

    @classmethod
    def make_deck(cls,
                  win_amounts: Union[int, List[int]],
                  loss_amounts: Union[int, List[int]],
                  win_weights: Union[None, int, List[int]] = None,
                  loss_weights: Union[None, int, List[int]] = None) -> 'Deck':
        """
        Generate a Deck class implementation for a given set of win and loss amounts and weights.

        Args:
            win_amounts: The possible winning amounts for this deck. If scalar, constant win amount is returned.
            loss_amounts: The possible loss amounts for this deck. If scalar, constant loss amount is returned.
            win_weights: If a weights sequence is specified, win selections are made according to the relative weights.
            loss_weights: If a weights sequence is specified, loss selections are made according to the relative weights

        Returns:
            An instance of a Deck class that implements the described distributions of wins and losses.
        """

        win_amounts = np.atleast_1d(win_amounts)
        loss_amounts = np.atleast_1d(loss_amounts)

        if win_weights is not None:
            win_weights = np.atleast_1d(win_weights)

        if loss_weights is not None:
            loss_weights = np.atleast_1d(loss_weights)

        if win_weights is not None and len(win_amounts) != len(win_weights):
            raise ValueError("The number of win amounts must have the same legnth and win weights")

        if loss_weights is not None and len(loss_amounts) != len(loss_weights):
            raise ValueError("The number of loss amounts must have the same legnth and loss weights")

        # FIXME: Right now the decks are done probabilistically
        # wins = random.shuffle([amount for count in win_weights for amount in win_amounts])
        # losses = random.shuffle([amount for count in win_weights for amount in win_amounts])

        class DeckImpl(Deck):
            def _pull(self):
                win_amount = self._random.choices(population=win_amounts, weights=win_weights, k=1)
                loss_amount = self._random.choices(population=loss_amounts, weights=loss_weights, k=1)
                return (win_amount[0], loss_amount[0])

        return DeckImpl()

    @classmethod
    def make_finite_deck(cls,
                         win_amounts: Union[int, List[int]],
                         loss_amounts: Union[int, List[int]],
                         win_weights: Union[None, int, List[int]] = None,
                         loss_weights: Union[None, int, List[int]] = None,
                         reshuffle: bool = True,
                         seed: Optional[int] = None) -> 'Deck':
        """
        Generate a Deck class implementation for a given set of win and loss amounts and weights.

        Args:
            win_amounts: The possible winning amounts for this deck. If scalar, constant win amount is returned.
            loss_amounts: The possible loss amounts for this deck. If scalar, constant loss amount is returned.
            win_weights: If a weights sequence is specified, win selections are made according to the relative weights.
            loss_weights: If a weights sequence is specified, loss selections are made according to the relative weights
            reshuffle: True causes deck to be reshuffled when cards are exhausted from pulls, False causes a ValueError.
                Default is True.
            seed: A seed for the random number generator for the deck. Default is time based.

        Returns:
            An instance of a Deck class that implements the described distributions of wins and losses.
        """

        win_amounts = np.atleast_1d(win_amounts)
        loss_amounts = np.atleast_1d(loss_amounts)

        if win_weights is not None:
            win_weights = np.atleast_1d(win_weights)

        if loss_weights is not None:
            loss_weights = np.atleast_1d(loss_weights)

        if win_weights is not None and len(win_amounts) != len(win_weights):
            raise ValueError("The number of win amounts must have the same length and win weights")

        if loss_weights is not None and len(loss_amounts) != len(loss_weights):
            raise ValueError("The number of loss amounts must have the same length and loss weights")

        if loss_weights is None and win_weights is None:
            raise ValueError("Deck size can't be determined without some weights.")

        if win_weights is None:
            win_weights = np.array([sum(loss_weights)])

        if loss_weights is None:
            loss_weights = np.array([sum(win_weights)])

        wins = [amount for amount, count in zip(win_amounts, win_weights) for i in range(count)]
        losses = [amount for amount, count in zip(loss_amounts, loss_weights) for i in range(count)]

        return FiniteDeck(wins=wins, losses=losses, reshuffle=reshuffle, seed=seed)


class FiniteDeck(Deck):
    """
    An implementation of a finite sizes deck.

    Args:
        wins: The list of winning values. Must be the same length as losses.
        losses: The list of losing values. Must be the same laenght as wins.
        reshuffle: Whether to reshuffle the deck when all cards have been pulled. If False,
            throw a ValueError when deck is exhausted.
        seed: The seed for the RNG, defaults to time based seed.

    """
    def __init__(self, wins: List[int], losses: List[int], reshuffle: bool = True, seed: Optional[int] = None):
        super(FiniteDeck, self).__init__(seed=seed)

        if len(wins) != len(losses):
            raise ValueError("Wins and Losses must be same length for FiniteDeck, they represent the wins and losses "
                             "for each card")

        self.deck_size = len(wins)
        self._wins = wins
        self._losses = losses
        self._reshuffle = reshuffle

        # Shuffle the deck
        self.shuffle()

    def shuffle(self):
        self._random.shuffle(self._wins)
        self._random.shuffle(self._losses)

    def _pull(self):

        num_pulls_this_shuffle = (self.num_pulls-1) % len(self._wins)

        if self.num_pulls > self.deck_size and not self._reshuffle:
            raise RuntimeError("No more cards left to draw from this finite deck.")

        win_amount = self._wins[num_pulls_this_shuffle]
        loss_amount = self._losses[num_pulls_this_shuffle]

        if num_pulls_this_shuffle == self.deck_size-1:
            if self._reshuffle:
                self.shuffle()

        return (win_amount, loss_amount)

