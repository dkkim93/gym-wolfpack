import gym
import numpy as np
import matplotlib.pyplot as plt
from gym_env.wolfpack.base import Base


class WolfPackEnv(Base):
    REWARD_LONELY = 1.
    REWARD_TEAM = 5.
    CAPTURE_RADIUS = 6.

    def __init__(self, args, log):
        super(WolfPackEnv, self).__init__(log=log, args=args)

        self.observation_shape = (11, 11, 3)  # Format: (height, width, channel)
        self.observation_space = gym.spaces.Box(low=0., high=1., shape=self.observation_shape)
        self.action_space = gym.spaces.Discrete(len(self.config.action_dict))
        self.pad = np.max(self.observation_shape) - 2

        self.base_gridmap_array = self._load_gridmap_array()
        self.base_gridmap_image = self._to_image(self.base_gridmap_array)

    def reset(self):
        self._reset_agents()
        gridmap_image = self._render_gridmap()

        observations = []
        for agent in self.agents:
            observation = self._get_observation(agent, gridmap_image)
            observations.append(observation)

        return observations

    def step(self, actions):
        assert len(actions) == self.args.n_predator + 1

        # Compute next locations
        for agent, action in zip(self.agents, actions):
            action = list(self.config.action_dict.keys())[action]

            if "spin" not in action: 
                next_location = agent.location + self.config.action_dict[action]
                next_orientation = agent.orientation
            else:
                next_location = agent.location
                next_orientation = agent.orientation + self.config.action_dict[action]
            agent.location = next_location
            agent.orientation = next_orientation

        # Get next observations
        gridmap_image = self._render_gridmap()

        observations = []
        for agent in self.agents:
            observation = self._get_observation(agent, gridmap_image)
            observations.append(observation)

        # Find who succeeded in hunting
        hunted_predator = None
        for predator in self.agents[1:]:
            if np.array_equal(self.agents[0].location, predator.location):
                hunted_predator = predator

        # Find nearby predators to the one succeeded in hunting
        nearby_predators = []
        if hunted_predator is not None:
            for predator in self.agents[1:]:
                if predator.id != hunted_predator.id:
                    dist = np.linalg.norm(predator.location - hunted_predator.location)
                    if dist < self.CAPTURE_RADIUS:
                        nearby_predators.append(predator)

        # Compute reward
        rewards = [0. for _ in range(len(self.agents))]
        if hunted_predator is not None:
            if len(nearby_predators) == 0:
                rewards[hunted_predator.id] = self.REWARD_LONELY
            else:
                rewards[hunted_predator.id] = self.REWARD_TEAM
                for neaby_predator in nearby_predators:
                    rewards[neaby_predator.id] = self.REWARD_TEAM

        # Compute done
        if hunted_predator is not None:
            done = True
        else:
            done = False

        return observations, rewards, done, {}
  
    def render(self, mode='human'):
        gridmap_image = self._render_gridmap()

        plt.figure(1)
        plt.clf()
        plt.imshow(gridmap_image)
        plt.axis('off')
        plt.pause(0.00001)
