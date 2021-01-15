import pandas as pd
import attr
import typing


@attr.s(auto_attribs=True)
class LibetRecord:
    trial: int
    stop_time_msecs: int
    urge_time_msecs: int


class LibetData:
    """
    A simple class to encapsulate the trial by trial data stored during the Libet experiment.
    """

    def __init__(self):
        self.data = []
        self.trial_idx = 0

    def add_trial(self, stop_time_msecs: int, urge_time_msecs: typing.Optional[int] = None):
        """
        Record a trial to the dataset.

        Args:
            stop_time_msecs: The record time when the user stopped the trial.
            urge_time_msecs: The reported time the user felt the urge to stop the trial.

        Returns:
            None
        """
        self.data.append(LibetRecord(trial=self.trial_idx,
                                     stop_time_msecs=stop_time_msecs,
                                     urge_time_msecs=urge_time_msecs))
        self.trial_idx = self.trial_idx + 1

    def remove_last_trial(self):
        """
        Remove the last trials data.

        Returns:
            None
        """
        if len(self.data) > 0:
            self.data.pop()
            self.trial_idx = self.trial_idx - 1

    def num_trials(self):
        """
        Get the number of trials recorded.

        Returns:
            The number of trials we have recorded.
        """
        return self.trial_idx



