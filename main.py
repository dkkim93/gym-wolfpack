import os
import argparse
import torch
import random
import numpy as np
from misc.utils import set_log, make_env


def main(args):
    # Create directories
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    # Set logs
    log = set_log(args)

    # Create env
    env = make_env(log, args)

    # Set seeds
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    env.seed(args.seed)

    # Visualize environment
    observations = env.reset()

    for _ in range(args.ep_max_timesteps):
        env.render()

        prey_action = env.action_space.sample()
        predator1_action = env.action_space.sample()
        predator2_action = env.action_space.sample()
        actions = [prey_action, predator1_action, predator2_action]

        observations, reward, done, _ = env.step(actions)

        if done:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")

    # Env
    parser.add_argument(
        "--env-name", type=str, default="",
        help="OpenAI gym environment name")
    parser.add_argument(
        "--ep-max-timesteps", type=int, default=150,
        help="Episode is terminated when max timestep is reached")
    parser.add_argument(
        "--n-predator", type=int, default=2,
        help="Number of predators")

    # Misc
    parser.add_argument(
        "--prefix", type=str, default="", 
        help="Prefix for tb_writer and logging")
    parser.add_argument(
        "--seed", type=int, default=1, 
        help="Sets Gym, PyTorch and Numpy seeds")

    args = parser.parse_args()

    # Set log name
    args.log_name = \
        "env::%s_seed::%s_n_predator::%s_prefix::%s_log" % (
            args.env_name, args.seed, args.n_predator, args.prefix)

    main(args=args)
