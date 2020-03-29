import os
import gym
import numpy as np
from gym_env.wolfpack.config import Config
from gym_env.wolfpack.agent import Agent


class Base(gym.Env):
    def __init__(self, log, args):
        super(Base, self).__init__()

        self.log = log
        self.args = args
        self.config = Config()

    def _load_gridmap_array(self):
        # Ref: https://github.com/xinleipan/gym-gridworld/blob/master/gym_gridworld/envs/gridworld_env.py
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "maze.txt")
        with open(path, 'r') as f:
            gridmap = f.readlines()

        gridmap_array = np.array(
            list(map(lambda x: list(map(lambda y: int(y), x.split(' '))), gridmap)))
        return gridmap_array

    def _to_image(self, gridmap_array):
        image = np.zeros((gridmap_array.shape[0], gridmap_array.shape[1], 3), dtype=np.float32)

        for row in range(gridmap_array.shape[0]):
            for col in range(gridmap_array.shape[1]):
                grid = gridmap_array[row, col]

                if grid == self.config.grid_dict["empty"]:
                    image[row, col] = self.config.color_dict["empty"]
                elif grid == self.config.grid_dict["wall"]:
                    image[row, col] = self.config.color_dict["wall"]
                elif grid == self.config.grid_dict["prey"]:
                    image[row, col] = self.config.color_dict["prey"]
                elif grid == self.config.grid_dict["predator"]:
                    image[row, col] = self.config.color_dict["predator"]
                elif grid == self.config.grid_dict["orientation"]:
                    image[row, col] = self.config.color_dict["orientation"]
                else:
                    raise ValueError()

        return image

    def _render_gridmap(self):
        gridmap_image = np.copy(self.base_gridmap_image)

        # Render orientation
        for agent in self.agents:
            orientation_location = agent.orientation_location
            gridmap_image[orientation_location[0], orientation_location[1]] = self.config.color_dict["orientation"]
            
        # Render location
        for agent in self.agents:
            location = agent.location
            gridmap_image[location[0], location[1]] = self.config.color_dict[agent.type]

        # Pad image
        pad_width = ((self.pad, self.pad), (self.pad, self.pad), (0, 0))
        gridmap_image = np.pad(gridmap_image, pad_width, mode="constant")

        return gridmap_image

    def _reset_agents(self):
        self.agents = []
        for i_agent, agent_type in enumerate(["prey"] + ["predator" for _ in range(self.args.n_predator)]):
            agent = Agent(i_agent, agent_type, self.base_gridmap_array)
            self.agents.append(agent)

    def _get_observation(self, agent, gridmap_image):
        """As in  Leibo et al., AAMAS-17 (https://arxiv.org/pdf/1702.03037.pdf),
        the observation depends on each player’s current position and orientation. 
        Specifically, depending on the orientation, the image is cropped and then
        post-processed such that the player's location is always at the bottom center.
        """
        row, col = agent.location[0] + self.pad, agent.location[1] + self.pad
        height, half_width = self.observation_shape[0], int(self.observation_shape[1] / 2)

        if agent.orientation == self.config.orientation_dict["up"]:
            observation = gridmap_image[
                row - height + 1: row + 1, 
                col - half_width: col + half_width + 1, :]
        elif agent.orientation == self.config.orientation_dict["right"]:
            observation = gridmap_image[
                row - half_width: row + half_width + 1, 
                col: col + height, :]
            observation = np.rot90(observation, k=1)
        elif agent.orientation == self.config.orientation_dict["down"]:
            observation = gridmap_image[
                row: row + height, 
                col - half_width: col + half_width + 1, :]
            observation = np.rot90(observation, k=2)
        elif agent.orientation == self.config.orientation_dict["left"]:
            observation = gridmap_image[
                row - half_width: row + half_width + 1, 
                col - height + 1: col + 1, :]
            observation = np.rot90(observation, k=3)
        else:
            raise ValueError()

        assert observation.shape == self.observation_shape

        return observation
