from gym.envs.registration import register


########################################################################################
# WOLFPACK
register(
    id='wolfpack-v0',
    entry_point='gym_env.wolfpack.wolfpack_env:WolfPackEnv',
    kwargs={'args': None},
    max_episode_steps=50
)
