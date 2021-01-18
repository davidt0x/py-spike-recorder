import random
import numpy as np

from typing import List, Union

class Deck:
    """
    A bass class that defines and interface for a Iowa Gambling Task card deck.
    """

    def __init__(self):
        self.num_pulls = 0

    def pull(self):
        """
        Pull a card fron the deck.

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

        class DeckImpl(Deck):
            def _pull(self):
                win_amount = random.choices(population=win_amounts, weights=win_weights, k=1)
                loss_amount = random.choices(population=loss_amounts, weights=loss_weights, k=1)
                return (win_amount[0], loss_amount[0])

        return DeckImpl()

