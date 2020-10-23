# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import random
import numpy as np
from .search_tracker import SearchTracker


class BaseOptimizer(SearchTracker):
    def __init__(self, search_space):
        super().__init__()
        self.search_space = search_space
        self.dim_sizes = np.array(
            [len(array) for array in search_space.values()]
        )
        self.search_space_positions = np.array(
            [range(len(array)) for array in search_space.values()]
        )
        self.max_positions = self.dim_sizes - 1
        self.search_space_values = list(search_space.values())

        self.optimizers = [self]

    def move_random(self):
        position = []
        for search_space_pos in self.search_space_positions:
            pos_ = random.choice(search_space_pos)
            position.append(pos_)

        return np.array(position)

    def track_nth_iter(func):
        def wrapper(self, *args, **kwargs):
            self.nth_iter = len(self.pos_new_list)
            pos = func(self, *args, **kwargs)
            self.pos_new = pos
            return pos

        return wrapper

    def random_restart(func):
        def wrapper(self, *args, **kwargs):
            if self.rand_rest_p > random.uniform(0, 1):
                return self.move_random()
            else:
                return func(self, *args, **kwargs)

        return wrapper

    def init_pos(self, pos):
        self.nth_iter = len(self.pos_new_list)
        self.pos_new = pos

    def evaluate(self, score_new):
        self.score_new = score_new

        self._evaluate_new2current(score_new)
        self._evaluate_current2best()
