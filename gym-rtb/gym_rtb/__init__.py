from gym.envs.registration import register

register(
    id='rtb-v0',
    entry_point='gym_rtb.envs:RtbEnv',
)