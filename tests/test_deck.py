from spike_recorder.experiments.iowa.deck import Deck, FiniteDeck

import random
import pytest

def test_deck():
    pass


def test_finite_deck_seed():

    def make_deck(seed):
        return Deck.make_finite_deck(win_amounts=100,
                              loss_amounts=[0, 150, 200, 250, 300, 350],
                              loss_weights=[5, 1, 1, 1, 1, 1],
                              reshuffle=True,
                              seed=seed)

    deck1 = make_deck(seed=0)
    deck2 = make_deck(seed=0)
    deck3 = make_deck(seed=42)

    pulls1 = [deck1.pull() for i in range(100)]
    pulls2 = [deck2.pull() for i in range(100)]
    pulls3 = [deck3.pull() for i in range(100)]

    assert pulls1 == pulls2
    assert pulls1 != pulls3


def test_deck_reshuffle():

    win_amounts = 100
    loss_amounts = [0, 150, 200, 250, 300, 350]
    def make_deck(reshuffle):
        return Deck.make_finite_deck(win_amounts=win_amounts,
                                     loss_amounts=loss_amounts,
                                     loss_weights=[5, 1, 1, 1, 1, 1],
                                     reshuffle=reshuffle)

    deck1 = make_deck(reshuffle=True)

    # The deck should have 10 cards, reshuffle should happen after ten pulls
    pulls1 = [deck1.pull() for i in range(10)]
    pulls2 = [deck1.pull() for i in range(10)]

    assert pulls1 != pulls2
    assert set([win for win, loss in pulls1]) == set([win_amounts])
    assert set([loss for win, loss in pulls1]) == set(loss_amounts)

    deck2 = make_deck(reshuffle=False)
    pulls3 = [deck2.pull() for i in range(10)]

    with pytest.raises(RuntimeError):
        deck2.pull()


def test_no_deck_interaction():

    def make_decks():
        # Define the deck behaviour
        deck1 = Deck.make_finite_deck(win_amounts=100,
                                      loss_amounts=[0, 150, 200, 250, 300, 350],
                                      loss_weights=[5, 1, 1, 1, 1, 1],
                                      seed=1)
        deck2 = Deck.make_finite_deck(win_amounts=100,
                                      loss_amounts=[0, 1250],
                                      loss_weights=[9, 1],
                                      seed=2)
        deck3 = Deck.make_finite_deck(win_amounts=50,
                                      loss_amounts=[0, 25, 50, 75],
                                      loss_weights=[4, 3, 2, 1],
                                      seed=3)
        deck4 = Deck.make_finite_deck(win_amounts=50,
                                      loss_amounts=[0, 250],
                                      loss_weights=[9, 1],
                                      seed=4)

        return [deck1, deck2, deck3, deck4]


    def play():
        """Play 100 trials accross for decks, random choice of deck each turn. Keep track of pulls for each deck"""
        decks = make_decks()

        deck_pulls = {deck: [] for deck in decks}
        for i in range(100):
            deck = random.choice(decks)
            deck_pulls[deck].append(deck.pull())

        return decks, deck_pulls

    # Play two separate games with the same seed for each deck but different order of draws from each deck.
    decks1, deck_pulls1 = play()
    decks2, deck_pulls2 = play()

    # Make sure that for each game, each deck produces the same sequence of cards (since each game has the same
    # seed). This means the deck's randomness are not interacting.
    for deck1, deck2 in zip(decks1, decks2):
        pulls1 = deck_pulls1[deck1]
        pulls2 = deck_pulls2[deck2]

        # We won't have the same number of pulls from each deck in each game. Just compare them for as many
        # pulls as we have for both.
        min_pulls = min(len(pulls1), len(pulls2))
        assert pulls1[0:min_pulls] == pulls2[0:min_pulls]
