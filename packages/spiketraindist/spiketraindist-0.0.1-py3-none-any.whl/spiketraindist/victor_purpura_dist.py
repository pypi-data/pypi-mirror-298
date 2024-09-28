import numpy as np
from numba import jit


@jit
def _victor_purpura_distance(spike_train_a: np.ndarray, spike_train_b: np.ndarray, cost: float) -> float:
    """ # noqa E501
    Inductive algorithm to calculate the spike time distance described in [1].

    The operation of this algorithm can be viewed as a two-dimensional spreadsheet, in which the cell in the ith row and jth column contains Gi,j.
    The initial row of the spreadsheet is filled by noting that Gi,1 = i, and the initial column is filled by noting that G1,j = j.
    Subsequent cells are filled with the formula of Eq. 3 from [1], which depends only on the cells immediately above and to the left.
    The value that appears in the final column of the final row (i = m, j = n) contains Gmn, which is the desired distance Dspike[q].

    [1] J. D. Victor and K. P. Purpura, “Nature and precision of temporal coding in visual cortex: a metric-space analysis,” Journal of Neurophysiology, vol. 76, no. 2. American Physiological Society, pp. 1310–1326, Aug. 01, 1996. doi: 10.1152/jn.1996.76.2.1310. Available: http://dx.doi.org/10.1152/jn.1996.76.2.1310

    Parameters
    ----------
    spike_train_a : np.ndarray
        The first spike train, represented as a 1D numpy array of spike times.
    spike_train_b : np.ndarray
        The second spike train, represented as a 1D numpy array of spike times.
    cost : float
        The cost of shifting a spike in time.

    Returns
    -------
    float
        The Victor-Purpura distance between the two spike trains.    
    """
    n_spikes_a = len(spike_train_a)
    n_spikes_b = len(spike_train_b)

    def _calculate_spreadsheet_row(previous_row: np.ndarray, i: int) -> np.ndarray:
        # Preallocation
        current_row = np.zeros(previous_row.shape)
        # Value from first coloumn, G1,i = i
        current_row[0] = i
        for j in range(1, len(current_row)):
            # Equation (3) from [1]
            current_row[j] = min(
                (
                    previous_row[j] + 1,
                    current_row[j - 1] + 1,
                    previous_row[j - 1] + cost * abs(spike_train_a[i - 1] - spike_train_b[j - 1]),
                )
            )
        return current_row

    # Preallocation
    current_row = np.zeros(n_spikes_b + 1)
    # The initial row of the spreadsheet is filled by noting that Gj,1 = j
    current_row[:] = np.arange(0, n_spikes_b + 1)
    # Calculate the rows of the spreadsheet, note that only the previous row is required to calculate next row.
    # The initial column is filled by noting that G1,i = i, (i ist the first value of each row).
    for i in range(1, n_spikes_a + 1):
        current_row = _calculate_spreadsheet_row(current_row, i)
    # The value that appears in the final column of the final row (i = m, j = n) contains Gmn, which is the desired
    # distance Dspike[q].
    distance = current_row[-1]
    return distance


def victor_purpura_distance(spike_train_a: np.ndarray, spike_train_b: np.ndarray, cost: float = 1.0) -> float:
    """
    Computes the "Victor-Purpura" or "spike time" distance between two spike trains.

    The Victor-Purpura distance is a metric for comparing spike trains, where spikes can be added, deleted,
    or shifted in time with specific costs associated with each operation. The distance between two spike trains
    is the minimum total cost needed to convert one spike train into the other.

    Parameters
    ----------
    spike_train_a : np.ndarray
        The first spike train, represented as a 1D numpy array of spike times.
    spike_train_b : np.ndarray
        The second spike train, represented as a 1D numpy array of spike times.
    cost : float, optional
        The cost of shifting a spike in time.
        If `cost` is 0.0, the distance is the absolute difference in the number of spikes "spike count distance".
        If `cost` is infinity, the distance is the sum of the number of spikes in both trains.
        Default is 1.0.

    Returns
    -------
    distance : float
        The Victor-Purpura distance between the two spike trains.

    Notes
    -----
    This implementation uses dynamic programming to compute the distance.

    References
    ---------- # noqa E501
    .. [1] J. D. Victor and K. P. Purpura, “Nature and precision of temporal coding in visual cortex: a metric-space analysis,” Journal of Neurophysiology, vol. 76, no. 2. American Physiological Society, pp. 1310–1326, Aug. 01, 1996. doi: 10.1152/jn.1996.76.2.1310. Available: http://dx.doi.org/10.1152/jn.1996.76.2.1310

    Examples
    --------
    >>> import numpy as np
    >>> from spiketraindist import victor_purpura_distance
    >>> spike_train_a = np.array([0.1, 0.3, 0.5])
    >>> spike_train_b = np.array([0.2, 0.4, 0.6])
    >>> victor_purpura_distance(spike_train_a, spike_train_b, cost=1.0)
    0.30000000000000004
    """

    n_spikes_a = len(spike_train_a)
    n_spikes_b = len(spike_train_b)

    if not isinstance(cost, (float, int)) or cost < 0 or isinstance(cost, bool):
        raise ValueError(f"Cost must be a non-negative number, provided: {cost}")
    # Special cases for cost:
    elif cost == 0.0:  # "spike count" metric
        return abs(n_spikes_a - n_spikes_b)
    elif cost == np.inf:  # m + n -2c, where c is the number of spike times in common
        return n_spikes_a + n_spikes_b - 2 * len(np.intersect1d(spike_train_a, spike_train_b))
    else:  # cost in [0, inf)
        return _victor_purpura_distance(spike_train_a, spike_train_b, cost)
