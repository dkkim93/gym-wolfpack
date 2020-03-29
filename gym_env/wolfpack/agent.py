import numpy as np
from gym_env.wolfpack.config import Config


class Agent(object):
    def __init__(self, i_agent, agent_type, base_gridmap_array):
        self.id = i_agent
        self.type = agent_type
        self.base_gridmap_array = base_gridmap_array

        self.config = Config()

        self._location = self._reset_location()
        self._orientation = self.config.orientation_dict["up"]

    def _reset_location(self):
        location = np.array([
            np.random.choice(self.base_gridmap_array.shape[0]), 
            np.random.choice(self.base_gridmap_array.shape[1])])
        grid = self.base_gridmap_array[location[0], location[1]]

        while grid != self.config.grid_dict["empty"]:
            location = np.array([
                np.random.choice(self.base_gridmap_array.shape[0]), 
                np.random.choice(self.base_gridmap_array.shape[1])])
            grid = self.base_gridmap_array[location[0], location[1]]

        return location

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        grid = self.base_gridmap_array[value[0], value[1]]
        if grid != self.config.grid_dict["wall"]:
            self._location = value

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value % len(self.config.orientation_dict)

    @property
    def orientation_location(self):
        orientation = list(self.config.orientation_dict.keys())[self._orientation]
        orientation_delta = self.config.orientation_delta_dict[orientation]
        self._orientation_location = self.location + orientation_delta

        grid = self.base_gridmap_array[self._orientation_location[0], self._orientation_location[1]]
        if grid == self.config.grid_dict["wall"]:
            self._orientation_location = np.copy(self.location)

        return self._orientation_location
