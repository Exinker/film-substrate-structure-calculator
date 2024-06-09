import matplotlib.pyplot as plt
import numpy as np

from calculator.config import PITCH, THRESHOLD
from calculator.data import Data, Datum
from calculator.types import Array, MicroMeter

from .optimize import approximate


def calculate_distances(data: Data, save: bool = False, show: bool = False, verbose: bool = False) -> Array[MicroMeter]:

    distances = []
    for datum in data:
        distance = calculate_distance(
            datum=datum.truncate(THRESHOLD),
            show=show,
            verbose=verbose,
        )
        distances.append(distance)
    distances = np.array(distances)

    if save:
        raise NotImplementedError

    return distances


def calculate_distance(datum: Datum, pitch: MicroMeter = PITCH, show: bool = False, verbose: bool = False) -> MicroMeter:
    left, right = datum.split()

    positions = approximate(datum=left, show=show, verbose=verbose), approximate(datum=right, show=show, verbose=verbose)
    distance = pitch * (max(positions) - min(positions))

    if show:
        plt.show()

    return distance
