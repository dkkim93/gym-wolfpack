import numpy as np


class Config(object):
    def __init__(self):
        super(Config, self).__init__()

        self._set_action_dict()
        self._set_orientation_dict()
        self._set_grid_dict()
        self._set_color_dict()

    def _set_action_dict(self):
        self.action_dict = {
            "stay": np.array([0, 0]),
            "move_up": np.array([-1, 0]),
            "move_down": np.array([1, 0]),
            "move_right": np.array([0, 1]),
            "move_left": np.array([+0, -1]),
            "spin_right": +1,
            "spin_left": -1,
        }

    def _set_orientation_dict(self):
        self.orientation_dict = {
            "up": 0,
            "right": 1,
            "down": 2,
            "left": 3,
        }

        self.orientation_delta_dict = {
            "up": np.array([-1, 0]),
            "right": np.array([0, 1]),
            "down": np.array([1, 0]),
            "left": np.array([+0, -1]),
        }

    def _set_grid_dict(self):
        self.grid_dict = {
            "empty": 0,
            "wall": 1,
            "prey": 2,
            "predator": 3,
            "orientation": 4,
        }

    def _set_color_dict(self):
        self.color_dict = {
            "empty": [0., 0., 0.],  # Black
            "wall": [0.5, 0.5, 0.5],  # Gray
            "prey": [1., 0., 0.],  # Red
            "predator": [0., 0., 1.],  # Blue
            "other_predator": [0., 0., 0.5],  # Light Blue
            "orientation": [0.1, 0.1, 0.1],  # Dark Gray
        }
